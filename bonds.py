import pandas as pd
import requests
import re
from datetime import date
today = date.today()
def clean_country(name):

    name = name.lower()

    # quitar patrones de maturities
    name = re.sub(r'\d+\s*(m|a|y|día|dias|day|month|year|s)$', '', name)

    # quitar conectores típicos
    name = re.sub(r'\s+a\s+', ' ', name)

    # limpiar espacios
    name = re.sub(r'\s+', ' ', name).strip()

    return name

url = "https://es.investing.com/rates-bonds/world-government-bonds?maturity_from=10&maturity_to=90"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    html = response.text

    tables = pd.read_html(
    html,
    decimal=",",
    thousands=".")

    valid_tables = []

    for df in tables:

        # Eliminar columnas completamente vacías
        df = df.dropna(axis=1, how='all')

        # Ignorar tablas vacías
        if df.empty:
            continue

        # Ignorar tablas que no tengan columna Nombre
        if "Nombre" not in df.columns:
            continue

        valid_tables.append(df)

    # Concatenar todas
    final_df = pd.concat(valid_tables, ignore_index=True)


final_df = final_df.sort_values(by = 'Rendimiento', ascending = False).reset_index(drop = True) 
final_df["Pais"] = final_df["Nombre"].apply(clean_country)

mapping = {
    "italiano 1 año": "italia",
    'español 1 año' : 'españa',
    'español 9 meses' : 'españa',
    'italiano 9 meses': 'italia',
    'alemán 1 año': 'alemania', 
    'español 6 meses': 'españa',
    'italiano 6 meses': 'italia', 
    'alemán 9 meses': 'alemania',
    'español 3 meses': 'españa', 
    'alemán 6 meses': 'alemania', 
    'italiano 3 meses': 'italia',
    'español 1 mes': 'españa', 
    'alemán 3 meses': 'alemania',
    'italiano 1 mes': 'italia'
}
final_df["Pais"] = final_df["Pais"].replace(mapping)

pais_a_fx = {
    "turquía": "TRY",
    "egipto": "EGP",
    "ucrania": "UAH",
    "kazakhstan": "KZT",
    "brasil": "BRL",
    "zambia": "ZMW",
    "rusia": "RUB",
    "uganda": "UGX",
    "botsuana": "BWP",
    "bangladés": "BDT",
    "sri lanka": "LKR",
    "kenia": "KES",
    "namibia": "NAD",
    "méxico": "MXN",
    "indonesia": "IDR",
    "cote d'ivoire": "XOF",
    "sudáfrica": "ZAR",
    "rumanía": "RON",
    "india": "INR",
    "filipinas": "PHP",
    "hungría": "HUF",
    "bahréin": "BHD",
    "chile": "CLP",
    "australia": "AUD",
    "grecia": "EUR",
    "greece": "EUR",
    "noruega": "NOK",
    "mauricio": "MUR",
    "serbia": "RSD",
    "reino unido": "GBP",
    "polonia": "PLN",
    "israel": "ILS",
    "ee.uu.": "USD",
    "u.s.": "USD",
    "república checa": "CZK",
    "vietnam": "VND",
    "corea del sur": "KRW",
    "nueva zelanda": "NZD",
    "malasia": "MYR",
    "bulgaria": "BGN",
    "eslovenia": "EUR",
    "canadá": "CAD",
    "francia": "EUR",
    "irlanda": "EUR",
    "italia": "EUR",
    "austria": "EUR",
    "portugal": "EUR",
    "malta": "EUR",
    "hong kong": "HKD",
    "españa": "EUR",
    "bélgica": "EUR",
    "alemania": "EUR",
    "holanda": "EUR",
    "países bajos": "EUR",
    "marruecos": "MAD",
    "dinamarca": "DKK",
    "suecia": "SEK",
    "croacia": "EUR",
    "singapur": "SGD",
    "singapore": "SGD",
    "china": "CNY",
    "japón": "JPY",
    "tailandia": "THB",
    "suiza": "CHF"
}
final_df["FX_code"] = final_df["Pais"].str.lower().map(pais_a_fx)



final_df.to_csv(f'bonds_{today}.csv', index=False)
