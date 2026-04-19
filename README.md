# 🎯 Lead Scoring & Pipeline Manager

CRM-based Lead Scoring system that analyzes leads, predicts conversion probability, and provides sales strategy recommendations. Built with Streamlit and machine learning.

---

## 🚀 Project Overview

This application allows users (admins/sales teams) to upload CRM lead data via CSV and automatically:

- Analyze each lead
- Predict conversion probability
- Recommend pricing and sales strategy
- Display KPI metrics and insights in real-time dashboard

---

## ✨ Features

- 📂 Upload CSV file with leads data
- 🧠 ML-based conversion probability prediction
- 💰 Pricing recommendation per lead
- 📊 KPI dashboard (high priority leads, conversion rate, total value)
- 🔎 Advanced filtering:
  - Budget slider
  - Industry multiselect
  - Conversion probability filter
- 📈 Data visualization:
  - Lead distribution charts (bar/line charts)
- 📋 Interactive dataframe:
  - Sorting
  - Expandable details
- 🎛 Streamlit sidebar controls

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas / NumPy
- Scikit-learn (for ML model)
- Matplotlib / Plotly (for charts)

---

## ⚙️ Installation (Local Setup)

Clone the repository:

```bash
Create virtual environment:

python -m venv venv

Activate environment:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶️ Run the App

Start Streamlit app:

streamlit run app.py

Then open in browser:

http://localhost:8501
☁️ Deployment (Streamlit Cloud)

This project is deployed on Streamlit Cloud.

Requirements:
App must be connected to GitHub repository
Must include requirements.txt
Must have app.py as entry point
Live App:

👉 https://your-streamlit-app-url.streamlit.app

📂 Project Structure
lead-scoring-app/
│
├── app.py
├── model.pkl
├── requirements.txt
├── data/
├── utils/
│   ├── preprocessing.py
│   ├── prediction.py
│
└── README.md
📊 Key Metrics
High Priority Leads
Conversion Rate
Total Lead Value
Average Deal Size
Probability Distribution
📌 How It Works
Admin uploads CSV file
Data is cleaned and preprocessed
ML model calculates conversion probability
System assigns:
Lead priority
Pricing recommendation
Dashboard visualizes insights
📄 License

This project is licensed under the MIT License.


---

Если хочешь дальше улучшить проект, я могу:
- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- или :contentReference[oaicite:2]{index=2}
- или :contentReference[oaicite:2]{index=2}
