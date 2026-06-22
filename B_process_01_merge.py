# -*- coding: utf-8 -*-
"""
Created on Mon May 25 14:32:50 2026

@author: ignacio.delatorre
"""

def merge_data(exchRate,inflation,bonds,  save_csv = True):
    import os
    import pandas as pd
    from datetime import date
    today = date.today()
    
    
    ###### Exchange rate #######
    #exchRate = pd.read_csv('data_tmp/exchangeRate_2026-05-21.csv')
    exchRate_long = exchRate.melt(
        id_vars='Date',
        var_name='Currency',
        value_name='ExchangeRate'
    )
    
    currency_to_country = {
        'USD': 'united states',
        'JPY': 'japan',
        'CZK': 'czech republic',
        'DKK': 'denmark',
        'GBP': 'united kingdom',
        'HUF': 'hungary',
        'PLN': 'poland',
        'SEK': 'sweden',
        'CHF': 'switzerland',
        'NOK': 'norway',
        'AUD': 'australia',
        'CAD': 'canada',
        'HKD': 'hong kong',
        'KRW': 'south korea',
        'NZD': 'new zealand',
        'SGD': 'singapore',
        'ZAR': 'south africa',
        'EGP': 'egypt',
        'ILS': 'israel',
        'INR': 'india',
        'XOF': 'senegal',          # moneda compartida por varios países
        'BHD': 'bahrain',
        'IDR': 'indonesia',
        'MYR': 'malaysia',
        'ZMW': 'zambia',
        'BRL': 'brazil',
        'RSD': 'serbia',
        'PHP': 'philippines',
        'MAD': 'morocco',
        'KZT': 'kazakhstan',
        'MXN': 'mexico',
        'RON': 'romania',
        'UAH': 'ukraine',
        'UGX': 'uganda',
        'LKR': 'sri lanka',
        'VND': 'vietnam',
        'RUB': 'russia',
        'CLP': 'chile',
        'KES': 'kenya',
        'BDT': 'bangladesh',
        'BWP': 'botswana',
        'MUR': 'mauritius',
        'TRY': 'turkey',
        'NAD': 'namibia',
        'CNY': 'china',
        'THB': 'thailand'
    }
    exchRate_long['country'] = exchRate_long['Currency'].map(currency_to_country)
    exchRate_long['Date'] = pd.to_datetime(exchRate_long['Date'])
    countries_exchange = exchRate_long['country'].unique()
    countries_EUR = ['austria', 
           'belgium', 'croatia', 'cyprus', 'france', 'germany', 'greece', 
           'ireland', 'italy', 'poland', 'portugal',
           'romania', 'spain']
    ####incluir paises europeos con EUR exchange rate de 1
    all_eur_series = []
    for country_eur in countries_EUR:
        serie = exchRate_long[exchRate_long['country'] == 'thailand']
        serie['country'] = country_eur
        serie['ExchangeRate'] = 1
        serie['Currency'] = 'EUR'
        all_eur_series.append(serie)
    df_all_eur_series = pd.concat(all_eur_series).reset_index(drop = True)
    
    exchRate_long = pd.concat([exchRate_long, df_all_eur_series]).reset_index(drop = True)
    
    ###### Inflation #######
    #inflation = pd.read_csv('data_tmp/inflation_INE_2026-05-27.csv')
    inflation = inflation.rename(columns = {'fecha':'Date', 'indice':'IPC'}).drop(['inflacion_yoy','inflacion_mom'], axis = 1)
    inflation['Date'] = pd.to_datetime(inflation['Date'].str[:10])
    inflation = inflation.set_index('Date')
    daily_index = pd.date_range(
        start=inflation.index.min(),
        end=inflation.index.max() + pd.offsets.MonthEnd(0),
        freq='D'
    )
    inflation_daily = (
        inflation
        .reindex(daily_index, method='ffill')
        .rename_axis('Date')
        .reset_index()
    )
    
    
    df_merge_1 = pd.merge(inflation_daily.reset_index(drop = True), exchRate_long, on = 'Date', how = 'inner')
    
    ########## Bonds ###########
    #bonds = pd.read_csv('data_tmp/bonds_historical_data_2026-05-28.csv')
    bonds['Date'] = pd.to_datetime(bonds['Date'])
    import re
    
    def parse_tenor(x):
        m = re.search(r'(\d+)([MY])$', x)
        n = int(m.group(1))
        unit = m.group(2)
        return n, unit
    
    bonds[['n','unit']] = bonds['bond'].apply(
        lambda x: pd.Series(parse_tenor(x))
    )
    
    from pandas.tseries.offsets import DateOffset
    def maturity_date(row):
        if row['unit'] == 'Y':
            return row['Date'] + DateOffset(years=row['n'])
        else:
            return row['Date'] + DateOffset(months=row['n'])
    
    bonds['MaturityDate'] = bonds.apply(maturity_date, axis=1)
    bonds = bonds.drop(columns = {'n', 'unit'})
    bonds = bonds.rename(columns = {'Date' : 'EmissionDate'})
    df_merge_2 = bonds.merge(
        df_merge_1,
        left_on=['MaturityDate','country'],
        right_on=['Date','country'],
        how='left'
    ).drop(columns = 'Date')
    
    ##### Acumulated inflation ######
    df_merge_2 = df_merge_2.rename(columns={'IPC': 'IPC_end'})
    ipc_start = df_merge_1[['Date', 'country', 'IPC']].drop_duplicates()
    
    df_merge_2 = df_merge_2.merge(
        ipc_start,
        left_on=['EmissionDate', 'country'],
        right_on=['Date', 'country'],
        how='left'
    )
    
    df_merge_2 = df_merge_2.rename(columns={'IPC': 'IPC_start'})
    df_merge_2 = df_merge_2.drop(columns='Date')
    
    
    df_merge_2['accumulatedInflation'] = (
        df_merge_2['IPC_end'] / df_merge_2['IPC_start'] - 1
    )
    
    ######## Exchange rate de vuelta
    df_merge_2 = df_merge_2.rename(columns = {'ExchangeRate':'ExchangeRate_end'})
    
    df_merge_2 = df_merge_2.merge(
        exchRate_long,
        left_on=['EmissionDate', 'country', 'Currency'],
        right_on=['Date', 'country','Currency'],
        how='left'
    )
    df_merge_2 = df_merge_2.rename(columns = {'ExchangeRate' : 'ExchangeRate_start'})
    df_merge_2 = df_merge_2[[ 'country','EmissionDate', 'Interest', 'bond', 'MaturityDate',
           'IPC_end','IPC_start', 'accumulatedInflation','Currency', 'ExchangeRate_start','ExchangeRate_end' ]]
    
    df_merge_2 = df_merge_2.dropna()
    
    if save_csv:
        os.makedirs("data_tmp", exist_ok=True)
        df_merge_2.to_csv(f'data_tmp/series_data_{today}.csv',index = False)
    return df_merge_2
