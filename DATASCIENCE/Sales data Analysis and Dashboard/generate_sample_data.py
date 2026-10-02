"""Creates a realistic sample sales dataset (sales_data.csv).
Skip this file if you already have your own dataset with the same columns:
Order ID, Order Date, Customer, Product, Category, Quantity, Sales, Region, Profit
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

products = {  # product: (category, unit price, profit margin)
    "Laptop": ("Electronics", 900, 0.16), "Smartphone": ("Electronics", 600, 0.18),
    "Headphones": ("Electronics", 90, 0.22), "Monitor": ("Electronics", 250, 0.15),
    "Office Chair": ("Furniture", 180, 0.14), "Desk": ("Furniture", 320, 0.12),
    "T-Shirt": ("Clothing", 25, 0.30), "Jeans": ("Clothing", 55, 0.28),
    "Keyboard": ("Office Supplies", 45, 0.25), "Mouse": ("Office Supplies", 20, 0.27),
    "Printer": ("Office Supplies", 150, 0.10), "Notebook Pack": ("Others", 12, 0.35),
}
weights = np.array([9, 10, 8, 6, 7, 4, 12, 8, 9, 10, 4, 6], dtype=float)
weights /= weights.sum()
names = list(products)

prod = rng.choice(names, size=N, p=weights)
dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 365, N), unit="D")
# seasonality: more orders towards year end
keep = rng.random(N) < (0.55 + 0.45 * dates.dayofyear / 365)
qty = rng.integers(1, 6, N)
price = np.array([products[p][1] for p in prod]) * rng.uniform(0.9, 1.1, N)
sales = np.round(price * qty, 2)
margin = np.array([products[p][2] for p in prod]) + rng.normal(0, 0.04, N)

df = pd.DataFrame({
    "Order ID": [f"ORD-{100000 + i}" for i in range(N)],
    "Order Date": dates.strftime("%Y-%m-%d"),
    "Customer": [f"CUST-{c:04d}" for c in rng.integers(1, 1500, N)],
    "Product": prod,
    "Category": [products[p][0] for p in prod],
    "Quantity": qty,
    "Sales": sales,
    "Region": rng.choice(["North", "South", "East", "West", "Central"], N, p=[.28, .22, .2, .17, .13]),
    "Profit": np.round(sales * margin, 2),
})[keep].reset_index(drop=True)

# Inject real-world messiness so the cleaning step has work to do
df.loc[df.sample(60, random_state=1).index, "Sales"] = np.nan
df.loc[df.sample(40, random_state=2).index, "Region"] = np.nan
df.loc[df.sample(30, random_state=3).index, "Customer"] = np.nan
df.loc[df.sample(25, random_state=4).index, "Region"] = " north "      # messy text
df = pd.concat([df, df.sample(45, random_state=5)]).sample(frac=1, random_state=6)  # duplicates
df.to_csv("sales_data.csv", index=False)
print(f"sales_data.csv created with {len(df)} rows")
