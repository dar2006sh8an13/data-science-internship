from pathlib import Path
import requests
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "results"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
CSV = DATA / "Sample-Superstore.csv"
URL = "https://raw.githubusercontent.com/vaibhavisnayak/data-analysis/main/Sample%20-%20Superstore.csv"


def load():
    if not CSV.exists():
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        CSV.write_bytes(response.content)
    df = pd.read_csv(CSV, encoding="latin1")
    df.columns = df.columns.str.strip()
    return df


def clean(df):
    before = len(df)
    df = df.drop_duplicates().copy()
    for c in ["Order Date", "Ship Date"]:
        if c in df:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ["Sales", "Profit", "Quantity", "Discount"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    required = ["Order Date", "Sales", "Profit", "Quantity", "Discount", "Category", "Region"]
    df = df.dropna(subset=[c for c in required if c in df.columns])
    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    pd.DataFrame({"metric": ["rows_before", "duplicates_removed", "rows_after", "missing_cells_after"],
                  "value": [before, before-len(df), len(df), int(df.isna().sum().sum())]}).to_csv(OUT/"cleaning_summary.csv", index=False)
    return df


def aggregate(df, dimensions):
    return (df.groupby(dimensions).agg(orders=("Order ID","nunique"), sales=("Sales","sum"),
            profit=("Profit","sum"), units=("Quantity","sum"), avg_discount=("Discount","mean"))
            .assign(profit_margin=lambda x: x.profit/x.sales.replace(0,np.nan))
            .sort_values("sales", ascending=False))


def main():
    df = clean(load())
    category = aggregate(df, ["Category"])
    subcat = aggregate(df, ["Sub-Category"])
    region = aggregate(df, ["Region"])
    segment = aggregate(df, ["Segment"])
    monthly = df.groupby("Order Month").agg(sales=("Sales","sum"), profit=("Profit","sum"))
    for name, table in [("category_performance",category),("subcategory_performance",subcat),
                        ("region_performance",region),("segment_performance",segment),
                        ("monthly_sales_profit",monthly)]:
        table.to_csv(OUT/f"{name}.csv")

    corr = df[["Sales","Profit","Quantity","Discount"]].corr()
    corr.to_csv(OUT/"correlation_matrix.csv")
    kpis = {"transaction_lines":len(df), "orders":df["Order ID"].nunique(),
            "customers":df["Customer ID"].nunique(), "sales_usd":df.Sales.sum(),
            "profit_usd":df.Profit.sum(), "units":df.Quantity.sum(),
            "profit_margin":df.Profit.sum()/df.Sales.sum(), "average_discount":df.Discount.mean()}
    pd.Series(kpis, name="value").to_csv(OUT/"kpi_summary.csv")

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9,5))
    category[["sales","profit"]].plot(kind="bar", ax=ax, title="Sales and Profit by Category")
    ax.set_ylabel("USD"); fig.tight_layout(); fig.savefig(OUT/"category_sales_profit.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,5))
    region["profit"].plot(kind="bar", ax=ax, title="Profit by Region", ylabel="USD")
    fig.tight_layout(); fig.savefig(OUT/"region_profit.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(11,5))
    monthly["sales"].plot(ax=ax, marker="o", title="Monthly Sales Trend", ylabel="USD")
    fig.tight_layout(); fig.savefig(OUT/"monthly_sales.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=df,x="Discount",y="Profit",hue="Category",alpha=.5,ax=ax)
    ax.set_title("Discount vs Profit"); fig.tight_layout(); fig.savefig(OUT/"discount_vs_profit.png",dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9,6))
    subcat.sort_values("profit").tail(12)["profit"].sort_values().plot(kind="barh",ax=ax,title="Top Sub-Categories by Profit",xlabel="USD")
    fig.tight_layout(); fig.savefig(OUT/"subcategory_profit.png",dpi=160); plt.close(fig)

    best_cat, worst_cat = category.profit.idxmax(), category.profit.idxmin()
    best_region = region.profit.idxmax()
    best_sub, worst_sub = subcat.profit.idxmax(), subcat.profit.idxmin()
    dcorr = corr.loc["Discount","Profit"]
    report = f"""# Retail Sales Analytics Report

## Executive summary
- Transaction lines: {len(df):,}
- Total sales: USD {df.Sales.sum():,.2f}
- Total profit: USD {df.Profit.sum():,.2f}
- Profit margin: {df.Profit.sum()/df.Sales.sum():.2%}
- Unique orders: {df['Order ID'].nunique():,}

## Findings
- Most profitable category: {best_cat} (USD {category.loc[best_cat,'profit']:,.2f}).
- Least profitable category: {worst_cat} (USD {category.loc[worst_cat,'profit']:,.2f}).
- Most profitable region: {best_region} (USD {region.loc[best_region,'profit']:,.2f}).
- Most profitable sub-category: {best_sub}.
- Least profitable sub-category: {worst_sub}.
- Pearson correlation between discount and profit: {dcorr:.3f}.

## Recommendations
1. Review loss-making sub-categories before increasing promotional spending.
2. Compare discount policies by product category and region.
3. Track profit margin alongside sales; revenue growth alone can hide unprofitable transactions.
4. Monitor monthly sales and profit together.

## Limitations
Sample Superstore describes a fictional retailer and is intended for learning. Correlation does not establish causation; product mix, geography, and order size may affect observed relationships. This analysis is descriptive, not a forecast.
"""
    (ROOT/"REPORT.md").write_text(report,encoding="utf-8")
    print(pd.Series(kpis).to_string())
    print("\nCategory performance:\n",category.to_string())
    print("\nRegion performance:\n",region.to_string())
    print("\nDiscount-profit correlation:",round(dcorr,3))
    print("Generated report, CSV summaries, and charts in",OUT)


if __name__ == "__main__":
    main()
