# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:20:24 2026

@author: ignacio.delatorre
"""
import urllib.request, json
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import date
today = date.today()
import warnings
warnings.filterwarnings("ignore", message="Could not infer format*")

country_map = {
    "turquía": "TUR",
    "egipto": "EGY",
    "ucrania": "UKR",
    "kazakhstan": "KAZ",
    "brasil": "BRA",
    "zambia": "ZMB",
    "rusia": "RUS",
    "uganda": "UGA",
    "botsuana": "BWA",
    "bangladés": "BGD",
    "sri lanka": "LKA",
    "kenia": "KEN",
    "namibia": "NAM",
    "méxico": "MEX",
    "indonesia": "IDN",
    "cote d'ivoire": "CIV",
    "sudáfrica": "ZAF",
    "rumanía": "ROU",
    "india": "IND",
    "filipinas": "PHL",
    "hungría": "HUN",
    "bahréin": "BHR",
    "chile": "CHL",
    "australia": "AUS",
    "grecia": "GRC",
    "greece": "GRC",
    "noruega": "NOR",
    "mauricio": "MUS",
    "serbia": "SRB",
    "reino unido": "GBR",
    "polonia": "POL",
    "israel": "ISR",
    "ee.uu.": "USA",
    "república checa": "CZE",
    "vietnam": "VNM",
    "corea del sur": "KOR",
    "nueva zelanda": "NZL",
    "malasia": "MYS",
    "bulgaria": "BGR",
    "eslovenia": "SVN",
    "canadá": "CAN",
    "francia": "FRA",
    "irlanda": "IRL",
    "italia": "ITA",
    "austria": "AUT",
    "portugal": "PRT",
    "malta": "MLT",
    "hong kong": "HKG",
    "españa": "ESP",
    "bélgica": "BEL",
    "alemania": "DEU",
    "holanda": "NLD",
    "países bajos": "NLD",
    "marruecos": "MAR",
    "dinamarca": "DNK",
    "suecia": "SWE",
    "croacia": "HRV",
    "singapur": "SGP",
    "singapore": "SGP",
    "china": "CHN",
    "japón": "JPN",
    "tailandia": "THA",
    "suiza": "CHE"
}

def get_imf_cpi(country, start="2010"):

    frequencies = ["M", "Q", "A"]

    key_templates = [
        "{country}.CPI.CP01.IX.{freq}",
        "{country}.PCPI_IX.PCPI_IX.{freq}",
        "{country}.CPI..IX.{freq}",
        "{country}..CP01.IX.{freq}",
        "{country}...IX.{freq}",
        "{country}.CPI.CP01..{freq}",
    ]

    for freq in frequencies:

        for template in key_templates:

            key = template.format(
                country=country,
                freq=freq
            )

            url = (
                "https://api.imf.org/external/sdmx/2.1/data/"
                f"IMF.STA,CPI/{key}"
                f"?startPeriod={start}"
                f"&dimensionAtObservation=TIME_PERIOD"
            )

            try:

                hdr = {
                    "Accept": "application/xml"
                }

                req = urllib.request.Request(
                    url,
                    headers=hdr
                )

                response = urllib.request.urlopen(req)

                xml_data = response.read()

                root = ET.fromstring(xml_data)

                valid_obs = []

                for obs in root.iter():

                    if obs.tag.endswith("Obs"):

                        value = obs.attrib.get("OBS_VALUE")

                        if value is not None:

                            try:

                                float(value)

                                valid_obs.append(value)

                            except:
                                pass

                if len(valid_obs) > 0:

                    print(
                        f"SUCCESS {country} -> {key}"
                    )

                    return {
                        "xml": xml_data,
                        "freq": freq,
                        "key": key
                    }

            except Exception as e:

                pass

    print(f"NO SERIES FOUND: {country}")

    return None



def parse_imf_xml(xml_data):

    root = ET.fromstring(xml_data)

    data = []

    for obs in root.iter():

        if obs.tag.endswith("Obs"):

            time = obs.attrib.get("TIME_PERIOD")
            value = obs.attrib.get("OBS_VALUE")

            if time and value:

                data.append([
                    time,
                    float(value)
                ])

    df = pd.DataFrame(
        data,
        columns=["date", "cpi"]
    )

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    return df



results = {}

for country_name, iso3 in country_map.items():

    result = get_imf_cpi(iso3)

    if result is not None:

        results[country_name] = result



dfs = []

for country_name, result in results.items():

    df = parse_imf_xml(result["xml"])

    freq = result["freq"]

    df["country"] = country_name
    df["freq"] = freq

    if freq == "Q":

        # index temporal
        df = df.set_index("date")

        # convertir a mensual
        df = df.resample("ME").ffill()

        # recuperar date
        df = df.reset_index()

        # marcar ya como mensual
        df["freq"] = "M"

    df["inflation_change"] = (
        df["cpi"].pct_change(1) 
    )

    # -----------------------------
    # INFLACIÓN YOY
    # -----------------------------

    df["inflation_yoy"] = (
        df["cpi"].pct_change(12)
    )

    dfs.append(df)

final_df = pd.concat(dfs).reset_index(drop=True).drop('freq', axis = 1)

final_df.to_csv(f'data_tmp/inflation_IMF_{today}.csv', index=False)
