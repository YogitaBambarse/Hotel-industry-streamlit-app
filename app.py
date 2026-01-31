import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hotel Industry Insights",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🍽️ Hotel Industry Insights: A Data-Driven Market Analysis")
st.caption("Exploratory Data Analysis of Restaurant Industry using Real-World Data")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("Dataset.csv")

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filter Options")

city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# ---------------- KPI METRICS ----------------
st.markdown("## 📊 Market Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏨 Total Active Restaurants", filtered_df.shape[0])
c2.metric(
    "⭐ Overall Customer Satisfaction",
    round(filtered_df["Aggregate rating"].mean(), 2)
)
c3.metric(
    "🗳️ Total Customer Engagement",
    int(filtered_df["Votes"].sum())
)
c4.metric(
    "🚚 Online Delivery Adoption",
    filtered_df[filtered_df["Has Online delivery"] == "Yes"].shape[0]
)

# ---------------- PRICE RANGE ----------------
st.markdown("## 💰 Price Range Distribution")

price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(price_counts.index, price_counts.values)
ax1.set_xlabel("Price Range")
ax1.set_ylabel("Number of Restaurants")
ax1.set_title("Distribution of Restaurants by Price Range")

st.pyplot(fig1)

st.info(
    "Insight: Majority of restaurants fall under mid-price categories, indicating strong customer preference for affordable dining options."
)

# ---------------- CUISINES ----------------
st.markdown("## 🍽️ Customer Preference Analysis (Top Cuisines)")

cuisines = (
    filtered_df["Cuisines"]
    .dropna()
    .str.split(", ")
    .explode()
)

top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_cuisines.index, top_cuisines.values)
ax2.set_xlabel("Number of Restaurants")
ax2.set_ylabel("Cuisine Type")
ax2.set_title("Top 10 Most Popular Cuisines")

st.pyplot(fig2)

st.info(
    "Insight: A limited set of cuisines dominates the market, reflecting concentrated customer taste preferences."
)

# ---------------- AVERAGE RATING GRAPH ----------------
st.markdown("## ⭐ Rating Performance Overview")

rating_df = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig3, ax3 = plt.subplots()
bars = ax3.bar(rating_df.index, rating_df.values)

ax3.set_xlabel("Price Range")
ax3.set_ylabel("Average Rating")
ax3.set_title("Average Rating by Price Range")

for bar in bars:
    height = bar.get_height()
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}",
        ha="center",
        va="bottom"
    )

st.pyplot(fig3)

st.info(
    "Insight: Customer satisfaction remains relatively stable across price categories, suggesting quality is not strictly price-dependent."
)

# ---------------- CITY WISE RESTAURANTS ----------------
st.markdown("## 🏨 City-wise Top Rated Restaurants")

city_df = filtered_df[
    ["Restaurant Name", "Aggregate rating"]
].dropna()

city_df = city_df.sort_values(
    by="Aggregate rating",
    ascending=False
).head(15)

fig4, ax4 = plt.subplots(figsize=(8, 6))
bars4 = ax4.barh(
    city_df["Restaurant Name"],
    city_df["Aggregate rating"]
)

ax4.set_xlabel("Aggregate Rating")
ax4.set_ylabel("Restaurant Name")
ax4.set_title("Top Rated Restaurants (Selected City)")
ax4.invert_yaxis()

for bar in bars4:
    width = bar.get_width()
    ax4.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.1f}",
        va="center"
    )

st.pyplot(fig4)

st.info(
    "Insight: The chart highlights competitive leaders within the selected city based on customer ratings."
)

# ---------------- DATA PREVIEW ----------------
st.markdown("## 📄 Dataset Preview")
st.dataframe(filtered_df.head(20))

# ---------------- CONCLUSION ----------------
st.markdown("## 📝 Key Business Insights & Conclusion")

st.success("""
• Mid-range priced restaurants dominate the market  
• Customer ratings are consistent across price ranges  
• A small set of cuisines captures major market share  
• City-wise analysis reveals strong competition among top-rated restaurants  
• Online delivery significantly enhances restaurant visibility  
""")