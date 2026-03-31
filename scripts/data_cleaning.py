import pandas as pd
import numpy as np
from datetime import datetime

LOG_FILE = 'cleaning_log.txt'

def log(msg):
    ts   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

# LOAD
log("Loading raw dataset...")
df = pd.read_csv('raw_orders.csv')
original = len(df)
log(f"Raw rows: {original}")
issues = {}

# Step 1: Remove duplicates
before = len(df)
df = df.drop_duplicates(subset=['order_id'], keep='first')
issues['duplicates_removed'] = before - len(df)
log(f"Duplicates removed: {issues['duplicates_removed']}")

# Step 2: Drop missing order dates
before = len(df)
df = df.dropna(subset=['order_date'])
issues['missing_dates_dropped'] = before - len(df)
log(f"Missing dates dropped: {issues['missing_dates_dropped']}")

# Step 3: Fix negative quantities
neg = df['quantity'] <= 0
issues['negative_qty_fixed'] = int(neg.sum())
df.loc[neg, 'quantity'] = 1
log(f"Negative quantities fixed: {issues['negative_qty_fixed']}")

# Step 4: Fix outlier prices
Q1  = df['price'].quantile(0.25)
Q3  = df['price'].quantile(0.75)
IQR = Q3 - Q1
mask = df['price'] > Q3 + 3 * IQR
issues['price_outliers_fixed'] = int(mask.sum())
df.loc[mask, 'price'] = df.groupby('category')['price'].transform('median')[mask]
log(f"Price outliers fixed: {issues['price_outliers_fixed']}")

# Step 5: Fill missing revenues
issues['null_revenue_filled'] = int(df['revenue'].isna().sum())
df['revenue'] = df['revenue'].fillna(
    df['price'] * df['quantity'] * (1 - df['discount']))
df['revenue'] = df['revenue'].round(2)
log(f"Null revenues filled: {issues['null_revenue_filled']}")

# Step 6: Fill missing segments
issues['null_segment_filled'] = int(df['customer_segment'].isna().sum())
df['customer_segment'] = df['customer_segment'].fillna('Regular')
log(f"Null segments filled: {issues['null_segment_filled']}")

# Step 7: Fill missing cities
issues['null_city_filled'] = int(df['city'].isna().sum())
df['city'] = df['city'].fillna('Unknown')
log(f"Null cities filled: {issues['null_city_filled']}")

# Step 8: Fill missing ratings
issues['null_rating_filled'] = int(df['rating'].isna().sum())
df['rating'] = df['rating'].fillna(df['rating'].median())
log(f"Null ratings filled: {issues['null_rating_filled']}")

# Step 9: Recalculate profit
df['profit'] = (df['revenue'] * df['profit_margin_pct']).round(2)

# Step 10: Date features
df['order_date']    = pd.to_datetime(df['order_date'])
df['delivery_date'] = pd.to_datetime(df['delivery_date'])
df['month']         = df['order_date'].dt.month
df['year']          = df['order_date'].dt.year
df['month_name']    = df['order_date'].dt.strftime('%b')
df['quarter']       = df['order_date'].dt.quarter
df['day_of_week']   = df['order_date'].dt.day_name()
df['week_number']   = df['order_date'].dt.isocalendar().week.astype(int)

# Step 11: Customer Lifetime Value
clv  = df.groupby('customer_id')['revenue'].sum().reset_index()
clv.columns = ['customer_id', 'clv']
df   = df.merge(clv, on='customer_id', how='left')
log("CLV calculated")

# Step 12: Order frequency
freq = df.groupby('customer_id')['order_id'].count().reset_index()
freq.columns = ['customer_id', 'order_frequency']
df   = df.merge(freq, on='customer_id', how='left')
log("Order frequency calculated")

# Step 13: Net revenue (after returns)
df['net_revenue'] = df.apply(
    lambda r: 0 if r['is_returned'] else r['revenue'], axis=1)

# Step 14: Discount band
df['discount_band'] = pd.cut(df['discount'],
    bins=[-0.01, 0.05, 0.10, 0.20, 0.30, 1.0],
    labels=['0-5%','5-10%','10-20%','20-30%','30%+'])

# FINAL
accuracy = round(len(df) / original * 100, 1)
log(f"Final rows: {len(df)}")
log(f"Columns: {len(df.columns)}")
log(f"Data accuracy: {accuracy}%")
log(f"Issues fixed: {issues}")
log(f"Total Revenue: Rs.{df['revenue'].sum():,.0f}")
log(f"Total Profit : Rs.{df['profit'].sum():,.0f}")
log(f"Total Orders : {len(df):,}")
log(f"Unique Customers: {df['customer_id'].nunique():,}")
log(f"Date Range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")

# Save
df.to_csv('clean_orders.csv', index=False)
df.to_excel('clean_orders.xlsx', index=False)
log("Saved: clean_orders.csv and clean_orders.xlsx")

print(f"\nDataset columns ({len(df.columns)}):")
print(list(df.columns))
print(f"\nBasic stats:")
print(df[['price','quantity','discount','revenue','profit']].describe().round(2))