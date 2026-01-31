import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Hotel Industry Insights",
    layout="wide"
)

# Title
st.title("🍽️ Hotel Industry Insights Through Data Analytics")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Dataset .csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

city_list = ["All"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)

c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"] == "Yes"].shape[0]
)

st.divider()

# ================= PRICE RANGE =================
st.subheader("💰 Price Range Distribution")

price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(price_counts.index, price_counts.values)
ax1.set_xlabel("Price Range")
ax1.set_ylabel("Number of Restaurants")
st.pyplot(fig1)

# ================= TOP CUISINES =================
st.subheader("🍕 Top 10 Cuisines")

cuisines = filtered_df["Cuisines"].dropna().str.split(", ")
cuisine_list = cuisines.explode()
top_cuisines = cuisine_list.value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_cuisines.index, top_cuisines.values)
ax2.set_xlabel("Count")
st.pyplot(fig2)

# ================= ONLINE DELIVERY VS RATING =================
st.subheader("🚚 Online Delivery vs Average Rating")

delivery_rating = (
    filtered_df.groupby("Has Online delivery")["Aggregate rating"]
    .mean()
)

fig3, ax3 = plt.subplots()
ax3.bar(delivery_rating.index, delivery_rating.values)
ax3.set_ylabel("Average Rating")
st.pyplot(fig3)

# ================= DATA PREVIEW =================
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))
