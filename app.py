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

# ---------------- Average Rating Standalone ----------------
st.subheader("⭐ Average Rating by Price Range")
avg_ratings = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(avg_ratings.index, avg_ratings.values, color='orange')

ax.set_xlabel("Price Range", fontsize=12)
ax.set_ylabel("Average Rating", fontsize=12)
ax.set_title("Average Rating of Restaurants by Price Range", fontsize=14)
ax.set_ylim(0, 5)  # Ratings scale 0-5

# Add rating labels above bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.05, f"{height:.2f}", 
            ha='center', va='bottom', color='red', fontweight='bold')

st.pyplot(fig)

# ---------------- Dataset Preview ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))