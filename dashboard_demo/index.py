from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import pandas as pd
from PriceIndices import MarketHistory, Indices

from PriceIndices import Indices, MarketHistory
import pandas as pd
import numpy as np
history = MarketHistory()

def get_coin_data(crypto='bitcoin', start_date='20130428', end_date='20200501', save_data=None):
    df = history.get_price(crypto, start_date, end_date)
    df_bi = Indices.get_bvol_index(df) # Bitmax Volatility Index
    df_bi.drop('price', axis=1, inplace=True)
    df_rsi = Indices.get_rsi(df)    # Relative Strength Index
    df_rsi.drop(['price', 'RS_Smooth', 'RSI_1'], axis=1, inplace=True)
    df_sma = Indices.get_simple_moving_average(df)  # Simple Moving Average
    df_sma.drop(['price'], axis=1, inplace=True)
    df_bb = Indices.get_bollinger_bands(df)      # Bollunger Bands
    df_bb.drop(['price'], axis=1, inplace=True)
    df_ema = Indices.get_exponential_moving_average(df, [20, 50]) # Exponential Moving Average
    df_ema.drop(['price'], axis=1, inplace=True)
    df_macd = Indices.get_moving_average_convergence_divergence(df) # Moving Average Convergence Divergence
    df_macd.drop(['price',], axis=1, inplace=True)

    df = pd.merge(df, df_macd, on='date', how='left')
    df = pd.merge(df, df_rsi, on='date', how='left')
    df = pd.merge(df, df_bi, on='date', how='left')
    df = pd.merge(df, df_bb, on='date', how='left')
    df = pd.merge(df, df_ema, on='date', how='left')
    df = pd.merge(df, df_sma, on='date', how='left')
    del df_rsi, df_macd, df_sma, df_bb, df_bi
    df.rename(columns={'RSI_2': 'RSI'}, inplace=True)
    df.fillna(0)
    for col in df.columns[1:]:
        df[col] = np.round(df[col], 2)
    while save_data:
        df.to_csv('data.csv', index=False)
        break
    return df

df1 = get_coin_data()