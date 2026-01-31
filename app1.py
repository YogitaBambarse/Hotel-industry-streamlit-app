import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.sidebar.header("🔍 Filters")
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(skipna=True), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum(skipna=True)))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.strip() == "Yes"].shape[0]
)

# Price Range Distribution
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
bars1 = ax1.bar(price_counts.index, price_counts.values, color='skyblue')
ax1.set_title("Restaurants by Price Range", fontsize=14)
ax1.set_xlabel("Price Range", fontsize=12)
ax1.set_ylabel("Number of Restaurants", fontsize=12)
ax1.set_xticks(price_counts.index)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height, str(height), ha='center', va='bottom')

st.pyplot(fig1)

# Top 10 Cuisines
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
bars2 = ax2.barh(top_cuisines.index[::-1], top_cuisines.values[::-1], color='lightgreen')
ax2.set_title("Top 10 Cuisines", fontsize=14)
ax2.set_xlabel("Number of Restaurants", fontsize=12)
ax2.set_ylabel("Cuisine Type", fontsize=12)

# Add value labels on bars
for bar in bars2:
    width = bar.get_width()
    ax2.text(width + 1, bar.get_y() + bar.get_height()/2, str(width), va='center')

st.pyplot(fig2)

# Dataset Preview
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))
