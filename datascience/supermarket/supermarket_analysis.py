"""CodSoft Data Science - Week 3: Supermarket Sales Data Analysis (full solution)"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- Module 1: Load the dataset ----------
if os.path.exists("supermarket_sales.csv"):
    df = pd.read_csv("supermarket_sales.csv")
else:  # sample data with the same 9 columns (used only if the CSV is missing)
    rng = np.random.default_rng(42)
    n = 1000
    cats = {"Food": (1, 6), "Beverages": (1, 4), "Electronics": (20, 120),
            "Clothing": (10, 60), "Household": (3, 15)}
    cat = rng.choice(list(cats), n, p=[.35, .25, .1, .15, .15])
    price = [round(rng.uniform(*cats[c]), 2) for c in cat]
    qty = rng.integers(1, 11, n)
    df = pd.DataFrame({
        "Invoice ID": np.arange(1001, 1001 + n),
        "Date": pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 31, n), unit="D"),
        "Product": [f"{c} item {rng.integers(1, 6)}" for c in cat],
        "Category": cat, "Quantity": qty, "Unit Price": price,
        "Customer Type": rng.choice(["Member", "Normal"], n, p=[.62, .38]),
        "Payment": rng.choice(["Cash", "Credit Card", "Debit Card", "Digital Payment"], n, p=[.42, .28, .2, .1]),
    })
    df["Total"] = (df["Quantity"] * df["Unit Price"]).round(2)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
print("MODULE 1\n", df.head(), "\n")

# ---------- Module 2: Explore ----------
print("MODULE 2\nShape:", df.shape)
df.info()
print(df.describe(), "\n")

# ---------- Module 3: Data quality check ----------
print("MODULE 3\nMissing values:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
print("Invalid quantities:", (df["Quantity"] <= 0).sum(),
      "| Invalid prices:", (df["Unit Price"] <= 0).sum(),
      "| Total mismatch:", (abs(df["Quantity"] * df["Unit Price"] - df["Total"]) > 0.01).sum(), "\n")

# ---------- Module 4: Cleaning ----------
df = df.dropna().drop_duplicates()
df = df[(df["Quantity"] > 0) & (df["Unit Price"] > 0)]
df["Date"] = pd.to_datetime(df["Date"])
print("MODULE 4\nClean shape:", df.shape, "\n")

# ---------- Module 5: Sales statistics ----------
total_sales, average_sales = df["Total"].sum(), df["Total"].mean()
maximum_sale, minimum_sale = df["Total"].max(), df["Total"].min()
print(f"MODULE 5\nTotal: ${total_sales:,.2f}\nAverage: ${average_sales:,.2f}\n"
      f"Highest: ${maximum_sale:,.2f}\nLowest: ${minimum_sale:,.2f}\n")

# ---------- Module 6: Sales by category ----------
category_sales = df.groupby("Category")["Total"].sum().sort_values(ascending=False)
print("MODULE 6\n", category_sales, "\n")

# ---------- Module 8: Quantity by category ----------
quantity = df.groupby("Category")["Quantity"].sum().sort_values(ascending=False)
print("MODULE 8\n", quantity, "\n")

# ---------- Module 9: Payment methods ----------
payment_count = df["Payment"].value_counts()
print("MODULE 9\n", payment_count, "\n")

# ---------- Module 10: Customer type ----------
customer_sales = df.groupby("Customer Type")["Total"].sum()
customer_txn = df["Customer Type"].value_counts()
print("MODULE 10\n", customer_sales, "\n", customer_txn, "\n")

# ---------- Modules 11 & 12: Daily sales / best day ----------
daily_sales = df.groupby("Date")["Total"].sum()
best_day, best_sales = daily_sales.idxmax(), daily_sales.max()
worst_day, worst_sales = daily_sales.idxmin(), daily_sales.min()
print(f"MODULE 11-12\nBest Day: {best_day.date()}  Sales: ${best_sales:,.2f}\n"
      f"Lowest Day: {worst_day.date()}  Sales: ${worst_sales:,.2f}\n"
      f"Average daily sales: ${daily_sales.mean():,.2f}\n")

# ---------- Module 7 + Dashboard (all visualizations) ----------
fig, ax = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Supermarket Sales Dashboard", fontsize=20, fontweight="bold")
pal = sns.color_palette("Set2")

category_sales.plot(kind="bar", ax=ax[0, 0], color=pal, rot=30)
ax[0, 0].set(title="Sales by Category", xlabel="Category", ylabel="Total Sales")

quantity.plot(kind="bar", ax=ax[0, 1], color=pal, rot=30)
ax[0, 1].set(title="Quantity Sold by Category", xlabel="Category", ylabel="Quantity")

payment_count.plot(kind="bar", ax=ax[0, 2], color=pal, rot=30)
ax[0, 2].set(title="Payment Methods", xlabel="Payment Method", ylabel="Transactions")

ax[1, 0].pie(customer_sales, labels=customer_sales.index, autopct="%1.0f%%",
             colors=pal, startangle=90)
ax[1, 0].set_title("Sales by Customer Type")

daily_sales.plot(kind="line", marker="o", ax=ax[1, 1], color="royalblue")
ax[1, 1].scatter(best_day, best_sales, color="red", zorder=5, label=f"Best: ${best_sales:,.0f}")
ax[1, 1].set(title="Daily Sales Trend", xlabel="Date", ylabel="Sales")
ax[1, 1].legend()

sns.heatmap(df.pivot_table(index="Category", columns="Payment", values="Total", aggfunc="sum"),
            annot=True, fmt=".0f", cmap="YlGnBu", ax=ax[1, 2])
ax[1, 2].set_title("Sales: Category x Payment")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(OUT, "dashboard.png"), dpi=130)

# ---------- Verification + Business insights ----------
assert abs(total_sales - category_sales.sum()) < 0.01, "Category totals must match total sales"
assert abs(total_sales - customer_sales.sum()) < 0.01, "Customer totals must match total sales"
assert df.isnull().sum().sum() == 0, "No missing values should remain"

insights = f"""BUSINESS INSIGHTS
1. Total sales: ${total_sales:,.2f} across {len(df)} transactions (avg ${average_sales:,.2f}).
2. Top category by revenue: {category_sales.idxmax()} (${category_sales.max():,.2f}); lowest: {category_sales.idxmin()}.
3. Top category by quantity: {quantity.idxmax()}. Compare with revenue ranking: high quantity does not always mean high revenue.
4. Most used payment method: {payment_count.idxmax()} ({payment_count.max()} transactions).
5. {customer_sales.idxmax()} customers generate more sales ({customer_sales.max() / total_sales:.0%} of revenue).
6. Best day: {best_day.date()} (${best_sales:,.2f}); weakest day: {worst_day.date()} (${worst_sales:,.2f}).
RECOMMENDATIONS: stock more of the top categories, promote loyalty membership,
support the leading payment methods, and run promotions on historically slow days.
"""
print(insights)
open(os.path.join(OUT, "insights.txt"), "w").write(insights)
