# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:29:03 2026

@author: ignacio.delatorre
"""
def extract_inflation_historical_data(save_csv = True):
    import os
    import requests
    import pandas as pd
    from datetime import date
    today = date.today()
    
    # TABLA IPC DETALLADA
    TABLE_ID = 79184
    
    url = f"https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/{TABLE_ID}?tip=AM"
    
    data = requests.get(url).json()
    
    series = []
    
    for s in data:
        nombre = s.get("Nombre")
        cod = s.get("COD")
    
        for obs in s.get("Data", []):
            series.append({
                "cod": cod,
                "categoria": nombre,
                "fecha": obs["Fecha"],
                "indice": obs["Valor"]
            })
    
    df = pd.DataFrame(series)
    
    df["fecha"] = (
        df["fecha"]
        .str.replace("M", "-")
    )
    
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.drop(['cod','categoria'], axis = 1)
    
    df = df.groupby("fecha").mean()
    
    
    df = df.sort_values(["fecha"])
    
    df["inflacion_yoy"] = (
        df["indice"]
          .pct_change(12)
          
    )
    df["inflacion_mom"] = (
        df["indice"]
          .pct_change(1)
    )
    
    
    
    if save_csv:
        os.makedirs("data_tmp", exist_ok=True)
        df.to_csv(f'data_tmp/inflation_INE_{today}.csv')
    return df