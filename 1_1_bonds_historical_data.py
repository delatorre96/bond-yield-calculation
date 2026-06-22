# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:29:10 2026

@author: ignacio.delatorre
"""
import investpy
import pandas as pd
import numpy as np
import re
import time
import random
from datetime import date
today = date.today()
today_str = today.strftime("%d/%m/%Y")

def maturity_to_years(name):

    match = re.search(r'(\d+)([YM])', name)

    if match is None:
        return np.nan

    value = int(match.group(1))
    unit = match.group(2)

    if unit == 'Y':
        return value

    elif unit == 'M':
        return value / 12

    return np.nan



countries = investpy.get_bond_countries()

all_data = []

for country in countries:

    print(f"\n===== {country} =====")

    try:

        country_bonds = investpy.get_bonds(country=country)

        country_bonds['maturity_years'] = (
            country_bonds['name']
            .apply(maturity_to_years)
        )

        country_bonds = country_bonds.dropna(
            subset=['maturity_years']
        )

        country_bonds = country_bonds[
            country_bonds['maturity_years'] < 3
        ]

    except Exception as e:

        print(f"Error obteniendo bonos de {country}: {e}")
        continue


    for index, row in country_bonds.iterrows():

        bond = row['name']

        print(f"Descargando {bond}")

        success = False
        retries = 5

        while not success and retries > 0:

            try:

                df = investpy.get_bond_historical_data(
                    bond=bond,
                    from_date='01/01/2011',
                    to_date=f'{today_str}'
                )

                df = df.reset_index()

                df['bond'] = bond
                df['country'] = country

                all_data.append(df)

                success = True

                # pausa aleatoria anti-bloqueo
                time.sleep(random.uniform(1, 3))

            except Exception as e:

                retries -= 1

                print(f"Error con {bond}: {e}")
                print(f"Reintentos restantes: {retries}")

                # esperar antes de reintentar
                time.sleep(random.uniform(5, 15))

        if not success:

            print(f"No se pudo descargar {bond}")
            continue



final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df.drop(['Open','High', 'Low'], axis = 1).rename(columns = {'Close' : 'Interest'})
final_df.to_csv(f'data_tmp/bonds_historical_data_{today}.csv', index=False)



