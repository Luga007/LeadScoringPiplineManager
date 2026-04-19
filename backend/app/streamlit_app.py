import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api/v1"

st.title("🎯 Lead Scoring Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
min_prob = st.sidebar.slider("Min Conversion", 0.0, 1.0, 0.0)
industry_filter = st.sidebar.text_input("Industry")

# Load leads
response = requests.get(f"{API_URL}/leads")

if response.status_code != 200:
    st.error("Backend not running ❌")
    st.stop()

data = response.json()
df = pd.DataFrame(data)

if not df.empty:

    # Filters
    df = df[df["conversion_probability"] >= min_prob]

    if industry_filter:
        df = df[df["industry"] == industry_filter]

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Leads", len(df))
    col2.metric("Avg Conversion", round(df["conversion_probability"].mean(), 2))
    col3.metric("High Priority", len(df[df["conversion_probability"] > 0.7]))
    col4.metric("Total Value", int(df["budget"].sum()))

    st.subheader("Leads Table")
    st.dataframe(df)

    st.subheader("Conversion Distribution")
    st.bar_chart(df["conversion_probability"])

else:
    st.warning("No data available")