import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()  # Remove extra spaces
    return df

df = load_data()

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔍 Filters")
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# ---------------- Metrics ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(skipna=True), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum(skipna=True)))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.strip() == "Yes"].shape[0]
)

# ---------------- Price Range Distribution ----------------
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots(figsize=(8,5))
bars1 = ax1.bar(price_counts.index, price_counts.values, color='skyblue')
ax1.set_title("Restaurants by Price Range", fontsize=14)
ax1.set_xlabel("Price Range", fontsize=12)
ax1.set_ylabel("Number of Restaurants", fontsize=12)
ax1.set_xticks(price_counts.index)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height, str(height), ha='center', va='bottom', color='blue', fontweight='bold')

st.pyplot(fig1)

# ---------------- Top 10 Cuisines ----------------
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(8,5))
bars2 = ax2.barh(top_cuisines.index[::-1], top_cuisines.values[::-1], color='lightgreen')
ax2.set_title("Top 10 Cuisines", fontsize=14)
ax2.set_xlabel("Number of Restaurants", fontsize=12)
ax2.set_ylabel("Cuisine Type", fontsize=12)

# Add value labels on bars
for bar in bars2:
    width = bar.get_width()
    ax2.text(width + 1, bar.get_y() + bar.get_height()/2, str(width), va='center', color='green', fontweight='bold')

st.pyplot(fig2)

# ---------------- Average Rating Standalone ----------------
st.subheader("⭐ Average Rating by Price Range")
avg_ratings = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig3, ax3 = plt.subplots(figsize=(8,5))
bars3 = ax3.bar(avg_ratings.index, avg_ratings.values, color='orange')

ax3.set_xlabel("Price Range", fontsize=12)
ax3.set_ylabel("Average Rating", fontsize=12)
ax3.set_title("Average Rating of Restaurants by Price Range", fontsize=14)
ax3.set_ylim(0, 5)  # Ratings scale 0-5

# Add rating labels above bars
for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height + 0.05, f"{height:.2f}", 
             ha='center', va='bottom', color='red', fontweight='bold')

st.pyplot(fig3)

# ---------------- Dataset Preview ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))