# 🛒 Supermarket Sales Data Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple) ![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange) ![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-teal) ![Level](https://img.shields.io/badge/Level-Easy-green)

**CodSoft Data Science Internship – Week 3**

Analyzing supermarket transaction data with Python to understand sales performance and discover useful business insights.


## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement and Objectives](#-problem-statement-and-objectives)
3. [Tools and Technologies](#-tools-and-technologies)
4. [Dataset](#-dataset)
5. [Project Workflow](#-project-workflow)
6. [Project Structure](#-project-structure)
7. [Module-by-Module Explanation](#-module-by-module-explanation)
8. [Installation and Usage](#-installation-and-usage)
9. [Dashboard](#-dashboard)
10. [Testing the Analysis](#-testing-the-analysis)
11. [Key Findings](#-key-findings)
12. [Business Recommendations](#-business-recommendations)
13. [Challenges and Solutions](#-challenges-and-solutions)
14. [Future Improvements](#-future-improvements)
15. [Learning Outcomes](#-learning-outcomes)
16. [Author](#-author)

## 📌 Project Overview

This project analyzes supermarket sales data using Python. It loads a sales dataset, checks and cleans the data, calculates sales metrics, studies product categories, payment methods and customer behavior, and presents the results as charts and written business insights.

**Final goal:** understand sales performance using data.

## 🎯 Problem Statement and Objectives

A supermarket records every sale, but raw transaction data does not tell the owner what is working. This project answers questions such as:

- How much did the store sell in total, and what is the average transaction value?
- Which product categories earn the most revenue, and which sell the most items?
- Does high quantity always mean high revenue?
- How do customers prefer to pay?
- Do members or normal customers generate more sales?
- How do sales change day by day, and when were sales highest and lowest?

**Objectives**

- Load, explore and clean a real-world style dataset
- Calculate key sales metrics
- Use grouping and aggregation to compare categories, customer types and dates
- Create clear visualizations
- Draw conclusions and give business recommendations

## 🧰 Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data loading, cleaning, filtering, grouping |
| NumPy | Numerical operations |
| Matplotlib | Bar, line and pie charts |
| Seaborn | Styling and heatmap |

## 🗂 Dataset

The dataset contains supermarket transaction records (1,000 rows, 9 columns).

| Column | Description | Data Type |
|---|---|---|
| Invoice ID | Unique transaction ID | int |
| Date | Purchase date | date (converted with `pd.to_datetime`) |
| Product | Product name | text |
| Category | Product category (Food, Beverages, Electronics, Clothing, Household) | text |
| Quantity | Number of items purchased | int |
| Unit Price | Price per item | float |
| Customer Type | Customer category (Member / Normal) | text |
| Payment | Payment method (Cash, Credit Card, Debit Card, Digital Payment) | text |
| Total | Transaction amount (Quantity x Unit Price) | float |

> **Note:** Place `supermarket_sales.csv` in the same folder as the script. If the file is missing, the script generates sample data with the same structure so it can still run. Results from sample data are for demonstration only.

## 🔄 Project Workflow

```
Data → Cleaning → Exploration → Analysis → Visualization → Insights
```

1. **Data:** load the CSV into a Pandas DataFrame
2. **Cleaning:** handle missing values, duplicates, invalid values and date format
3. **Exploration:** check shape, data types and summary statistics
4. **Analysis:** sales metrics, category, payment, customer and daily analysis
5. **Visualization:** charts combined into one dashboard
6. **Insights:** written findings and recommendations

## 📁 Project Structure

```
├── supermarket_analysis.py   # Full analysis script (Modules 1–12)
├── supermarket_sales.csv     # Dataset (add your file here)
├── dashboard.png             # Output dashboard with 6 charts
├── insights.txt              # Generated business insights
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🧩 Module-by-Module Explanation

| # | Module | What it does | Key code |
|---|---|---|---|
| 1 | Load the Dataset | Reads the CSV into a DataFrame | `pd.read_csv()` |
| 2 | Explore the Dataset | Checks records, columns, data types, min/max/mean | `df.shape`, `df.info()`, `df.describe()` |
| 3 | Data Quality Check | Finds missing values, duplicates, invalid quantities and prices, and incorrect totals | `df.isnull().sum()`, `df.duplicated().sum()` |
| 4 | Data Cleaning | Removes missing records and duplicates, filters invalid rows, converts date | `dropna()`, `drop_duplicates()`, `pd.to_datetime()` |
| 5 | Sales Statistics | Total, average, highest and lowest transaction | `sum()`, `mean()`, `max()`, `min()` |
| 6 | Sales by Category | Revenue per product category | `groupby("Category")["Total"].sum()` |
| 7 | Visualize Category Sales | Bar chart to compare categories | `plot(kind="bar")` |
| 8 | Product Quantity Analysis | Items sold per category, compared against revenue | `groupby("Category")["Quantity"].sum()` |
| 9 | Payment Method Analysis | Number of transactions per payment method | `value_counts()` |
| 10 | Customer Analysis | Sales and transaction count by customer type | `groupby("Customer Type")["Total"].sum()` |
| 11 | Daily Sales Analysis | Sales trend over time as a line chart | `groupby("Date")["Total"].sum()` |
| 12 | Highest Sales Day | Best day, lowest day and average daily sales | `idxmax()`, `idxmin()` |

### Example: Data cleaning

```python
df = df.dropna().drop_duplicates()
df = df[(df["Quantity"] > 0) & (df["Unit Price"] > 0)]
df["Date"] = pd.to_datetime(df["Date"])
```

### Example: Category analysis

```python
category_sales = df.groupby("Category")["Total"].sum().sort_values(ascending=False)
quantity = df.groupby("Category")["Quantity"].sum().sort_values(ascending=False)
```

## ⚙️ Installation and Usage

**Requirements:** Python 3.8 or higher

1. Clone or download this project:

   ```bash
   git clone <your-repository-url>
   cd <project-folder>
   ```

2. Install the libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Put `supermarket_sales.csv` in the project folder.

4. Run the script:

   ```bash
   python supermarket_analysis.py
   ```

5. Check the outputs: the console shows every module's results, and `dashboard.png` and `insights.txt` are created in the same folder.

## 📊 Dashboard

| Chart | Type | Question answered |
|---|---|---|
| Sales by Category | Bar | Which category earns the most? |
| Quantity Sold by Category | Bar | Which category sells the most items? |
| Payment Methods | Bar | How do customers prefer to pay? |
| Sales by Customer Type | Pie | Do members or normal customers spend more? |
| Daily Sales Trend | Line | How do sales change over time, and which day was best? |
| Category x Payment | Heatmap | Which category and payment method combinations earn the most? |

## ✅ Testing the Analysis

The script verifies its own results with assertions, and you should also check the following manually:

- [x] Total sales match the sum of category sales
- [x] Total sales match the sum of customer type sales
- [x] No missing values remain after cleaning
- [ ] Average sales look reasonable compared with min and max
- [ ] Highest and lowest sales days match the daily sales table
- [ ] Charts have titles, axis labels and correct values

## 🔍 Key Findings

*Replace this section with the numbers from your own `insights.txt` after running the script on your real dataset.*

| Metric | Result |
|---|---|
| Total sales | ... |
| Average transaction value | ... |
| Highest transaction | ... |
| Lowest transaction | ... |
| Top category by revenue | ... |
| Top category by quantity | ... |
| Most used payment method | ... |
| Customer group with more sales | ... |
| Best sales day | ... |
| Lowest sales day | ... |

## 💡 Business Recommendations

- **Stock planning:** keep the top-selling categories well stocked and review slow ones.
- **Pricing and promotions:** where a category sells many items but earns less revenue, consider bundles or price adjustments.
- **Loyalty program:** promote membership if members drive a large share of sales.
- **Payments:** make sure the most-used payment methods work smoothly at every checkout.
- **Scheduling:** run promotions on slow days and staff up on the busiest days.

## 🧗 Challenges and Solutions

| Challenge | Solution |
|---|---|
| Date stored as text | Converted with `pd.to_datetime()` before time-based analysis |
| Possible missing or duplicate rows | Checked with `isnull()` and `duplicated()`, then removed |
| Invalid quantities or prices | Filtered out rows with zero or negative values |
| Making sure results are correct | Added assertions that totals match across groupings |

## 🚀 Future Improvements

- Add monthly and weekly sales analysis
- Analyze individual products, not only categories
- Build an interactive dashboard with Streamlit or Plotly
- Add sales forecasting with a simple machine learning model
- Package the analysis as a Jupyter Notebook

## 🎓 Learning Outcomes

- Data loading and exploration
- Data cleaning and filtering
- Grouping and aggregation
- Statistical analysis
- Data visualization with Matplotlib and Seaborn
- Finding patterns and drawing conclusions

## 👤 Author

**Your Name**
CodSoft Data Science Intern
GitHub: `your-username` | LinkedIn: `your-profile`
