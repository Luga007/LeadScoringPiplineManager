import streamlit as st
import pandas as pd
import requests
from openai import OpenAI

# -----------------------
# CONFIG
# -----------------------
API_URL = "https://leadscoringpiplinemanager.onrender.com/api/v1"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Lead Scoring", layout="wide")
st.title("🎯 Lead Scoring & Pipeline Manager")

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------
st.sidebar.header("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Budget Summary",
        "Industry Analysis",
        "High Value Leads",
        "Top Leads",
        "All Leads",
        "Problem Board",
        "AI Assistant"
    ]
)

# -----------------------
# AI FUNCTION
# -----------------------
def ask_ai(question, df):
    if df.empty:
        return "No data available for analysis."

    context = df.head(30).to_csv(index=False)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "You are a CRM AI assistant. You analyze sales leads and suggest actions."
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nCRM DATA:\n{context}"
            }
        ]
    )

    return response.output_text


# -----------------------
# TRELLO FUNCTION
# -----------------------
def create_trello_card(title, description):
    url = "https://api.trello.com/1/cards"

    query = {
        'key': st.secrets["TRELLO_API_KEY"],
        'token': st.secrets["TRELLO_TOKEN"],
        'idList': st.secrets["TRELLO_LIST_ID"],
        'name': title,
        'desc': description
    }

    response = requests.post(url, params=query)
    return response.status_code


# -----------------------
# Upload CSV
# -----------------------
st.sidebar.header("Upload CSV")

uploaded_file = st.sidebar.file_uploader("Upload leads CSV", type=["csv"])

if uploaded_file:
    files = {
        "file": (uploaded_file.name, uploaded_file, "text/csv")
    }
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


# =====================================================
# PAGES
# =====================================================

# 🟢 DASHBOARD
if page == "Dashboard":
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Leads", len(df))
        col2.metric("Avg Conversion", round(df["conversion_probability"].mean(), 2))
        col3.metric("High Priority", len(df[df["conversion_probability"] > 0.7]))
        col4.metric("Total Value", int(df["budget"].sum()))
    else:
        st.warning("No data available")

    st.subheader("Conversion Distribution")
    if not df.empty:
        st.bar_chart(df["conversion_probability"])


# 💰 BUDGET SUMMARY
elif page == "Budget Summary":
    st.subheader("💰 Budget Summary")

    if not df.empty:
        budget_summary = pd.DataFrame({
            "Metric": ["Min Budget", "Max Budget", "Average Budget", "Total Budget"],
            "Value": [
                df["budget"].min(),
                df["budget"].max(),
                int(df["budget"].mean()),
                int(df["budget"].sum())
            ]
        })
        st.table(budget_summary)


# 🏭 INDUSTRY ANALYSIS
elif page == "Industry Analysis":
    st.subheader("🏭 Budget by Industry")

    if not df.empty and "industry" in df.columns:
        industry_budget = (
            df.groupby("industry")["budget"]
            .agg(["count", "sum", "mean"])
            .reset_index()
            .rename(columns={
                "count": "Leads",
                "sum": "Total Budget",
                "mean": "Avg Budget"
            })
        )
        st.dataframe(industry_budget, use_container_width=True)


# 🔥 HIGH VALUE LEADS
elif page == "High Value Leads":
    st.subheader("🔥 High Value Leads")

    if not df.empty:
        high_value_df = df[df["budget"] > df["budget"].mean()]
        st.dataframe(high_value_df, use_container_width=True)


# ⭐ TOP LEADS + TRELOO
elif page == "Top Leads":
    st.subheader("⭐ Top Leads")

    if not df.empty:
        top_leads = df.sort_values(
            by="conversion_probability", ascending=False
        ).head(10)

        st.dataframe(top_leads, use_container_width=True)

        st.subheader("📌 Send Lead to Trello")

        selected_name = st.selectbox("Select Lead", top_leads["name"])

        if st.button("Send to Trello"):
            lead = top_leads[top_leads["name"] == selected_name].iloc[0]

            title = f"Lead: {lead['name']}"
            desc = f"""
Email: {lead['email']}
Industry: {lead['industry']}
Budget: {lead['budget']}
Conversion: {lead['conversion_probability']}
"""

            status = create_trello_card(title, desc)

            if status == 200:
                st.success("Sent to Trello ✅")
            else:
                st.error("Failed ❌")


# 📋 ALL LEADS
elif page == "All Leads":
    st.subheader("Leads Table")

    if not df.empty:
        st.dataframe(df, use_container_width=True)


# 🧩 PROBLEM BOARD (TRELL0-LIKE)
elif page == "Problem Board":
    st.subheader("🧩 Problem Board")

    if "problems" not in st.session_state:
        st.session_state.problems = []

    st.markdown("### ➕ Add Problem")

    title = st.text_input("Title")
    desc = st.text_area("Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Add Problem"):
        if title:
            st.session_state.problems.append({
                "title": title,
                "desc": desc,
                "priority": priority
            })
            st.success("Added ✅")

    st.markdown("### 📋 Board")

    col1, col2, col3 = st.columns(3)

    for p in st.session_state.problems:

        card = f"""
**{p['title']}**  
{p['desc']}  
🏷 {p['priority']}
"""

        if p["priority"] == "High":
            col1.warning(card)
        elif p["priority"] == "Medium":
            col2.info(card)
        else:
            col3.success(card)


# 🤖 AI ASSISTANT
elif page == "AI Assistant":
    st.subheader("AI CRM Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input("Ask about your leads...")

    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})

        with st.chat_message("user"):
            st.write(user_msg)

        reply = ask_ai(user_msg, df)

        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)