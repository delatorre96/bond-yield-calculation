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
final_df["country"] = final_df["Nombre"].apply(clean_country)

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
final_df["country"] = final_df["country"].replace(mapping)

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
final_df["FX_code"] = final_df["country"].str.lower().map(pais_a_fx)


tenor_map = {
    # Alemania
    "alemán a 3 meses": 3,
    "alemán a 6 meses": 6,
    "alemán a 9 meses": 9,
    "alemán a 1 año": 12,

    # Australia
    "Australia 1A": 12,

    # Austria
    "Austria 1A": 12,
    "Austria 3M": 3,
    "Austria 6M": 6,

    # Bélgica
    "Bélgica 3M": 3,
    "Bélgica 6M": 6,
    "Bélgica 9M": 9,

    # Bahréin
    "Bahréin 1A": 12,
    "Bahréin 3M": 3,
    "Bahréin 6M": 6,
    "Bahréin 9M": 9,

    # Bangladés
    "Bangladés 1A": 12,
    "Bangladés 3M": 3,
    "Bangladés 6M": 6,

    # Botsuana
    "Botsuana 6M": 6,

    # Brasil
    "Brasil 1A": 12,
    "Brasil 3M": 3,
    "Brasil 6M": 6,
    "Brasil 9M": 9,

    # Bulgaria
    "Bulgaria 1A": 12,

    # Canadá
    "Canadá 1A": 12,
    "Canadá 1M": 1,
    "Canadá 2M": 2,
    "Canadá 3M": 3,
    "Canadá 6M": 6,

    # Chile
    "Chile 1A": 12,

    # China
    "China 1A": 12,

    # Corea del Sur
    "Corea del Sur 1A": 12,

    # Costa de Marfil
    "Cote d'Ivoire 1Y": 12,
    "Cote d'Ivoire 3M": 3,
    "Cote d'Ivoire 6M": 6,

    # Croacia
    "Croacia 1A": 12,

    # Dinamarca
    "Dinamarca 3M": 3,
    "Dinamarca 6M": 6,

    # EE.UU.
    "EE.UU. 1A": 12,
    "EE.UU. 1M": 1,
    "EE.UU. 2M": 2,
    "EE.UU. 3M": 3,
    "EE.UU. 4M": 4,
    "EE.UU. 6M": 6,

    # Egipto
    "Egipto 1A": 12,
    "Egipto 3M": 3,
    "Egipto 6M": 6,
    "Egipto 9M": 9,
    "Egipto a 1 día": 1/30,

    # Eslovenia
    "Eslovenia 1A": 12,

    # España
    "español a 1 año": 12,
    "español a 1 mes": 1,
    "español a 3 meses": 3,
    "español a 6 meses": 6,
    "español a 9 meses": 9,

    # Filipinas
    "Filipinas 1A": 12,
    "Filipinas 1M": 1,
    "Filipinas 3M": 3,
    "Filipinas 6M": 6,

    # Francia
    "Francia 1A": 12,
    "Francia 1M": 1,
    "Francia 3M": 3,
    "Francia 6M": 6,
    "Francia 9M": 9,

    # Grecia
    "Grecia 1M": 1,
    "Grecia 3M": 3,
    "Grecia 6M": 6,
    "Greece 1Y": 12,

    # Holanda
    "Holanda 1M": 1,
    "Holanda 3M": 3,
    "Holanda 6M": 6,

    # Hong Kong
    "Hong Kong 1A": 12,
    "Hong Kong 1M": 1,
    "Hong Kong 1S": 0.25,
    "Hong Kong 3M": 3,
    "Hong Kong 6M": 6,
    "Hong Kong 9M": 9,

    # Hungría
    "Hungría 1A": 12,
    "Hungría 3M": 3,
    "Hungría 6M": 6,

    # India
    "India 1A": 12,
    "India 3M": 3,
    "India 6M": 6,

    # Indonesia
    "Indonesia 1A": 12,
    "Indonesia 1M": 1,
    "Indonesia 3M": 3,
    "Indonesia 6M": 6,

    # Irlanda
    "Irlanda 1A": 12,

    # Israel
    "Israel 1A": 12,
    "Israel 1M": 1,
    "Israel 3M": 3,
    "Israel 6M": 6,
    "Israel 9M": 9,

    # Italia
    "italiano a 1 año": 12,
    "italiano a 1 mes": 1,
    "italiano a 3 meses": 3,
    "italiano a 6 meses": 6,
    "italiano a 9 meses": 9,

    # Japón
    "Japón 1A": 12,
    "Japón 1M": 1,
    "Japón 3M": 3,
    "Japón 6M": 6,
    "Japón 9M": 9,

    # Kazakhstan
    "Kazakhstan 1Y": 12,
    "Kazakhstan 6M": 6,

    # Kenia
    "Kenia 1A": 12,

    # México
    "México 1A": 12,
    "México 1M": 1,
    "México 3M": 3,
    "México 6M": 6,
    "México 9M": 9,

    # Malasia
    "Malasia 1A": 12,
    "Malasia 3M": 3,
    "Malasia 3S": 0.75,
    "Malasia 7M": 7,

    # Malta
    "Malta 1A": 12,
    "Malta 1M": 1,
    "Malta 3M": 3,
    "Malta 6M": 6,

    # Marruecos
    "Marruecos 3M": 3,
    "Marruecos 6M": 6,

    # Mauricio
    "Mauricio 1A": 12,
    "Mauricio 4M": 4,
    "Mauricio 6M": 6,
    "Mauricio 8M": 8,

    # Namibia
    "Namibia 1A": 12,
    "Namibia 3M": 3,
    "Namibia 6M": 6,
    "Namibia 9M": 9,

    # Noruega
    "Noruega 1A": 12,
    "Noruega 6M": 6,
    "Noruega 9M": 9,

    # Nueva Zelanda
    "Nueva Zelanda 1A": 12,
    "Nueva Zelanda 1M": 1,
    "Nueva Zelanda 2M": 2,
    "Nueva Zelanda 3M": 3,
    "Nueva Zelanda 4M": 4,
    "Nueva Zelanda 5M": 5,
    "Nueva Zelanda 6M": 6,

    # Polonia
    "Polonia 1A": 12,
    "Polonia 1M": 1,
    "Polonia 2M": 2,
    "Polonia a 1 día": 1/30,

    # Portugal
    "Portugal 1A": 12,
    "Portugal 3M": 3,
    "Portugal 6M": 6,

    # Reino Unido
    "Reino Unido 1A": 12,
    "Reino Unido 1M": 1,
    "Reino Unido 3M": 3,
    "Reino Unido 6M": 6,

    # República Checa
    "República Checa 1A": 12,

    # Rumanía
    "Rumanía 1A": 12,
    "Rumanía 6M": 6,

    # Rusia
    "Rusia 1A": 12,
    "Rusia 1M": 1,
    "Rusia 2M": 2,
    "Rusia 3M": 3,
    "Rusia 6M": 6,

    # Serbia
    "Serbia 1A": 12,

    # Singapur
    "Singapur 1A": 12,
    "Singapur 1M": 1,
    "Singapur 3M": 3,
    "Singapur 6M": 6,
    "Singapur 9M": 9,

    # Sri Lanka
    "Sri Lanka 1A": 12,
    "Sri Lanka 3M": 3,
    "Sri Lanka 6M": 6,

    # Sudáfrica
    "Sudáfrica 3M": 3,

    # Suecia
    "Suecia 1M": 1,
    "Suecia 2M": 2,
    "Suecia 3M": 3,
    "Suecia 6M": 6,

    # Suiza
    "Suiza 1A": 12,
    "Suiza 1M": 1,
    "Suiza 1S": 0.25,
    "Suiza 2M": 2,
    "Suiza 3M": 3,
    "Suiza 6M": 6,
    "Suiza a 1 día": 1/30,

    # Tailandia
    "Tailandia 1A": 12,

    # Turquía
    "Turquía 3M": 3,
    "Turquía 6M": 6,
    "Turquía 9M": 9,

    # Ucrania
    "Ucrania 1A": 12,

    # Uganda
    "Uganda 1A": 12,
    "Uganda 3M": 3,
    "Uganda 6M": 6,

    # Vietnam
    "Vietnam 1A": 12,

    # Zambia
    "Zambia 1Y": 12,
    "Zambia 2Y": 24,
    "Zambia 6M": 6,
    "Zambia 9M": 9,
}

final_df["tenor_months"] = final_df["Nombre"].map(tenor_map)


final_df.to_csv(f'data_tmp/bonds_{today}.csv', index=False)
