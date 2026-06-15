st.title("VERSION TEST 2 - IF YOU SEE THIS, DEPLOY WORKS")
import streamlit as st
import pandas as pd
import os
import datetime
import plotly.express as px
import joblib

st.set_page_config(page_title="Smart Fridge", layout="wide")

FILE = "inventory.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["Food", "Quantity", "Category", "Expiration"])
    df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)

model = None
encoder = None

if os.path.exists("food_model.pkl") and os.path.exists("encoder.pkl"):
    model = joblib.load("food_model.pkl")
    encoder = joblib.load("encoder.pkl")
    
def predict_food(days_left, category):
    cat_encoded = encoder.transform([category])[0]
    pred = model.predict([[days_left, cat_encoded]])
    return pred[0]

today = datetime.date.today()

def get_status(expiration_date):
    exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
    days_left = (exp_date - today).days

    if days_left < 0:
        return "🔴 Expired"
    elif days_left <= 2:
        return "🟠 Expiring Soon"
    elif days_left <= 5:
        return "🟡 Medium"
    else:
        return "🟢 Fresh"

df["Status"] = df["Expiration"].apply(get_status)

page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Add Food", "Inventory"]
)

if page == "Dashboard":

    st.title("🥗 Smart Fridge Dashboard")

    expiring_items = df[df["Status"] == "🟠 Expiring Soon"]

    if not expiring_items.empty:
        st.warning("⚠️ You have food expiring soon! Check your inventory.")

    total_items = len(df)
    expired = len(df[df["Status"] == "🔴 Expired"])
    expiring = len(df[df["Status"] == "🟠 Expiring Soon"])
    fresh = len(df[df["Status"] == "🟢 Fresh"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Items", total_items)
    col2.metric("Expired", expired)
    col3.metric("Expiring Soon", expiring)
    col4.metric("Fresh Items", fresh)

    st.write("## 📊 Food Status Distribution")

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig = px.pie(status_counts, names="Status", values="Count")
    st.plotly_chart(fig, use_container_width=True)

    st.write("## 💰 Estimated Food Waste Impact")

    avg_value_per_item = 4
    money_lost = expired * avg_value_per_item
    money_saved = fresh * avg_value_per_item

    col1, col2 = st.columns(2)
    col1.metric("Estimated Waste Cost", f"${money_lost}")
    col2.metric("Potential Savings", f"${money_saved}")


if page == "Add Food":

    st.title("➕ Add Food")

    with st.form("add_food_form"):
        food = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)

        category = st.selectbox(
            "Category",
            ["Dairy", "Vegetables", "Fruit", "Meat", "Grains", "Other"]
        )

        expiration = st.date_input("Expiration Date")

        submitted = st.form_submit_button("Add Item")

    if submitted:
        new_item = pd.DataFrame({
            "Food": [food],
            "Quantity": [quantity],
            "Category": [category],
            "Expiration": [str(expiration)]
        })

        df = pd.concat([df, new_item], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success("Item added!")
        st.rerun()


if page == "Inventory":

    st.title("📦 Inventory")

    search = st.text_input("Search food")

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Food"].str.contains(search, case=False)
        ]

    st.write("## 📊 Inventory Data")

    if model is not None:

        st.write("## 🤖 AI Prediction")

        def get_ml_prediction(row):
            exp_date = datetime.datetime.strptime(row["Expiration"], "%Y-%m-%d").date()
            days_left = (exp_date - datetime.date.today()).days
            cat_encoded = encoder.transform([row["Category"]])[0]
            return model.predict([[days_left, cat_encoded]])[0]

        filtered_df["AI Prediction"] = filtered_df.apply(get_ml_prediction, axis=1)

        st.dataframe(filtered_df, use_container_width=True)

    else:
        st.dataframe(filtered_df, use_container_width=True)
        st.info("ML model not trained yet. Run ml_model.py first.")