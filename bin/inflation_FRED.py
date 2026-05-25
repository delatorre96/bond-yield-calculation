# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:57:50 2026

@author: ignacio.delatorre
"""

from fredapi import Fred
import pandas as pd

fred = Fred(api_key='29eaeef7b1a969529bccd7a2ae9ee90c ')

fred_cpi_map = {
    'ee.uu.': 'CPIAUCSL',
    'u.s.': 'CPIAUCSL',

    'reino unido': 'GBRCPIALLMINMEI',
    'canadá': 'CPALCY01CAM661N',
    'japón': 'JPNCPIALLMINMEI',
    'suiza': 'CHECPIALLMINMEI',
    'australia': 'AUSCPIALLMINMEI',
    'nueva zelanda': 'NZLCPIALLMINMEI',

    'china': 'CHNCPIALLMINMEI',
    'india': 'INDCPIALLMINMEI',
    'brasil': 'BRACPIALLMINMEI',
    'méxico': 'MEXCPIALLMINMEI',
    'rusia': 'RUSCPIALLMINMEI',
    'turquía': 'TURCPIALLMINMEI',
    'corea del sur': 'KORCPIALLMINMEI',

    'sudáfrica': 'ZAFCPALTT01IXOBM',
}

fred_cpi_map = {
    'ee.uu.': 'CPIAUCSL',
    'reino unido': 'GBRCPIALLMINMEI',
    'japón': 'JPNCPIALLMINMEI',
    'canadá': 'CPALCY01CAM661N',
    'india': 'INDCPIALLMINMEI',
    'brasil': 'BRACPIALLMINMEI',
    'méxico': 'MEXCPIALLMINMEI',
    'china': 'CHNCPIALLMINMEI',
    'turquía': 'TURCPIALLMINMEI',
    'rusia': 'RUSCPIALLMINMEI',
    'corea del sur': 'KORCPIALLMINMEI',
}

all_data = []

for country, series_id in fred_cpi_map.items():
    try:
        s = fred.get_series(series_id)

        df = pd.DataFrame({
            'date': s.index,
            'cpi': s.values,
            'country': country
        })

        df = df.sort_values('date')

        df['inflation_mom'] = df['cpi'].pct_change(1) * 100
        df['inflation_yoy'] = df['cpi'].pct_change(12) * 100

        all_data.append(df)

    except Exception as e:
        print(country, series_id, e)

final = pd.concat(all_data)


