# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:55:23 2026

@author: ignacio.delatorre
"""
import pandas as pd
from datetime import date
today = date.today()

df = pd.read_csv('data_tmp/series_data_2026-06-14.csv')


df['rentability'] = ((df['ExchangeRate_start'] *(1 + df['Interest']))/(df['ExchangeRate_end'] * (1 + df['accumulatedInflation']))) - 1


df = df.sort_values(by = 'rentability', ascending = False).reset_index(drop = True)


df.to_csv(f'data_tmp/series_data_{today}.csv',index = False)
