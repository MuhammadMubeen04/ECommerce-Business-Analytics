"""
E-Commerce Business Analytics
-----------------------------
EDA + key business questions + charts + summary exports for Power BI.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
CHARTS = Path(__file__).parent / "charts"
CHARTS.mkdir(exist_ok=True)
SUMMARIES = DATA / "summaries"
SUMMARIES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)

# Load
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["OrderDate", "DeliveryDate"])
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["JoinDate"])
df = orders.merge(customers, on="CustomerID", how="left")

print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Order lines : {len(df):,}")
print(f"Orders      : {df['OrderID'].nunique():,}")
print(f"Customers   : {df['CustomerID'].nunique():,}")
print(f"Date range  : {df['OrderDate'].min().date()} → {df['OrderDate'].max().date()}")
print(f"Total Sales : ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Return Rate : {(df['Returned']=='Yes').mean()*100:.1f}%")
print(f"Avg Rating  : {df['CustomerRating'].mean():.2f}")

# KPIs
print("\n" + "=" * 60)
print("OVERALL KPIs")
print("=" * 60)
print(f"Profit Margin : {df['Profit'].sum()/df['Sales'].sum()*100:.2f}%")
print(f"AOV           : ${df.groupby('OrderID')['Sales'].sum().mean():.2f}")

# Category
print("\n" + "=" * 60)
print("CATEGORY PERFORMANCE")
print("=" * 60)
cat = df.groupby("Category").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum"),
    ReturnRate=("Returned", lambda x: (x == "Yes").mean() * 100),
    AvgRating=("CustomerRating", "mean")
).round(2)
cat["Margin%"] = (cat["Profit"] / cat["Revenue"] * 100).round(2)
print(cat.sort_values("Revenue", ascending=False))

# Discount impact
df["DiscountBand"] = pd.cut(df["Discount"], bins=[-0.01, 0, 0.10, 0.20, 1],
                            labels=["No Discount", "1-10%", "11-20%", "21%+"])
print("\n" + "=" * 60)
print("DISCOUNT IMPACT")
print("=" * 60)
disc = df.groupby("DiscountBand", observed=True).agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Margin=("Profit", lambda x: x.sum() / df.loc[x.index, "Sales"].sum() * 100 if len(x) else 0)
).round(2)
print(disc)

# ---------- Charts ----------
# 1. Revenue & Profit by Category
fig, ax = plt.subplots()
cat_sorted = cat.sort_values("Revenue", ascending=True)
cat_sorted[["Revenue", "Profit"]].plot(kind="barh", ax=ax, color=["#4e79a7", "#59a14f"])
ax.set_title("Revenue & Profit by Category")
ax.set_xlabel("Amount ($)")
plt.tight_layout()
plt.savefig(CHARTS / "01_category_revenue_profit.png", dpi=150)
plt.close()

# 2. Monthly Revenue Trend
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
monthly = df.groupby("YearMonth")["Sales"].sum()
fig, ax = plt.subplots(figsize=(14, 5))
monthly.plot(ax=ax, marker="o", color="#4e79a7")
ax.set_title("Monthly Revenue Trend")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig(CHARTS / "02_monthly_revenue.png", dpi=150)
plt.close()

# 3. Return Rate by Category
fig, ax = plt.subplots()
cat["ReturnRate"].sort_values().plot(kind="barh", color="#e15759", ax=ax)
ax.set_title("Return Rate by Category (%)")
ax.set_xlabel("Return Rate (%)")
plt.tight_layout()
plt.savefig(CHARTS / "03_return_rate_by_category.png", dpi=150)
plt.close()

# 4. Discount vs Profit Margin
fig, ax = plt.subplots()
disc["Margin"].plot(kind="bar", color="#f28e2b", ax=ax)
ax.set_title("Profit Margin by Discount Band")
ax.set_ylabel("Profit Margin (%)")
ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
plt.savefig(CHARTS / "04_discount_impact.png", dpi=150)
plt.close()

# 5. Region Performance
region = df.groupby("Region").agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Revenue", ascending=False)
fig, ax = plt.subplots()
region.plot(kind="bar", ax=ax, color=["#4e79a7", "#59a14f"])
ax.set_title("Revenue & Profit by Region")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "05_region_performance.png", dpi=150)
plt.close()

# 6. Rating Distribution
fig, ax = plt.subplots()
df["CustomerRating"].value_counts().sort_index().plot(kind="bar", color="#76b7b2", ax=ax)
ax.set_title("Customer Rating Distribution")
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(CHARTS / "06_rating_distribution.png", dpi=150)
plt.close()

# 7. Top 10 Products by Profit
top_prod = df.groupby("ProductName")["Profit"].sum().nlargest(10).sort_values()
fig, ax = plt.subplots()
top_prod.plot(kind="barh", color="#59a14f", ax=ax)
ax.set_title("Top 10 Products by Profit")
ax.set_xlabel("Profit ($)")
plt.tight_layout()
plt.savefig(CHARTS / "07_top_products_profit.png", dpi=150)
plt.close()

# 8. Ship Mode analysis
ship = df.groupby("ShipMode").agg(
    Orders=("OrderID", "nunique"),
    AvgDelivery=("DeliveryDays", "mean"),
    AvgRating=("CustomerRating", "mean")
)
fig, ax = plt.subplots()
ship["AvgDelivery"].plot(kind="bar", color="#edc948", ax=ax)
ax.set_title("Average Delivery Days by Ship Mode")
ax.set_ylabel("Days")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "08_delivery_by_shipmode.png", dpi=150)
plt.close()

print(f"\nCharts saved to: {CHARTS}")

# Exports
cat.to_csv(SUMMARIES / "category_summary.csv")
disc.to_csv(SUMMARIES / "discount_summary.csv")
region.to_csv(SUMMARIES / "region_summary.csv")
df.to_csv(SUMMARIES / "ecommerce_enriched.csv", index=False)

kpi = pd.DataFrame([{
    "Total_Orders": df["OrderID"].nunique(),
    "Total_Customers": df["CustomerID"].nunique(),
    "Total_Revenue": round(df["Sales"].sum(), 2),
    "Total_Profit": round(df["Profit"].sum(), 2),
    "Profit_Margin_Pct": round(df["Profit"].sum() / df["Sales"].sum() * 100, 2),
    "Return_Rate_Pct": round((df["Returned"] == "Yes").mean() * 100, 2),
    "Avg_Rating": round(df["CustomerRating"].mean(), 2)
}])
kpi.to_csv(SUMMARIES / "overall_kpis.csv", index=False)

print(f"Summaries exported to: {SUMMARIES}")
print("\n✅ E-Commerce analysis complete.")