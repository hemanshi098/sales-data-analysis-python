import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset. In Google Colab, upload sales_data.csv when prompted.
try:
    from google.colab import files
    uploaded = files.upload()
    file_name = next(iter(uploaded))
except Exception:
    file_name = "sales_data.csv"

df = pd.read_csv(file_name)

print("FIRST FIVE ROWS")
print(df.head())

print("\nDATASET INFORMATION")
df.info()

print("\nMISSING VALUES")
print(df.isna().sum())

print("\nDUPLICATE ROWS:", df.duplicated().sum())

# Clean the data
df = df.drop_duplicates().copy()
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["city"] = df["city"].fillna("Unknown")
df["product"] = df["product"].fillna("Unknown")
df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
df = df.dropna(subset=["order_date", "quantity", "revenue", "cost"])

# Calculate profit and month
df["profit"] = df["revenue"] - df["cost"]
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# Key performance indicators
print("\nKEY BUSINESS METRICS")
print("Total revenue:", round(df["revenue"].sum(), 2))
print("Total cost:", round(df["cost"].sum(), 2))
print("Total profit:", round(df["profit"].sum(), 2))
print("Total orders:", df["order_id"].nunique())
print("Average order revenue:", round(df["revenue"].mean(), 2))

# Product and city performance
print("\nREVENUE BY PRODUCT")
print(df.groupby("product")["revenue"].sum().sort_values(ascending=False))

print("\nREVENUE BY CITY")
print(df.groupby("city")["revenue"].sum().sort_values(ascending=False))

# Monthly revenue trend
monthly = df.groupby("month")["revenue"].sum()
print("\nMONTHLY REVENUE")
print(monthly)

monthly.plot(kind="line", marker="o", title="Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Revenue by product chart
df.groupby("product")["revenue"].sum().sort_values().plot(
    kind="barh", title="Revenue by Product"
)
plt.xlabel("Revenue")
plt.tight_layout()
plt.show()

# Revenue by city chart
df.groupby("city")["revenue"].sum().sort_values().plot(
    kind="bar", title="Revenue by City"
)
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

print("\nBUSINESS INSIGHTS")
print("- Compare product and city revenue rankings to identify top performers.")
print("- Use the monthly trend to identify stronger and weaker sales months.")
print("- Profit is calculated as revenue minus cost.")
