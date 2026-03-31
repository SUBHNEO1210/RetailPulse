import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# LOAD
print("Loading clean dataset...")
df = pd.read_csv('clean_orders.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

print(f"Total orders        : {len(df):,}")
print(f"Total revenue       : Rs.{df['revenue'].sum():,.0f}")
print(f"Total profit        : Rs.{df['profit'].sum():,.0f}")
print(f"Unique customers    : {df['customer_id'].nunique():,}")
print(f"Categories          : {df['category'].nunique()}")
print(f"Cities              : {df['city'].nunique()}")
print(f"Date range          : {df['order_date'].min().date()} to {df['order_date'].max().date()}")

# Style
plt.rcParams.update({
    'figure.facecolor' : 'white',
    'axes.facecolor'   : '#F8F9FA',
    'axes.grid'        : True,
    'grid.alpha'       : 0.3,
    'font.family'      : 'sans-serif',
    'font.size'        : 11,
})
COLORS = ['#2E86AB','#E84855','#3BB273','#F4A261',
          '#9B5DE5','#F15BB5','#00BBF9','#FEE440']

# ── CHART 1: Revenue by Category ─────────────────────────────
print("\nGenerating Chart 1: Revenue by Category...")
cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].barh(cat_rev.index, cat_rev.values/1e6,
             color=COLORS[:len(cat_rev)], edgecolor='white')
for i, val in enumerate(cat_rev.values):
    axes[0].text(val/1e6 + 0.1, i,
                 f'Rs.{val/1e6:.1f}M', va='center', fontsize=9)
axes[0].set_title('Revenue by Category', fontweight='bold')
axes[0].set_xlabel('Revenue (Millions Rs.)')

cat_profit = df.groupby('category')['profit'].sum().sort_values(ascending=True)
axes[1].barh(cat_profit.index, cat_profit.values/1e6,
             color=COLORS[:len(cat_profit)], edgecolor='white', alpha=0.8)
axes[1].set_title('Profit by Category', fontweight='bold')
axes[1].set_xlabel('Profit (Millions Rs.)')

plt.suptitle('Category Performance Analysis',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart1_revenue_by_category.png', dpi=150)
plt.show()
print("Saved: chart1_revenue_by_category.png")

# ── CHART 2: Monthly Revenue Trend ───────────────────────────
print("Generating Chart 2: Monthly Revenue Trend...")
monthly = df.groupby(['year','month']).agg(
    revenue = ('revenue','sum'),
    orders  = ('order_id','count'),
    profit  = ('profit','sum')
).reset_index()
monthly['period'] = (monthly['year'].astype(str) + '-' +
                     monthly['month'].astype(str).str.zfill(2))
monthly = monthly.sort_values('period')
monthly['growth'] = monthly['revenue'].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(16, 6))
ax2 = ax1.twinx()

ax1.fill_between(range(len(monthly)),
                  monthly['revenue']/1e6, alpha=0.2, color='#2E86AB')
ax1.plot(range(len(monthly)), monthly['revenue']/1e6,
         color='#2E86AB', linewidth=2.5, marker='o', markersize=5,
         label='Revenue')
ax1.plot(range(len(monthly)), monthly['profit']/1e6,
         color='#3BB273', linewidth=2, marker='s', markersize=4,
         label='Profit', linestyle='--')
ax2.bar(range(len(monthly)), monthly['growth'],
        alpha=0.3, color='#F4A261', label='Growth %')

ax1.set_xticks(range(len(monthly)))
ax1.set_xticklabels(monthly['period'], rotation=45, ha='right')
ax1.set_ylabel('Revenue / Profit (Millions Rs.)', color='#2E86AB')
ax2.set_ylabel('MoM Growth %', color='#F4A261')
ax1.set_title('Monthly Revenue & Profit Trend with Growth Rate',
              fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
plt.tight_layout()
plt.savefig('chart2_monthly_trend.png', dpi=150)
plt.show()
print("Saved: chart2_monthly_trend.png")

# ── CHART 3: Pareto Analysis ──────────────────────────────────
print("Generating Chart 3: Pareto Analysis...")
product_rev     = df.groupby('product_name')['revenue'].sum()\
                    .sort_values(ascending=False)
product_rev_pct = product_rev / product_rev.sum() * 100
cumulative_pct  = product_rev_pct.cumsum()
total_products  = len(product_rev)
top_10_idx      = int(total_products * 0.10)
top_10_rev      = product_rev_pct.iloc[:top_10_idx].sum()

print(f"Pareto: Top 10% SKUs = {top_10_rev:.1f}% of revenue")

fig, ax1 = plt.subplots(figsize=(14, 7))
ax2 = ax1.twinx()

x = range(len(product_rev))
ax1.bar(x, product_rev_pct.values,
        color='#2E86AB', alpha=0.7, label='Revenue %')
ax2.plot(x, cumulative_pct.values,
         color='#E84855', linewidth=2.5, label='Cumulative %')
ax2.axhline(y=80, color='gray', linestyle='--', alpha=0.5, label='80% line')
ax1.axvline(x=top_10_idx, color='orange',
            linestyle='--', alpha=0.7, label=f'Top 10% ({top_10_idx} SKUs)')

ax2.text(top_10_idx + 1, top_10_rev + 2,
         f'{top_10_rev:.0f}%', color='orange',
         fontsize=12, fontweight='bold')

ax1.set_ylabel('Individual Revenue %', color='#2E86AB')
ax2.set_ylabel('Cumulative Revenue %', color='#E84855')
ax1.set_xlabel('Products (ranked by revenue)')
ax1.set_title(
    f'Pareto Analysis: Top 10% SKUs ({top_10_idx} products) '
    f'generate {top_10_rev:.0f}% of revenue',
    fontsize=13, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='center right')
plt.tight_layout()
plt.savefig('chart3_pareto_analysis.png', dpi=150)
plt.show()
print("Saved: chart3_pareto_analysis.png")

# ── CHART 4: Customer Segment Analysis ───────────────────────
print("Generating Chart 4: Customer Segments...")
seg = df.groupby('customer_segment').agg(
    revenue   = ('revenue','sum'),
    orders    = ('order_id','count'),
    avg_val   = ('revenue','mean'),
    avg_clv   = ('clv','mean'),
    avg_rating= ('rating','mean')
).reset_index().sort_values('revenue', ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].bar(seg['customer_segment'], seg['revenue']/1e6,
            color=COLORS[:4], edgecolor='white')
axes[0].set_title('Revenue by Segment', fontweight='bold')
axes[0].set_ylabel('Revenue (Millions Rs.)')
for i, val in enumerate(seg['revenue']):
    axes[0].text(i, val/1e6 + 0.1,
                 f'Rs.{val/1e6:.1f}M', ha='center', fontsize=9)

axes[1].bar(seg['customer_segment'], seg['avg_val'],
            color=COLORS[:4], edgecolor='white')
axes[1].set_title('Avg Order Value by Segment', fontweight='bold')
axes[1].set_ylabel('Avg Order Value (Rs.)')

axes[2].bar(seg['customer_segment'], seg['avg_clv'],
            color=COLORS[:4], edgecolor='white')
axes[2].set_title('Avg CLV by Segment', fontweight='bold')
axes[2].set_ylabel('Customer Lifetime Value (Rs.)')

for ax in axes:
    ax.tick_params(axis='x', rotation=15)

plt.suptitle('Customer Segment Deep Dive',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart4_customer_segments.png', dpi=150)
plt.show()
print("Saved: chart4_customer_segments.png")

# ── CHART 5: Regional Analysis ────────────────────────────────
print("Generating Chart 5: Regional Analysis...")
region = df.groupby('region').agg(
    revenue = ('revenue','sum'),
    orders  = ('order_id','count'),
    profit  = ('profit','sum'),
    avg_val = ('revenue','mean')
).reset_index().sort_values('revenue', ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].bar(region['region'], region['revenue']/1e6,
            color=COLORS[:5], edgecolor='white')
axes[0].set_title('Revenue by Region', fontweight='bold')
axes[0].set_ylabel('Revenue (Millions Rs.)')
for i, val in enumerate(region['revenue']):
    axes[0].text(i, val/1e6 + 0.1,
                 f'Rs.{val/1e6:.1f}M', ha='center', fontsize=9)

axes[1].bar(region['region'], region['profit']/1e6,
            color=COLORS[:5], edgecolor='white', alpha=0.8)
axes[1].set_title('Profit by Region', fontweight='bold')
axes[1].set_ylabel('Profit (Millions Rs.)')

axes[2].pie(region['orders'], labels=region['region'],
            autopct='%1.1f%%', colors=COLORS[:5], startangle=90)
axes[2].set_title('Order Share by Region', fontweight='bold')

plt.suptitle('Regional Performance Analysis',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart5_regional_analysis.png', dpi=150)
plt.show()
print("Saved: chart5_regional_analysis.png")

# ── CHART 6: Top 15 Products ──────────────────────────────────
print("Generating Chart 6: Top Products...")
top_prod = df.groupby('product_name').agg(
    revenue = ('revenue','sum'),
    orders  = ('order_id','count'),
    profit  = ('profit','sum')
).sort_values('revenue', ascending=True).tail(15)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

axes[0].barh(top_prod.index, top_prod['revenue']/1e3,
             color='#2E86AB', edgecolor='white')
axes[0].set_title('Top 15 Products by Revenue',
                  fontweight='bold')
axes[0].set_xlabel('Revenue (Thousands Rs.)')

axes[1].barh(top_prod.index, top_prod['profit']/1e3,
             color='#3BB273', edgecolor='white')
axes[1].set_title('Top 15 Products by Profit',
                  fontweight='bold')
axes[1].set_xlabel('Profit (Thousands Rs.)')

plt.suptitle('Product Performance Analysis',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart6_top_products.png', dpi=150)
plt.show()
print("Saved: chart6_top_products.png")

# ── CHART 7: Discount Impact Analysis ────────────────────────
print("Generating Chart 7: Discount Analysis...")
disc = df.groupby('discount_band', observed=True).agg(
    avg_revenue = ('revenue','mean'),
    total_orders= ('order_id','count'),
    avg_profit  = ('profit','mean'),
    return_rate = ('is_returned','mean')
).reset_index()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].bar(disc['discount_band'], disc['avg_revenue'],
              color='#2E86AB', edgecolor='white')
axes[0,0].set_title('Avg Revenue by Discount Band',
                     fontweight='bold')
axes[0,0].set_ylabel('Avg Revenue (Rs.)')

axes[0,1].bar(disc['discount_band'], disc['total_orders'],
              color='#3BB273', edgecolor='white')
axes[0,1].set_title('Total Orders by Discount Band',
                     fontweight='bold')
axes[0,1].set_ylabel('Number of Orders')

axes[1,0].bar(disc['discount_band'], disc['avg_profit'],
              color='#F4A261', edgecolor='white')
axes[1,0].set_title('Avg Profit by Discount Band',
                     fontweight='bold')
axes[1,0].set_ylabel('Avg Profit (Rs.)')

axes[1,1].bar(disc['discount_band'],
              disc['return_rate']*100,
              color='#E84855', edgecolor='white')
axes[1,1].set_title('Return Rate by Discount Band',
                     fontweight='bold')
axes[1,1].set_ylabel('Return Rate (%)')

plt.suptitle('Discount Impact Analysis',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart7_discount_analysis.png', dpi=150)
plt.show()
print("Saved: chart7_discount_analysis.png")

# ── CHART 8: City-wise Top 10 Revenue ────────────────────────
print("Generating Chart 8: City Analysis...")
city_rev = df.groupby(['city','region'])['revenue'].sum()\
             .sort_values(ascending=True).tail(10)

fig, ax = plt.subplots(figsize=(12, 7))
colors_city = [COLORS[REGIONS.index(r) % len(COLORS)]
               if (REGIONS := ['North','South','East','West','Central'])
               else '#2E86AB'
               for c, r in city_rev.index]
ax.barh([f"{c} ({r})" for c, r in city_rev.index],
        city_rev.values/1e6,
        color='#2E86AB', edgecolor='white')
ax.set_title('Top 10 Cities by Revenue',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Revenue (Millions Rs.)')
plt.tight_layout()
plt.savefig('chart8_city_analysis.png', dpi=150)
plt.show()
print("Saved: chart8_city_analysis.png")

# ── CHART 9: Payment Method Analysis ─────────────────────────
print("Generating Chart 9: Payment Methods...")
pay = df.groupby('payment_method').agg(
    revenue     = ('revenue','sum'),
    orders      = ('order_id','count'),
    avg_val     = ('revenue','mean')
).reset_index().sort_values('revenue', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].bar(pay['payment_method'], pay['revenue']/1e6,
            color=COLORS[:len(pay)], edgecolor='white')
axes[0].set_title('Revenue by Payment Method',
                   fontweight='bold')
axes[0].set_ylabel('Revenue (Millions Rs.)')
axes[0].tick_params(axis='x', rotation=15)

axes[1].pie(pay['orders'], labels=pay['payment_method'],
            autopct='%1.1f%%',
            colors=COLORS[:len(pay)], startangle=90)
axes[1].set_title('Order Share by Payment Method',
                   fontweight='bold')

plt.suptitle('Payment Method Analysis',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart9_payment_analysis.png', dpi=150)
plt.show()
print("Saved: chart9_payment_analysis.png")

# ── CHART 10: Return Analysis ─────────────────────────────────
print("Generating Chart 10: Return Analysis...")
return_by_cat = df.groupby('category').agg(
    return_rate = ('is_returned','mean'),
    total       = ('order_id','count'),
    returned    = ('is_returned','sum')
).reset_index()
return_by_cat['return_rate'] *= 100
return_by_cat = return_by_cat.sort_values('return_rate',
                                           ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].barh(return_by_cat['category'],
             return_by_cat['return_rate'],
             color='#E84855', edgecolor='white')
axes[0].set_title('Return Rate by Category (%)',
                   fontweight='bold')
axes[0].set_xlabel('Return Rate (%)')

reason_counts = df['return_reason'].dropna().value_counts()
axes[1].bar(reason_counts.index, reason_counts.values,
            color=COLORS[:len(reason_counts)],
            edgecolor='white')
axes[1].set_title('Return Reasons Distribution',
                   fontweight='bold')
axes[1].set_ylabel('Number of Returns')
axes[1].tick_params(axis='x', rotation=20)

plt.suptitle('Return Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('chart10_return_analysis.png', dpi=150)
plt.show()
print("Saved: chart10_return_analysis.png")

# ── PRINT KEY INSIGHTS ────────────────────────────────────────
print("\n" + "="*60)
print("KEY BUSINESS INSIGHTS")
print("="*60)
print(f"1. Total Revenue      : Rs.{df['revenue'].sum():,.0f}")
print(f"2. Total Profit       : Rs.{df['profit'].sum():,.0f}")
print(f"3. Total Orders       : {len(df):,}")
print(f"4. Avg Order Value    : Rs.{df['revenue'].mean():,.0f}")
print(f"5. Unique Customers   : {df['customer_id'].nunique():,}")
print(f"6. Top Category       : {df.groupby('category')['revenue'].sum().idxmax()}")
print(f"7. Top Region         : {df.groupby('region')['revenue'].sum().idxmax()}")
print(f"8. Top City           : {df.groupby('city')['revenue'].sum().idxmax()}")
print(f"9. Return Rate        : {df['is_returned'].mean()*100:.1f}%")
print(f"10. Repeat Customer % : {df['is_repeat_customer'].mean()*100:.1f}%")
print(f"11. Top Payment Method: {df.groupby('payment_method')['revenue'].sum().idxmax()}")
print(f"12. Pareto Insight    : Top 10% SKUs = {top_10_rev:.0f}% revenue")
print("="*60)