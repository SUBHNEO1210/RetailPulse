import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker('en_IN')
random.seed(42)
np.random.seed(42)

# ── CONFIG ───────────────────────────────────────────────────
NUM_ORDERS = 60000  # increased to 60,000+

CATEGORIES = {
    'Electronics': {
        'products': [
            ('Smartphone X12',      12999, 0.15),
            ('Laptop Pro 15',       45999, 0.10),
            ('Wireless Earbuds',     2999, 0.25),
            ('Smart Watch Series 5', 8999, 0.18),
            ('Tablet 10inch',       18999, 0.12),
            ('USB-C Hub 7port',      1499, 0.30),
            ('Portable Charger 20K', 1999, 0.22),
            ('Bluetooth Speaker',    3499, 0.20),
            ('Gaming Mouse',         2499, 0.20),
            ('Mechanical Keyboard',  4999, 0.15),
            ('Webcam 4K',            3999, 0.18),
            ('Smart TV 43inch',     32999, 0.08),
        ],
        'weight': 25
    },
    'Clothing': {
        'products': [
            ('Men Formal Shirt',    1299, 0.20),
            ('Women Kurti Printed', 1499, 0.25),
            ('Slim Fit Jeans',      1999, 0.15),
            ('Sports T-Shirt DryFit', 799, 0.30),
            ('Winter Puffer Jacket', 3999, 0.10),
            ('Ethnic Anarkali Dress', 2499, 0.18),
            ('Kids School Uniform',   899, 0.22),
            ('Casual White Sneakers', 2299, 0.20),
            ('Formal Trousers',      1599, 0.18),
            ('Saree Silk Blend',     3499, 0.15),
            ('Men Polo T-Shirt',      899, 0.28),
            ('Women Blazer',         2999, 0.15),
        ],
        'weight': 20
    },
    'Home & Kitchen': {
        'products': [
            ('Air Fryer 4L Digital', 4999, 0.12),
            ('Mixer Grinder 750W',   3499, 0.15),
            ('Cotton Bedsheet Set',  1299, 0.20),
            ('Pressure Cooker 5L',   2199, 0.18),
            ('LED Bulb 9W Pack12',    499, 0.35),
            ('RO Water Purifier',    8999, 0.08),
            ('Engineered Bookshelf', 5999, 0.10),
            ('Bagless Vacuum',       6999, 0.12),
            ('Non-stick Cookware Set',3499, 0.15),
            ('Induction Cooktop',    2999, 0.18),
            ('Steel Dinner Set',     1999, 0.20),
            ('Curtains Blackout',    1499, 0.22),
        ],
        'weight': 18
    },
    'Beauty & Health': {
        'products': [
            ('Vitamin C Face Serum',  1299, 0.25),
            ('Pro Hair Dryer 2200W',  2499, 0.18),
            ('Whey Protein 1kg',      1999, 0.20),
            ('SPF50 Sunscreen 100ml',  699, 0.30),
            ('Sonic Toothbrush',      1999, 0.22),
            ('Vitamin D3+K2 Tablets',  599, 0.28),
            ('Salicylic Acid Wash',    399, 0.35),
            ('EDP Perfume 100ml',     2999, 0.15),
            ('Retinol Night Cream',   1499, 0.22),
            ('Jade Roller Gua Sha',    799, 0.30),
            ('Digital Thermometer',    699, 0.25),
            ('Pulse Oximeter',         999, 0.22),
        ],
        'weight': 17
    },
    'Sports & Fitness': {
        'products': [
            ('TPE Yoga Mat 6mm',      1299, 0.20),
            ('Adjustable Dumbbell',   3499, 0.15),
            ('Road Cycling Helmet',   2999, 0.18),
            ('Running Shoes Gel',     4999, 0.12),
            ('Resistance Band Set',    799, 0.30),
            ('SG Cricket Bat',        2499, 0.20),
            ('Nivia Football Size5',  1299, 0.25),
            ('Yonex Badminton Racket',1499, 0.22),
            ('Gym Gloves Pro',         699, 0.30),
            ('Skipping Rope Digital',  899, 0.28),
            ('Foam Roller 90cm',       999, 0.25),
            ('Pull Up Bar Doorway',   1799, 0.20),
        ],
        'weight': 12
    },
    'Books & Stationery': {
        'products': [
            ('Data Science Handbook',  799, 0.20),
            ('Python for Beginners',   699, 0.22),
            ('CAT 2025 Prep Guide',    599, 0.25),
            ('A4 Notebook 200pg Pack', 299, 0.40),
            ('Faber Castell Pen Set',  199, 0.45),
            ('2025 Weekly Planner',    499, 0.30),
            ('Watercolor Art Kit',     999, 0.20),
            ('Casio Scientific Calc', 1299, 0.18),
            ('UPSC GS Paper 1 Guide',  799, 0.22),
            ('English Grammar Book',   399, 0.30),
            ('Sticky Notes Bulk Pack', 249, 0.40),
            ('Sketch Book A3',         599, 0.25),
        ],
        'weight': 8
    },
    'Grocery & Food': {
        'products': [
            ('Organic Almonds 500g',   899, 0.10),
            ('Cold Press Olive Oil',  1299, 0.12),
            ('Green Tea 100 bags',     499, 0.20),
            ('Quinoa 1kg',             699, 0.15),
            ('Dark Chocolate 70%',     399, 0.18),
            ('Protein Granola 400g',   599, 0.15),
            ('Honey Raw Organic 500g', 799, 0.12),
            ('Oats Quick Cook 1kg',    299, 0.22),
        ],
        'weight': 6
    },
    'Toys & Baby': {
        'products': [
            ('LEGO Classic 500pcs',   2999, 0.12),
            ('Baby Monitor WiFi',     4999, 0.10),
            ('Wooden Puzzle Set',      799, 0.20),
            ('RC Car 4WD',            1999, 0.15),
            ('Baby Walker Foldable',  2499, 0.12),
            ('Art Easel Kids',        1299, 0.18),
            ('Soft Toy Elephant',      699, 0.25),
            ('Educational Tablet Kids',3499, 0.12),
        ],
        'weight': 5
    },
}

REGIONS        = ['North', 'South', 'East', 'West', 'Central']
REGION_WEIGHTS = [25, 22, 18, 20, 15]

SEGMENTS        = ['Regular', 'Premium', 'VIP', 'New']
SEGMENT_WEIGHTS = [45, 25, 10, 20]

PAYMENT_METHODS = ['UPI', 'Credit Card', 'Debit Card',
                   'Net Banking', 'COD', 'Wallet']
PAYMENT_WEIGHTS = [35, 22, 18, 10, 10, 5]

CITIES_BY_REGION = {
    'North'  : ['Delhi', 'Lucknow', 'Jaipur', 'Chandigarh', 'Agra'],
    'South'  : ['Bangalore', 'Chennai', 'Hyderabad', 'Kochi', 'Coimbatore'],
    'East'   : ['Kolkata', 'Bhubaneswar', 'Patna', 'Guwahati', 'Ranchi'],
    'West'   : ['Mumbai', 'Pune', 'Ahmedabad', 'Surat', 'Nagpur'],
    'Central': ['Bhopal', 'Indore', 'Raipur', 'Jabalpur', 'Gwalior'],
}

RETURN_REASONS = ['Defective product', 'Wrong item delivered',
                  'Size mismatch', 'Changed mind', 'Better price found',
                  None, None, None, None, None]  # 80% no return

# Flatten products
all_products = []
all_weights  = []
for cat, data in CATEGORIES.items():
    for prod in data['products']:
        all_products.append((cat, prod[0], prod[1], prod[2]))
        all_weights.append(data['weight'])
all_weights = [w/sum(all_weights) for w in all_weights]

# Generate customer pool
NUM_CUSTOMERS = 10000
customers = [f"CUST{str(i).zfill(5)}" for i in range(1, NUM_CUSTOMERS+1)]

# Customer segment assignment (consistent per customer)
customer_segments = {
    cust: random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    for cust in customers
}

print(f"Generating {NUM_ORDERS} orders...")
orders = []
start_date = date(2023, 1, 1)

for i in range(NUM_ORDERS):
    # Pick product
    idx          = np.random.choice(len(all_products), p=all_weights)
    cat, product_name, base_price, base_discount = all_products[idx]

    # Customer
    customer_id = random.choice(customers)
    segment     = customer_segments[customer_id]

    # Discount by segment
    if segment == 'VIP':
        discount = round(random.uniform(0.20, 0.35), 2)
    elif segment == 'Premium':
        discount = round(random.uniform(0.10, 0.25), 2)
    elif segment == 'New':
        discount = round(random.uniform(0.05, 0.15), 2)
    else:
        discount = round(random.uniform(0.0, base_discount), 2)

    quantity   = random.choices([1,2,3,4,5,6],
                                 weights=[45,25,12,8,6,4])[0]
    price      = round(base_price * random.uniform(0.93, 1.07), 2)
    revenue    = round(price * quantity * (1 - discount), 2)
    profit_pct = {
        'Electronics': 0.12, 'Clothing': 0.35,
        'Home & Kitchen': 0.25, 'Beauty & Health': 0.40,
        'Sports & Fitness': 0.30, 'Books & Stationery': 0.45,
        'Grocery & Food': 0.20, 'Toys & Baby': 0.28,
    }[cat]
    profit     = round(revenue * profit_pct, 2)

    # Dates
    order_date    = start_date + timedelta(days=random.randint(0, 729))
    delivery_days = random.choices([1,2,3,4,5,7,10],
                                    weights=[5,15,30,25,15,8,2])[0]
    delivery_date = order_date + timedelta(days=delivery_days)

    # Region and city
    region = random.choices(REGIONS, weights=REGION_WEIGHTS)[0]
    city   = random.choice(CITIES_BY_REGION[region])

    # Payment
    payment = random.choices(PAYMENT_METHODS,
                              weights=PAYMENT_WEIGHTS)[0]

    # Ratings
    rating  = random.choices([1,2,3,4,5],
                               weights=[3,6,18,42,31])[0]

    # Return
    is_returned   = random.choices([True, False],
                                    weights=[12, 88])[0]
    return_reason = random.choice(RETURN_REASONS) if is_returned else None

    # Repeat customer flag
    is_repeat = random.choices([True, False], weights=[65, 35])[0]

    # Shipping cost
    shipping_cost = random.choices([0, 49, 99, 149],
                                    weights=[40, 30, 20, 10])[0]

    # SKU ID
    sku_id = f"SKU{str(idx+1).zfill(4)}"

    orders.append({
        'order_id'        : f"ORD{str(i+1).zfill(6)}",
        'order_date'      : order_date,
        'delivery_date'   : delivery_date,
        'delivery_days'   : delivery_days,
        'customer_id'     : customer_id,
        'customer_segment': segment,
        'is_repeat_customer': is_repeat,
        'sku_id'          : sku_id,
        'product_name'    : product_name,
        'category'        : cat,
        'price'           : price,
        'quantity'        : quantity,
        'discount'        : discount,
        'revenue'         : revenue,
        'profit'          : profit,
        'profit_margin_pct': profit_pct,
        'region'          : region,
        'city'            : city,
        'payment_method'  : payment,
        'rating'          : rating,
        'is_returned'     : is_returned,
        'return_reason'   : return_reason,
        'shipping_cost'   : shipping_cost,
    })

df = pd.DataFrame(orders)

# ── INJECT DIRTINESS ─────────────────────────────────────────
print("Injecting data quality issues...")

# 1. Null revenues (~2%)
df.loc[df.sample(frac=0.02).index, 'revenue'] = None

# 2. Null customer segments (~2%)
df.loc[df.sample(frac=0.02).index, 'customer_segment'] = None

# 3. Negative quantities (~1%)
df.loc[df.sample(frac=0.01).index, 'quantity'] = -1

# 4. Duplicate rows (~2%)
dupes = df.sample(frac=0.02, random_state=1)
df    = pd.concat([df, dupes], ignore_index=True)

# 5. Outlier prices (~1%)
df.loc[df.sample(frac=0.01).index, 'price'] *= 10

# 6. Missing order dates (~1%)
df.loc[df.sample(frac=0.01).index, 'order_date'] = None

# 7. Missing cities (~1.5%)
df.loc[df.sample(frac=0.015).index, 'city'] = None

# 8. Missing ratings (~2%)
df.loc[df.sample(frac=0.02).index, 'rating'] = None

print(f"\nRaw dataset: {len(df)} rows")
print(f"Columns ({len(df.columns)}): {list(df.columns)}")

# ── SAVE ─────────────────────────────────────────────────────
df.to_csv('raw_orders.csv', index=False)
print(f"\nSaved: raw_orders.csv")
print(f"Sample:")
print(df.head(3).to_string())