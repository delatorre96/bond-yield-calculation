# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:11:05 2026

@author: ignacio.delatorre
"""
import wbdata
import pandas as pd
from datetime import datetime
from datetime import date
today = date.today()

currency_country = {
    'USD': 'US',
    'JPY': 'JP',
    'CZK': 'CZ',
    'DKK': 'DK',
    'GBP': 'GB',
    'HUF': 'HU',
    'PLN': 'PL',
    'SEK': 'SE',
    'CHF': 'CH',
    'NOK': 'NO',
    'AUD': 'AU',
    'CAD': 'CA',
    'HKD': 'HK',
    'KRW': 'KR',
    'NZD': 'NZ',
    'SGD': 'SG',
    'ZAR': 'ZA',
    'EGP': 'EG',
    'ILS': 'IL',
    'INR': 'IN',
    'BHD': 'BH',
    'IDR': 'ID',
    'MYR': 'MY',
    'ZMW': 'ZM',
    'BRL': 'BR',
    'RSD': 'RS',
    'PHP': 'PH',
    'MAD': 'MA',
    'KZT': 'KZ',
    'MXN': 'MX',
    'RON': 'RO',
    'UAH': 'UA',
    'UGX': 'UG',
    'LKR': 'LK',
    'VND': 'VN',
    'RUB': 'RU',
    'CLP': 'CL',
    'KES': 'KE',
    'BDT': 'BD',
    'BWP': 'BW',
    'MUR': 'MU',
    'TRY': 'TR',
    'NAD': 'NA',
    'CNY': 'CN',
    'THB': 'TH',
}


indicator = {'FP.CPI.TOTL.ZG': 'inflation'}

all_data = []

for ccy, country in currency_country.items():

    try:
        df = wbdata.get_dataframe(
            indicator,
            country=country,
            date=(datetime(2000,1,1), datetime(2025,1,1))
        )

        df = df.reset_index()

        df['FX_code'] = ccy

        all_data.append(df)

    except Exception as e:
        print(ccy, e)

inflation_df = pd.concat(all_data)
inflation_df = inflation_df.pivot(
    index='date',
    columns='FX_code',
    values='inflation'
)


inflation_df.to_csv(f'inflation_FRED_{today}.csv')
