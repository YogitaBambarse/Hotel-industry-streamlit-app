import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()

    df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")
    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")

    def rating_category(r):
        if r >= 4.5:
            return "Excellent"
        elif r >= 3.5:
            return "Good"
        else:
            return "Average"

    df["Rating Category"] = df["Aggregate rating"].apply(rating_category)
    return df
