import streamlit as st
import pandas as pd
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="wakulima_agro_db"
    )

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    conn = get_connection()
    query = "SELECT * FROM products"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# ---------------- DASHBOARD UI ----------------
st.title("🌾 Wakulima Agro Cost Analysis Dashboard")

# KPIs
st.metric("Total Products", len(df))
st.metric("Total Production Cost", round(df["production_cost"].sum(), 2))
st.metric("Average Cost", round(df["cost"].mean(), 2))

st.divider()

# Filters
category = st.selectbox("Filter by Category", ["All"] + list(df["category"].unique()))

if category != "All":
    df = df[df["category"] == category]

# ---------------- TABLE ----------------
st.subheader("📦 Products Data")
st.dataframe(df)

# ---------------- ANALYSIS ----------------
st.subheader("📊 Category Summary")
category_summary = df.groupby("category")["production_cost"].sum()
st.bar_chart(category_summary)

st.subheader("💰 Top 5 Expensive Products")
top5 = df.sort_values("production_cost", ascending=False).head(5)
st.dataframe(top5)

# ---------------- RUN ----------------
# streamlit run app.py
