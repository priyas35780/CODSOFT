import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")


class SalesAnalyzer:
    """Load -> Explore -> Clean -> KPIs -> Analysis -> Charts -> Dashboard -> Insights."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.insights = []

    # ---------- Module 1 & 2 : Load and explore ----------
    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("\n📥 Data loaded successfully")
        print(self.df.head())
        return self.df

    def explore_data(self):
        df = self.df
        print("\n🔍 EXPLORATION")
        print("Shape          :", df.shape)
        print("Columns        :", list(df.columns))
        print("\nData types & non-null counts:")
        df.info()
        print("\nMissing values:\n", df.isnull().sum()[df.isnull().sum() > 0])
        print("Duplicate rows :", df.duplicated().sum())
        print("\nNumerical statistics:\n", df.describe().round(2))

    # ---------- Module 3 & 4 : Cleaning and missing data ----------
    def clean_data(self):
        df = self.df.copy()
        before = len(df)

        df = df.drop_duplicates()
        print(f"\n🧹 CLEANING\nDuplicates removed: {before - len(df)}")

        # Standardize text values
        for col in ["Region", "Product", "Category", "Customer"]:
            df[col] = df[col].astype("string").str.strip()
        df["Region"] = df["Region"].str.title()

        # Correct data types
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

        # Missing values - choose an appropriate treatment for each column
        df["Region"] = df["Region"].fillna("Unknown")          # keep the sale, label region
        df["Customer"] = df["Customer"].fillna("Unknown")
        # Sales can be recovered: median unit price of the same product x quantity
        unit_price = (df["Sales"] / df["Quantity"]).groupby(df["Product"]).transform("median")
        missing_sales = df["Sales"].isna().sum()
        df["Sales"] = df["Sales"].fillna((unit_price * df["Quantity"]).round(2))
        print(f"Missing Sales recovered from product median price: {missing_sales}")

        # Remove invalid values
        invalid = (df["Quantity"] <= 0) | (df["Sales"] <= 0) | df["Order Date"].isna()
        df = df[~invalid]
        print(f"Invalid rows removed: {invalid.sum()}")

        df["Month"] = df["Order Date"].dt.to_period("M")
        self.df = df.reset_index(drop=True)
        print("Remaining missing values:", int(self.df.isnull().sum().sum()))
        print(f"Clean dataset shape: {self.df.shape}")
        return self.df

    # ---------- Module 5 : KPIs ----------
    def calculate_kpis(self):
        df = self.df
        self.kpis = {
            "Total Sales": df["Sales"].sum(),
            "Total Profit": df["Profit"].sum(),
            "Total Orders": df["Order ID"].nunique(),
            "Total Quantity": int(df["Quantity"].sum()),
            "Customers": df.loc[df["Customer"] != "Unknown", "Customer"].nunique(),
        }
        self.kpis["Average Order Value"] = self.kpis["Total Sales"] / self.kpis["Total Orders"]
        self.kpis["Profit Margin %"] = self.kpis["Total Profit"] / self.kpis["Total Sales"] * 100

        print("\n📊 KEY PERFORMANCE INDICATORS")
        for k, v in self.kpis.items():
            print(f"{k:<22}: {v:,.2f}")
        return self.kpis

    # ---------- Module 6-9 : Analysis ----------
    def run_analysis(self):
        df = self.df
        self.category = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                                                    Quantity=("Quantity", "sum")).sort_values("Sales", ascending=False)
        self.category["Contribution %"] = self.category["Sales"] / self.category["Sales"].sum() * 100

        known = df[df["Region"] != "Unknown"]
        self.region = known.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                                                   Orders=("Order ID", "nunique")).sort_values("Sales", ascending=False)
        self.region["Contribution %"] = self.region["Sales"] / self.region["Sales"].sum() * 100

        self.product = df.groupby("Product").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                                                  Quantity=("Quantity", "sum")).sort_values("Sales", ascending=False)

        self.monthly = df.groupby("Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        self.monthly.index = self.monthly.index.to_timestamp()
        self.monthly["Margin %"] = self.monthly["Profit"] / self.monthly["Sales"] * 100

        print("\n📦 SALES BY CATEGORY\n", self.category.round(2))
        print("\n🌍 SALES BY REGION\n", self.region.round(2))
        print("\n🏷️ TOP 10 PRODUCTS\n", self.product.head(10).round(2))
        print("\n📈 MONTHLY SALES\n", self.monthly.round(2))

    # ---------- Charts ----------
    def create_visualizations(self):
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(x=self.category.index, y=self.category["Sales"], hue=self.category.index, palette="viridis", legend=False, ax=ax)
        ax.set_title("Sales by Category"); ax.set_ylabel("Sales ($)"); ax.set_xlabel("")
        plt.xticks(rotation=20); plt.tight_layout(); plt.savefig("category_sales.png", dpi=120); plt.close()

        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.barplot(x=self.region.index, y=self.region["Sales"], hue=self.region.index, palette="crest", legend=False, ax=ax)
        ax.set_title("Sales by Region"); ax.set_ylabel("Sales ($)"); ax.set_xlabel("")
        plt.tight_layout(); plt.savefig("regional_sales.png", dpi=120); plt.close()

        top = self.product.head(10).iloc[::-1]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.barh(top.index, top["Sales"], color=sns.color_palette("mako", 10))
        ax.set_title("Top 10 Products by Sales"); ax.set_xlabel("Sales ($)")
        plt.tight_layout(); plt.savefig("top_products.png", dpi=120); plt.close()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(self.monthly.index, self.monthly["Sales"], marker="o", color="#2563eb")
        ax.fill_between(self.monthly.index, self.monthly["Sales"], alpha=0.15, color="#2563eb")
        ax.set_title("Monthly Sales Trend"); ax.set_ylabel("Sales ($)")
        plt.tight_layout(); plt.savefig("monthly_trend.png", dpi=120); plt.close()
        print("\n🖼️ Individual charts saved.")

    # ---------- Dashboard ----------
    def build_dashboard(self):
        k = self.kpis
        fig = plt.figure(figsize=(16, 10), facecolor="#f4f6fb")
        fig.suptitle("SALES DASHBOARD", fontsize=22, fontweight="bold", color="#1e1b4b")
        gs = fig.add_gridspec(3, 4, height_ratios=[0.5, 1.5, 1.5], hspace=0.45, wspace=0.35)

        cards = [("Total Sales", f"${k['Total Sales']:,.0f}", "#2563eb"),
                 ("Total Profit", f"${k['Total Profit']:,.0f}", "#7c3aed"),
                 ("Total Orders", f"{k['Total Orders']:,}", "#059669"),
                 ("Total Quantity", f"{k['Total Quantity']:,}", "#ea580c")]
        for i, (label, val, color) in enumerate(cards):
            ax = fig.add_subplot(gs[0, i]); ax.axis("off")
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, color="white", transform=ax.transAxes, ec=color, lw=2))
            ax.text(0.5, 0.68, label, ha="center", fontsize=12, color="#475569")
            ax.text(0.5, 0.25, val, ha="center", fontsize=20, fontweight="bold", color=color)

        ax = fig.add_subplot(gs[1, :3])
        ax.plot(self.monthly.index, self.monthly["Sales"], marker="o", color="#2563eb")
        ax.fill_between(self.monthly.index, self.monthly["Sales"], alpha=0.15, color="#2563eb")
        ax.set_title("Monthly Sales Trend", fontweight="bold")

        ax = fig.add_subplot(gs[1, 3])
        ax.pie(self.category["Sales"], autopct=lambda p: f"{p:.0f}%" if p > 5 else "", startangle=90,
               pctdistance=0.78, wedgeprops=dict(width=0.45), colors=sns.color_palette("Set2"))
        ax.legend(self.category.index, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=8, frameon=False)
        ax.set_title("Sales by Category", fontweight="bold")

        ax = fig.add_subplot(gs[2, :1])
        sns.barplot(x=self.region.index, y=self.region["Sales"], hue=self.region.index, palette="crest", legend=False, ax=ax)
        ax.set_title("Regional Sales", fontweight="bold"); ax.set_xlabel(""); ax.set_ylabel("")

        ax = fig.add_subplot(gs[2, 1:3])
        top = self.product.head(10).iloc[::-1]
        ax.barh(top.index, top["Sales"], color=sns.color_palette("mako", 10))
        ax.set_title("Top 10 Products", fontweight="bold")

        ax = fig.add_subplot(gs[2, 3])
        ax.bar(self.monthly.index.strftime("%b"), self.monthly["Profit"], color="#a78bfa")
        ax2 = ax.twinx(); ax2.plot(self.monthly.index.strftime("%b"), self.monthly["Margin %"], color="#ec4899", marker="o")
        ax2.grid(False); ax.set_title("Profit & Margin %", fontweight="bold"); ax.tick_params(axis="x", labelsize=7)

        plt.savefig("sales_dashboard.png", dpi=120, bbox_inches="tight"); plt.close()
        print("🖥️ Dashboard saved as 'sales_dashboard.png'")

    # ---------- Testing & Insights ----------
    def generate_insights(self):
        c, r, p, m = self.category, self.region, self.product, self.monthly
        first, last = m["Sales"].iloc[:3].mean(), m["Sales"].iloc[-3:].mean()
        trend = "increasing" if last > first * 1.05 else "decreasing" if last < first * 0.95 else "fluctuating"
        self.insights = [
            f"1. Highest-selling category : {c.index[0]} (${c['Sales'].iloc[0]:,.0f}, {c['Contribution %'].iloc[0]:.1f}% of sales)",
            f"2. Best-performing region   : {r.index[0]} (${r['Sales'].iloc[0]:,.0f}, {r['Contribution %'].iloc[0]:.1f}% of sales)",
            f"3. Best-selling product     : {p.index[0]} (${p['Sales'].iloc[0]:,.0f}); lowest: {p.index[-1]} (${p['Sales'].iloc[-1]:,.0f})",
            f"4. Highest sales month      : {m['Sales'].idxmax():%B %Y} (${m['Sales'].max():,.0f}); lowest: {m['Sales'].idxmin():%B %Y}",
            f"5. Most profitable category : {c['Profit'].idxmax()}; most profitable product: {p['Profit'].idxmax()}",
            f"6. Sales trend              : {trend} (first 3 months avg ${first:,.0f} -> last 3 months avg ${last:,.0f})",
            f"7. Overall profit margin    : {self.kpis['Profit Margin %']:.1f}%; average order value ${self.kpis['Average Order Value']:,.2f}",
        ]
        print("\n💡 BUSINESS INSIGHTS")
        print("\n".join(self.insights))
        with open("business_insights.txt", "w", encoding="utf-8") as f:
            f.write("SALES DATA ANALYSIS - BUSINESS INSIGHTS\n" + "=" * 45 + "\n")
            f.write("\n".join(f"{k}: {v:,.2f}" for k, v in self.kpis.items()) + "\n\n")
            f.write("\n".join(self.insights))

    def save_clean_data(self):
        out = self.df.drop(columns=["Month"]).copy()
        out.to_csv("cleaned_sales_data.csv", index=False)
        print("\n✅ 'cleaned_sales_data.csv' saved (ready to import into Power BI / Excel).")


if __name__ == "__main__":
    print("\n📊 Sales Data Analysis & Dashboard System Started 📊")
    FILE_PATH = "sales_data.csv"

    if not os.path.exists(FILE_PATH):
        print(f"Error: '{FILE_PATH}' not found. Run generate_sample_data.py or add your dataset.")
        raise SystemExit

    analyzer = SalesAnalyzer(FILE_PATH)
    analyzer.load_data()
    analyzer.explore_data()
    analyzer.clean_data()
    analyzer.calculate_kpis()
    analyzer.run_analysis()
    analyzer.create_visualizations()
    analyzer.build_dashboard()
    analyzer.generate_insights()
    analyzer.save_clean_data()
