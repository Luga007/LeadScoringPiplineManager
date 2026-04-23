import streamlit as st
import pandas as pd
import requests
from openai import OpenAI

# -----------------------
# CONFIG
# -----------------------
API_URL = "https://leadscoringpiplinemanager.onrender.com/api/v1"

client = OpenAI(api_key="OPENAI_API_KEY")  # use env variable in real projects

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("🎯 Lead Scoring & Pipeline Manager")


# -----------------------
#  AI FUNCTION
# -----------------------
def ask_ai(question, df):
    if df.empty:
        return "No data available for analysis."

    context = df.head(20).to_string()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a CRM AI assistant. "
                    "You analyze sales leads, find insights, and suggest actions."
                )
            },
            {
                "role": "user",
                "content": f"""
Question: {question}

CRM DATA:
{context}
"""
            }
        ]
    )

    return response.choices[0].message.content


# -----------------------
# Upload CSV
# -----------------------
st.sidebar.header("Upload CSV")

uploaded_file = st.sidebar.file_uploader("Upload leads CSV", type=["csv"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        st.sidebar.success("Uploaded successfully ✅")
    else:
        st.sidebar.error("Upload failed ❌")


# -----------------------
# Filters
# -----------------------
st.sidebar.header("Filters")

min_prob = st.sidebar.slider("Min Conversion Probability", 0.0, 1.0, 0.0)

min_budget, max_budget = st.sidebar.slider(
    "Budget Range",
    0, 100000,
    (0, 100000)
)

# Industry list
try:
    industries_resp = requests.get(f"{API_URL}/leads/industries")
    industries_list = industries_resp.json() if industries_resp.status_code == 200 else []
except:
    industries_list = []

selected_industries = st.sidebar.multiselect(
    "Industry",
    options=industries_list if industries_list else ["IT", "Finance", "SaaS"]
)


# -----------------------
# Fetch Leads
# -----------------------
params = {"min_prob": min_prob}

if selected_industries:
    for ind in selected_industries:
        params.setdefault("industries", []).append(ind)

response = requests.get(f"{API_URL}/leads", params=params)

if response.status_code != 200:
    st.error("Backend not running ❌")
    st.stop()

data = response.json()
df = pd.DataFrame(data)


# -----------------------
# Local Filters
# -----------------------
if not df.empty:
    df = df[df["budget"] >= min_budget]
    df = df[df["budget"] <= max_budget]


# -----------------------
# KPIs
# -----------------------
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Leads", len(df))
    col2.metric("Avg Conversion", round(df["conversion_probability"].mean(), 2))
    col3.metric("High Priority", len(df[df["conversion_probability"] > 0.7]))
    col4.metric("Total Value", int(df["budget"].sum()))
else:
    st.warning("No data available")


# -----------------------
# Chart
# -----------------------
st.subheader("Conversion Distribution")

if not df.empty:
    st.bar_chart(df["conversion_probability"])


# -----------------------
# Table
# -----------------------
st.subheader("Leads Table")

if not df.empty:
    st.dataframe(df, use_container_width=True)


# =====================================================
# AI CHAT (CLEAN CHATGPT STYLE UI)
# =====================================================
st.subheader("AI CRM Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# user input
user_msg = st.chat_input("Ask about your leads...")

if user_msg:
    # store user msg
    st.session_state.messages.append({"role": "user", "content": user_msg})

    with st.chat_message("user"):
        st.write(user_msg)

    # AI response
    reply = ask_ai(user_msg, df)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)