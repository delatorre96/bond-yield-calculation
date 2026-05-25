# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:34:34 2026

@author: ignacio.delatorre
"""

import zipfile
from io import BytesIO
import requests
import pandas as pd
from datetime import date
today = date.today()
######################## TIPO DE CAMBIO ###########################

### Para 'PLN', 'CAD', 'NZD', 'JPY', 'HKD', 'ZAR', 'DKK', 'CZK', 'CHF', 'AUD', 'KRW', 'SEK', 'SGD', 'NOK', 'GBP', 'HUF', 'USD'
## Usamos las estadísticas oficiales dela Unión Europea
url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
r = requests.get(url)

z = zipfile.ZipFile(BytesIO(r.content))
file_name = z.namelist()[0]

with z.open(file_name) as f:
    df_forex = pd.read_csv(f)
df_forex = df_forex.dropna(axis = 1)


#### Para el resto, tenemos que usar fuentes alternativas
import yfinance as yf

currencies = [
    'NAD', 'CLP', 'UGX', 'INR', 'XOF', 'MYR', 'CNY',
    'RON', 'BHD', 'KZT', 'IDR', 'MXN', 'THB',
    'UAH', 'EGP', 'BRL', 'LKR', 'MAD', 'KES', 'VND',
    'BWP', 'MUR', 'TRY', 'BDT', 'ILS', 'RUB', 'ZMW',
    'RSD', 'PHP'
]
tickers = [f"EUR{ccy}=X" for ccy in currencies]

data = yf.download(
    tickers,
    start="2000-01-01",
    end= today,
    auto_adjust=True,
    progress=False,
    group_by='ticker'
)
df_yf = data.xs('Close', level='Price', axis=1)
df_yf.columns = [
    col.replace('EUR', '').replace('=X', '')
    for col in df_yf.columns
]

##### Unimos data frames
df_forex['Date'] = pd.to_datetime(df_forex['Date'])
df_yf.index = pd.to_datetime(df_yf.index)
df_yf = df_yf.reset_index()
df_final = df_forex.merge(
    df_yf,
    on='Date',
    how='left'
)


df_final.to_csv(f'data_tmp/exchangeRate_{today}.csv', index=False)
