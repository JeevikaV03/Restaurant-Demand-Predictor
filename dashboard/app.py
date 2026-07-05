import streamlit as st
import requests
import pandas as pd
import json

# ----------------------------
# Page Header
# ----------------------------
st.title("🍽 Restaurant Demand Predictor")

st.markdown("""
Predict restaurant demand using **Machine Learning**.

This dashboard forecasts expected restaurant orders based on:

- 📅 Date
- ⏰ Hour
- 🍽 Menu Item
""")

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/orders.csv")

# ----------------------------
# Load Model Metrics
# ----------------------------
try:
    with open("model/metrics.json", "r") as f:
        metrics = json.load(f)
except FileNotFoundError:
    with open("../model/metrics.json", "r") as f:
        metrics = json.load(f)

st.subheader("📈 Model Performance")

col1, col2 = st.columns(2)

col1.metric("MAE", metrics["MAE"])
col2.metric("R² Score", metrics["R2 Score"])

# ----------------------------
# Charts
# ----------------------------
st.subheader("📊 Orders by Item")

chart_data = df.groupby("item")["orders"].sum()
st.bar_chart(chart_data)

st.subheader("📈 Rush Hour Analysis")

rush_data = df.groupby("hour")["orders"].mean()
st.line_chart(rush_data)

# ----------------------------
# Top Rush Hours
# ----------------------------
st.subheader("🏆 Top 3 Rush Hours")

top_hours = (
    df.groupby("hour")["orders"]
    .mean()
    .sort_values(ascending=False)
    .head(3)
)

top_hours = top_hours.reset_index()
top_hours.columns = ["Hour", "Average Orders"]

st.table(top_hours)

# ----------------------------
# Dataset Summary
# ----------------------------
st.subheader("📋 Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Food Items", df["item"].nunique())
col3.metric("Average Orders", round(df["orders"].mean(), 2))

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("Prediction Inputs")

date = st.sidebar.date_input("Select Date")

hour = st.sidebar.slider(
    "Select Hour",
    0,
    23
)

item = st.sidebar.selectbox(
    "Select Item",
    [
        "Biryani",
        "Burger",
        "Pizza",
        "Dosa",
        "Idli",
        "FriedRice",
        "Noodles"
    ]
)

day = date.weekday()

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

st.info(f"📅 Selected Day: {days[day]}")

# ----------------------------
# Prediction
# ----------------------------
if st.button("Predict"):

    url = f"http://127.0.0.1:8000/predict?day={day}&hour={hour}&item={item}"

    try:

        response = requests.get(url)
        result = response.json()

        orders = result["predicted_orders"]

        st.subheader("📋 Prediction Summary")

        summary_df = pd.DataFrame({
            "Field": [
                "Date",
                "Day",
                "Hour",
                "Menu Item",
                "Predicted Orders"
            ],
            "Value": [
                date.strftime("%Y-%m-%d"),
                days[day],
                hour,
                item,
                round(orders, 2)
            ]
        })

        st.table(summary_df)

        st.success(f"🎯 Predicted Orders: {round(orders,2)}")

        if orders >= 80:
            st.error("🔥 Very High Demand Expected!")

        elif orders >= 60:
            st.warning("⚠ Moderate Demand Expected")

        else:
            st.info("✅ Low Demand Expected")

        report_df = pd.DataFrame({
            "Date": [date],
            "Day": [days[day]],
            "Hour": [hour],
            "Item": [item],
            "Predicted Orders": [round(orders, 2)]
        })

        csv = report_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Prediction Report",
            data=csv,
            file_name="prediction_report.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("API not running!")
        st.write(e)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Developed using ❤️ Streamlit, FastAPI and Scikit-learn")