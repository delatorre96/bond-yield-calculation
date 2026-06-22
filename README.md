# Real Bond Returns for Euro Investors

This project estimates the **real return obtained by a Euro-area investor purchasing sovereign bonds denominated in foreign currencies**.

The analysis combines:

- Sovereign bond yields obtained from Investing.com.
- Historical exchange rates from the European Central Bank (ECB).
- Euro-area inflation from the Spanish National Statistics Institute (INE).

The objective is to reconstruct the ex-post real return of each bond and identify the main drivers of profitability across countries and periods.

---

## Motivation

A high nominal bond yield does not necessarily imply a high real return for a Euro investor.

While investors often focus on bond yields, exchange-rate movements can dominate realized returns, especially in emerging markets. A bond paying a high interest rate may ultimately generate poor returns if the local currency depreciates significantly against the Euro.

This project quantifies the interaction between:

- Bond yields
- Exchange-rate dynamics
- Inflation

to understand what truly drives sovereign bond profitability from the perspective of a Euro investor.

---

## Methodology

For a bond issued at time \(t\) and maturing at time \(t+k\), the real return is calculated as:

```math
r_{real}
=
\frac{X_{t+k}^{real}}{X_t}
-1
=
\frac{
S_t (1+i)
}{
S_{t+k}
\left(1+\pi^{EUR}_{t,t+k}\right)
}
-1
```

where:

| Variable | Description |
|-----------|------------|
| \(i\) | Bond interest rate |
| \(S_t\) | Exchange rate at bond issuance |
| \(S_{t+k}\) | Exchange rate at maturity |
| \(\pi^{EUR}_{t,t+k}\) | Accumulated Euro-area inflation between issuance and maturity |
| \(r_{real}\) | Real return for a Euro investor |

The framework decomposes profitability into three components:

1. Bond yield.
2. Exchange-rate dynamics.
3. Inflation erosion.

---

## Data Sources

### Sovereign Bond Yields

Obtained from Investing.com using the `investpy` package.

Script:

```text
A_extract_01_bonds_historical_data.py
```

---

### Exchange Rates

Historical ECB exchange-rate reference data.

Source:

https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip

Script:

```text
A_extract_02_exchange_rate.py
```

---

### Inflation

Euro-area CPI series obtained from the Spanish National Statistics Institute (INE).

Source:

https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/{TABLE_ID}?tip=AM

Script:

```text
A_extract_03_inflation_ine.py
```

---

## Data Processing

### Merge Stage

Script:

```text
B_process_01_merge.py
```

This stage:

- Converts ECB exchange-rate data into long format.
- Maps currencies to countries.
- Constructs exchange-rate series for Euro-area countries.
- Converts monthly CPI observations into daily observations using forward filling.
- Computes bond maturity dates from bond tenors.
- Retrieves exchange rates and inflation values at:
  - issuance date
  - maturity date
- Calculates accumulated inflation:

```math
\pi^{EUR}_{t,t+k}
=
\frac{IPC_{t+k}}
{IPC_t}
-1
```

---

### Real Return Calculation

Script:

```text
B_process_02_rentabilityCalculation.py
```

Computes:

```math
r_{real}
=
\frac{
S_t (1+i)
}{
S_{t+k}
(1+\pi^{EUR}_{t,t+k})
}
-1
```

for every bond observation.

---

## Machine Learning Analysis

Script:

```text
C_analysis_01_gradient_boosting.py
```

A Gradient Boosting model is trained to identify the variables most strongly associated with high real returns.

The analysis includes:

- Feature importance analysis
- SHAP values
- Partial Dependence Plots (PDPs)

The objective is not prediction itself, but interpretation of the drivers of bond profitability.

---

## Indonesia Case Study

The notebook:

```text
Indonesia.ipynb
```

contains an exploratory analysis focused on Indonesian sovereign bonds.

Preliminary findings suggest that the exceptionally high real returns observed in several Indonesian bond vintages are largely explained by exchange-rate dynamics between the Euro and the Indonesian Rupiah.

In particular, abrupt exchange-rate adjustments appear to contribute more to realized profitability than nominal bond yields alone.

---

## Pipeline

The project follows a simple ETL workflow:

```text
Extract
│
├── Bond yields
├── Exchange rates
└── Inflation

        ↓

Process
│
├── Merge datasets
└── Compute real returns

        ↓

Analysis
│
├── Gradient Boosting
├── SHAP
├── PDP
└── Visualizations
```

The full pipeline can be executed through:

```bash
python Main.py
```

---

## Repository Structure

```text
.
├── Main.py
│
├── A_extract_01_bonds_historical_data.py
├── A_extract_02_exchange_rate.py
├── A_extract_03_inflation_ine.py
│
├── B_process_01_merge.py
├── B_process_02_rentabilityCalculation.py
│
├── C_analysis_01_gradient_boosting.py
│
├── Indonesia.ipynb
│
├── data_tmp/
├── viz/
└── requirements.txt
```

---

## Installation

Create a Python environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python Main.py
```

---

## Future Work

Potential extensions include:

- Additional inflation sources (FRED, IMF, World Bank).
- Currency-hedged return calculations.
- Cross-country comparison of exchange-rate risk premia.
- Explainable machine-learning analysis across all sovereign issuers.
- Integration with macroeconomic indicators and sovereign risk measures.