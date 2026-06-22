# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:55:23 2026

@author: ignacio.delatorre
"""

def real_rentability_calculation (df_merge_2, save_csv = True):
    
    import os
    import pandas as pd
    from datetime import date
    today = date.today()
    
    
    df_merge_2['rentability'] = ((df_merge_2['ExchangeRate_start'] *(1 + df_merge_2['Interest']))/(df_merge_2['ExchangeRate_end'] * (1 + df_merge_2['accumulatedInflation']))) - 1
    
    
    df_merge_2 = df_merge_2.sort_values(by = 'rentability', ascending = False).reset_index(drop = True)
    
    if save_csv:
        os.makedirs("data_tmp", exist_ok=True)
        df_merge_2.to_csv(f'data_tmp/series_data_{today}.csv',index = False)
    return df_merge_2
    
    
