# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:01:58 2026

@author: ignacio.delatorre
"""

import logging

logging.basicConfig(level=logging.INFO)

from A_extract_01_bonds_historical_data import extract_bonds_historical_data
from A_extract_02_exchange_rate import extract_exchRate_historical_data
from A_extract_03_inflation_ine import extract_inflation_historical_data

from B_process_01_merge import merge_data
from B_process_02_rentabilityCalculation import real_rentability_calculation


def run_pipeline():

    # =========================
    # 1. EXTRACT
    # =========================

    logging.info("[EXTRACT] Starting bonds extraction")
    bonds = extract_bonds_historical_data()
    logging.info(f"[EXTRACT] Bonds done | shape={bonds.shape}")

    logging.info("[EXTRACT] Starting exchange rate extraction")
    exch_rate = extract_exchRate_historical_data()
    logging.info(f"[EXTRACT] Exchange rate done | shape={exch_rate.shape}")

    logging.info("[EXTRACT] Starting inflation extraction")
    inflation = extract_inflation_historical_data()
    logging.info(f"[EXTRACT] Inflation done | shape={inflation.shape}")

    # =========================
    # 2. PROCESS
    # =========================

    logging.info("[PROCESS] Starting merge")
    df = merge_data(
        exch_rate=exch_rate,
        inflation=inflation,
        bonds=bonds
    )
    logging.info(f"[PROCESS] Merge done | shape={df.shape}")

    logging.info("[PROCESS] Starting rentability calculation")
    df = real_rentability_calculation(df)
    logging.info(f"[PROCESS] Rentability done | shape={df.shape}")

    return df


def main():

    logging.info("========== PIPELINE START ==========")

    df = run_pipeline()

    logging.info("========== PIPELINE FINISHED ==========")
    logging.info(f"Final dataset shape: {df.shape}")


if __name__ == "__main__":
    main()