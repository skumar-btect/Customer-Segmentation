"""
PROJECT 2: Demand Forecasting & Inventory Optimisation
DATA CLEANING SCRIPT
Author: S. Kumar | Data Analyst
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("PROJECT 2: Demand Forecasting & Inventory Optimisation")
print("DATA CLEANING PIPELINE")
print("=" * 60)

# ── 1. LOAD RAW DATA ──────────────────────────────────────────
df = pd.read_csv('/home/claude/da-projects/project2-demand-forecasting/data/raw_sales_data.csv')
print(f"\n[LOAD] Raw shape: {df.shape}")

# ── 2. INITIAL QUALITY REPORT ─────────────────────────────────
print("\n[QUALITY REPORT - BEFORE CLEANING]")
print(f"  Total rows          : {len(df)}")
print(f"  Duplicate rows      : {df.duplicated().sum()}")
print(f"  Negative demand     : {(df['demand_units'] < 0).sum()}")
print(f"  Zero/null price     : {(df['unit_price'].isna() | (df['unit_price']<=0)).sum()}")
print(f"  Missing values      :\n{df.isnull().sum()[df.isnull().sum()>0]}")

# ── 3. PARSE DATES ────────────────────────────────────────────
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['week'] = df['date'].dt.isocalendar().week.astype(int)
df['quarter'] = df['date'].dt.quarter
print("\n[DATES] Extracted year, month, week, quarter")

# ── 4. FIX INVALID DEMAND ─────────────────────────────────────
bad_demand = df['demand_units'] < 0
df.loc[bad_demand, 'demand_units'] = np.nan
# Impute with median demand per product
df['demand_units'] = df.groupby('product_id')['demand_units'].transform(
    lambda x: x.fillna(x.median()))
df['demand_units'] = df['demand_units'].round().astype(int)
print(f"[DEMAND FIX] Replaced {bad_demand.sum()} invalid demand rows with product median")

# ── 5. FIX MISSING PRICES ─────────────────────────────────────
missing_price = df['unit_price'].isna() | (df['unit_price'] <= 0)
df.loc[missing_price, 'unit_price'] = np.nan
df['unit_price'] = df.groupby('product_id')['unit_price'].transform(
    lambda x: x.fillna(x.median()))
print(f"[PRICE FIX] Imputed {missing_price.sum()} missing prices with product median")

# ── 6. RECALCULATE REVENUE ────────────────────────────────────
df['revenue'] = (df['demand_units'] * df['unit_price']).round(2)
print("[REVENUE] Recalculated revenue from cleaned demand × price")

# ── 7. FEATURE ENGINEERING ────────────────────────────────────
df['rolling_4w_demand'] = df.groupby('product_id')['demand_units'].transform(
    lambda x: x.rolling(4, min_periods=1).mean().round(1))
df['demand_vs_avg'] = ((df['demand_units'] - df['rolling_4w_demand']) /
                        df['rolling_4w_demand'].replace(0, 1)).round(3)
df['is_stockout_risk'] = ((df['stock_level'] < df['rolling_4w_demand']) &
                           (df['stock_level'] < 50)).astype(int)
df['promo_demand_lift'] = df['is_promotion'] * df['demand_units']

stockout_skus = df[df['is_stockout_risk']==1]['product_id'].nunique()
print(f"[FEATURES] Added rolling averages, demand variance, stockout risk")
print(f"[STOCKOUT] {stockout_skus} SKUs flagged with stockout risk")

# ── 8. FINAL QUALITY REPORT ───────────────────────────────────
print("\n[QUALITY REPORT - AFTER CLEANING]")
print(f"  Final shape         : {df.shape}")
print(f"  Null values         : {df.isnull().sum().sum()}")
print(f"  Date range          : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"  Unique SKUs         : {df['product_id'].nunique()}")
print(f"  Total revenue       : ₹{df['revenue'].sum():,.0f}")
print(f"  Categories          :\n{df['category'].value_counts()}")

# ── 9. SAVE CLEAN DATA ────────────────────────────────────────
df.to_csv('/home/claude/da-projects/project2-demand-forecasting/data/clean_sales_data.csv', index=False)
print(f"\n[SAVE] Clean data saved → ../data/clean_sales_data.csv")
print("=" * 60)
