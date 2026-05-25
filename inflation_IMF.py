# -*- coding: utf-8 -*-
"""
Created on Mon May 25 12:15:17 2026

@author: ignacio.delatorre
"""
########### Python 3.2 #############
import urllib.request, json
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import date
today = date.today()

def get_imf_cpi(country, start="2010"):

    url = (
        "https://api.imf.org/external/sdmx/2.1/data/"
        f"IMF.STA,CPI/{country}.CPI.CP01.IX.M"
        f"?startPeriod={start}&dimensionAtObservation=TIME_PERIOD"
    )

    hdr = {
        "Accept": "application/xml",
        "Cache-Control": "no-cache",
    }

    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)

    xml_data = response.read()
    return xml_data


def parse_imf_cpi(xml_data):

    root = ET.fromstring(xml_data)

    data = []

    # buscar TODOS los Obs sin namespace
    for obs in root.iter():

        if obs.tag.endswith("Obs"):

            time = obs.attrib.get("TIME_PERIOD")
            value = obs.attrib.get("OBS_VALUE")

            if time and value:
                data.append([time, float(value)])

    df = pd.DataFrame(data, columns=["date", "cpi"])

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date").reset_index(drop=True)

    return df

def get_country_cpi(country_name, start="2010"):

    if country_name not in country_map:
        print(f"NO MAPEO: {country_name}")
        return None

    code = country_map[country_name]

    try:
        xml = get_imf_cpi(code, start=start)
        df = parse_imf_cpi(xml)
        df["country"] = country_name

        df["inflation_mom"] = df["cpi"].pct_change(1) * 100
        df["inflation_yoy"] = df["cpi"].pct_change(12) * 100

        return df

    except Exception as e:
        print(country_name, e)
        return None
country_map = {
    'turquía': 'TUR',
    'egipto': 'EGY',
    'ucrania': 'UKR',
    'kazakhstan': 'KAZ',
    'brasil': 'BRA',
    'zambia': 'ZMB',
    'rusia': 'RUS',
    'uganda': 'UGA',
    'botsuana': 'BWA',
    'bangladés': 'BGD',
    'sri lanka': 'LKA',
    'kenia': 'KEN',
    'namibia': 'NAM',
    'méxico': 'MEX',
    'indonesia': 'IDN',
    "cote d'ivoire": 'CIV',
    'sudáfrica': 'ZAF',
    'rumanía': 'ROU',
    'india': 'IND',
    'filipinas': 'PHL',
    'hungría': 'HUN',
    'bahréin': 'BHR',
    'chile': 'CHL',
    'australia': 'AUS',
    'grecia': 'GRC',
    'greece': 'GRC',
    'noruega': 'NOR',
    'mauricio': 'MUS',
    'serbia': 'SRB',
    'reino unido': 'GBR',
    'polonia': 'POL',
    'israel': 'ISR',
    'ee.uu.': 'USA',
    'u.s.': 'USA',
    'república checa': 'CZE',
    'vietnam': 'VNM',
    'corea del sur': 'KOR',
    'nueva zelanda': 'NZL',
    'malasia': 'MYS',
    'bulgaria': 'BGR',
    'eslovenia': 'SVN',
    'canadá': 'CAN',
    'francia': 'FRA',
    'irlanda': 'IRL',
    'italia': 'ITA',
    'austria': 'AUT',
    'portugal': 'PRT',
    'malta': 'MLT',
    'hong kong': 'HKG',
    'españa': 'ESP',
    'bélgica': 'BEL',
    'alemania': 'DEU',
    'holanda': 'NLD',
    'marruecos': 'MAR',
    'dinamarca': 'DNK',
    'suecia': 'SWE',
    'croacia': 'HRV',
    'singapur': 'SGP',
    'singapore': 'SGP',
    'china': 'CHN',
    'japón': 'JPN',
    'tailandia': 'THA',
    'suiza': 'CHE'
}


countries = [
'turquía', 'egipto', 'ucrania', 'kazakhstan', 'brasil', 'zambia',
'rusia', 'uganda', 'botsuana', 'bangladés', 'sri lanka', 'kenia',
'namibia', 'méxico', 'indonesia', "cote d'ivoire", 'sudáfrica',
'rumanía', 'india', 'filipinas', 'hungría', 'bahréin', 'chile',
'australia', 'grecia', 'noruega', 'mauricio', 'serbia',
'reino unido', 'polonia', 'israel', 'ee.uu.', 'u.s.',
'república checa', 'vietnam', 'corea del sur', 'nueva zelanda',
'malasia', 'bulgaria', 'eslovenia', 'canadá', 'francia', 'irlanda',
'italia', 'austria', 'portugal', 'malta', 'hong kong',
'españa', 'bélgica', 'alemania', 'holanda', 'marruecos',
'dinamarca', 'suecia', 'croacia', 'singapur', 'china',
'japón', 'tailandia', 'suiza'
]

all_data = []

for c in countries:
    df = get_country_cpi(c)
    if df is not None:
        all_data.append(df)
        
final_df = pd.concat(all_data)
final_df.to_csv(f'data_tmp/inflation_IMF_{today}.csv',index = False)




