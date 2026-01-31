import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Hotel Industry Insights",
    layout="wide"
)

st.title("🍽️ Hotel Industry Insights Through Data Analytics")

@st.cache_data
def load_data():
    return pd.read_csv("Dataset.csv")

df = load_data()

st.sidebar.header("🔍 Filters")

city_list = ["All"] + sorted(df["City"].unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"] == "Yes"].shape[0]
)

st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(price_counts.index, price_counts.values)
st.pyplot(fig1)

st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_cuisines.index, top_cuisines.values)
st.pyplot(fig2)

st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))
