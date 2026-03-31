import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# LOAD
print("Loading data...")
df = pd.read_csv('clean_orders.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

# FEATURE ENGINEERING
le = LabelEncoder()
df['category_enc']  = le.fit_transform(df['category'])
df['region_enc']    = le.fit_transform(df['region'])
df['segment_enc']   = le.fit_transform(df['customer_segment'])
df['payment_enc']   = le.fit_transform(df['payment_method'])
df['city_enc']      = le.fit_transform(df['city'])
df['day_enc']       = le.fit_transform(df['day_of_week'])

FEATURES = [
    'price', 'quantity', 'discount',
    'category_enc', 'region_enc', 'segment_enc',
    'payment_enc', 'month', 'quarter',
    'shipping_cost', 'delivery_days',
    'profit_margin_pct'
]

X = df[FEATURES].fillna(df[FEATURES].median())
y = df['revenue']

print(f"Dataset   : {len(X):,} rows")
print(f"Features  : {len(FEATURES)}")

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# TRAIN
print("\nTraining Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)

# CROSS VALIDATION
cv = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"5-fold CV R2: {cv.mean():.3f} (+/- {cv.std():.3f})")

# EVALUATE
y_pred = model.predict(X_test)
r2     = r2_score(y_test, y_pred)
mae    = mean_absolute_error(y_test, y_pred)

print(f"\n{'='*50}")
print(f"  R2 SCORE : {r2:.3f}")
print(f"  MAE      : Rs.{mae:,.0f}")
print(f"{'='*50}")

# CHART 1: Actual vs Predicted
plt.figure(figsize=(10, 6))
sample = min(2000, len(y_test))
idx    = np.random.choice(len(y_test), sample, replace=False)
plt.scatter(y_test.iloc[idx], y_pred[idx],
            alpha=0.3, color='#2E86AB', s=15)
max_val = max(y_test.max(), y_pred.max())
plt.plot([0, max_val], [0, max_val],
         'r--', linewidth=2, label='Perfect prediction')
plt.xlabel('Actual Revenue (Rs.)')
plt.ylabel('Predicted Revenue (Rs.)')
plt.title(f'Actual vs Predicted Revenue | R2 = {r2:.3f}',
          fontsize=13, fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('chart11_actual_vs_predicted.png', dpi=150)
plt.show()
print("Saved: chart11_actual_vs_predicted.png")

# CHART 2: Feature Importance
coef_df = pd.DataFrame({
    'Feature'    : FEATURES,
    'Coefficient': np.abs(model.coef_)
}).sort_values('Coefficient', ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(coef_df['Feature'], coef_df['Coefficient'],
         color='#3BB273', edgecolor='white')
plt.title('Feature Importance - Linear Regression',
          fontsize=13, fontweight='bold')
plt.xlabel('Absolute Coefficient')
plt.tight_layout()
plt.savefig('chart12_feature_importance.png', dpi=150)
plt.show()
print("Saved: chart12_feature_importance.png")

# REVENUE UPLIFT ANALYSIS
print("\n" + "="*60)
print("REVENUE UPLIFT OPPORTUNITY ANALYSIS")
print("="*60)

current = df['revenue'].sum()

# Opportunity 1: Reduce discount on high-rated products
opp1 = df[(df['discount'] > 0.20) & (df['rating'] >= 4)]
gain1 = (opp1['price'] * opp1['quantity'] * 0.05).sum()

# Opportunity 2: Convert returned orders
opp2       = df[df['is_returned'] == True]
gain2      = opp2['revenue'].sum() * 0.30

# Opportunity 3: Upsell to repeat customers
opp3       = df[df['is_repeat_customer'] == True]
gain3      = opp3['revenue'].mean() * opp3['customer_id'].nunique() * 0.10

total_gain = gain1 + gain2 + gain3

print(f"Current Revenue          : Rs.{current:,.0f}")
print(f"Opportunity 1 (Discount) : Rs.{gain1:,.0f}")
print(f"Opportunity 2 (Returns)  : Rs.{gain2:,.0f}")
print(f"Opportunity 3 (Upsell)   : Rs.{gain3:,.0f}")
print(f"Total Uplift Potential   : Rs.{total_gain:,.0f}")
print("="*60)

print(f"\nRegression complete!")
print(f"R2 Score : {r2:.3f}")
print(f"MAE      : Rs.{mae:,.0f}")