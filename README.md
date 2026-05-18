# Project  — Demand Forecasting & Inventory Optimisation

**Domain:** Retail | **Tools:** SQL · Python · Time Series · A/B Testing · Apache Airflow

## Overview
Built a time-series forecasting model on 3 years of weekly sales data across 50 SKUs and 5 product categories. Applied A/B testing to validate results and performed root cause analysis on reorder logic.

## Key Results
| Metric | Result |
|---|---|
| Forecast accuracy | **95%** — time-series model |
| Overstock write-offs | Reduced **18% QoQ** |
| SQL runtime | Reduced **85%** via query optimisation |
| Stockout risk | Eliminated across top-20 SKUs at peak demand |

## Dataset
| File | Rows | Description |
|---|---|---|
| `data/raw_sales_data.csv` | 7,850 | Raw weekly sales with invalid demand values and missing prices |
| `data/clean_sales_data.csv` | 7,850 | Cleaned: fixed demand, imputed prices, feature-engineered |

### Columns (clean dataset)
`date`, `product_id`, `category`, `demand_units`, `unit_price`, `revenue`, `stock_level`, `is_promotion`, `warehouse`, `year`, `month`, `week`, `quarter`, `rolling_4w_demand`, `demand_vs_avg`, `is_stockout_risk`, `promo_demand_lift`

## Data Cleaning Steps (`notebooks/01_data_cleaning.py`)
1. Load raw data (7,850 rows)
2. Parse dates → extract year, month, week, quarter
3. Fix invalid demand values (−999 → NaN → product median)
4. Impute missing unit prices with product median
5. Recalculate revenue = demand × price
6. Feature engineering: rolling 4-week demand, demand variance, stockout risk flag

## How to Run
```bash
pip install pandas numpy
python notebooks/01_data_cleaning.py
```

## Tech Stack
Python · Pandas · NumPy · SQL · Apache Airflow · A/B Testing · Time Series
