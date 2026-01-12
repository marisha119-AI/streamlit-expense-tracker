import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Smart Expense Tracker")
st.write("Track your daily expenses and analyze your spending.")

# ---------------- FILE SETUP ----------------
FILE_NAME = "expenses.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)

# ---------------- ADD EXPENSE ----------------
st.subheader("➕ Add New Expense")

expense_date = st.date_input("Date", date.today())
category = st.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)
amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
note = st.text_input("Note (optional)")

if st.button("Add Expense"):
    new_data = {
        "Date": expense_date,
        "Category": category,
        "Amount": amount,
        "Note": note
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.success("Expense added successfully!")

# ---------------- DASHBOARD ----------------
st.subheader("📊 Expense Dashboard")

total_expense = df["Amount"].sum()
st.metric("Total Expense (₹)", total_expense)

st.write("### Category-wise Expense")
category_summary = df.groupby("Category")["Amount"].sum()
st.bar_chart(category_summary)

st.write("### All Expenses")
st.dataframe(df)
st.download_button(
    label="Download Expense Data as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='expenses.csv',
    mime='text/csv',
)
st.write("Developed by Your Marisha")
