import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Customer Intelligence Platform", layout="wide")

st.title("Customer Intelligence Platform")
st.write("Dashboard for customer segmentation and inactivity analysis.")
st.markdown("### Insights")
st.write("""
- Champions generate the majority of revenue  
- At Risk customers are mostly inactive  
- Retention strategies should focus on high-value inactive customers  
""")

# -----------------------------
# Load data
# -----------------------------
BASE_PATH = Path(__file__).resolve().parent.parent
file_path = BASE_PATH / "data/processed/customer_features.csv"

df = pd.read_csv(file_path)

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(df))
col2.metric("Total Revenue", f"{df['total_revenue'].sum():,.0f}")
col3.metric("Inactive Customers", int(df["is_inactive"].sum()))
col4.metric("Avg Order Value", f"{df['avg_order_value'].mean():.2f}")

st.markdown("---")

# -----------------------------
# Segment Distribution
# -----------------------------
st.subheader("Customer Segments")

segment_counts = df["segment"].value_counts()

fig1, ax1 = plt.subplots()
segment_counts.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Customers")
ax1.set_title("Customer Segments")
st.pyplot(fig1)

# -----------------------------
# Revenue per Segment
# -----------------------------
st.subheader("Revenue per Segment")

segment_revenue = df.groupby("segment")["total_revenue"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
segment_revenue.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Revenue")
ax2.set_title("Revenue per Segment")
st.pyplot(fig2)

# -----------------------------
# Activity
# -----------------------------
st.subheader("Customer Activity")

activity = df["is_inactive"].value_counts()
activity.index = ["Active", "Inactive"]

fig3, ax3 = plt.subplots()
activity.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Customers")
ax3.set_title("Active vs Inactive")
st.pyplot(fig3)

# -----------------------------
# Top Customers
# -----------------------------
st.subheader("Top Customers")

top_customers = df.sort_values("total_revenue", ascending=False).head(10)
st.dataframe(top_customers)

# -----------------------------
# Priority Filter
# -----------------------------
st.subheader("Priority Segments")

priority = st.selectbox("Select Priority", df["priority"].unique())

filtered = df[df["priority"] == priority]
st.dataframe(filtered.sort_values("total_revenue", ascending=False).head(20))