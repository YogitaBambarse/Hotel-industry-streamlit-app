import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.markdown("Professional Dashboard for Restaurant Data Analysis")
st.divider()

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ================= SIDEBAR FILTERS =================
st.sidebar.header("🔍 Filters")

# City
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

# Price Range
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect(
    "Select Price Range",
    price_list,
    default=price_list
)

# Cuisines
cuisine_list = sorted(
    df["Cuisines"].dropna().str.split(", ").explode().unique()
)
selected_cuisine = st.sidebar.multiselect(
    "Select Cuisines",
    cuisine_list,
    default=cuisine_list
)

# ================= FILTERING (SAFE) =================
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_price:
    filtered_df = filtered_df[filtered_df["Price range"].isin(selected_price)]

if selected_cuisine:
    filtered_df = filtered_df[
        filtered_df["Cuisines"].str.contains("|".join(selected_cuisine), na=False)
    ]

# Fill missing values
filtered_df["Aggregate rating"] = filtered_df["Aggregate rating"].fillna(0)
filtered_df["Votes"] = filtered_df["Votes"].fillna(0)
filtered_df["Has Online delivery"] = filtered_df["Has Online delivery"].fillna("No")

# ================= DOWNLOAD =================
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_hotel_data.csv"
)

# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.lower() == "yes"].shape[0]
)

st.divider()

# ================= PRICE RANGE DISTRIBUTION =================
st.subheader("💰 Price Range Distribution")

price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
sns.barplot(
    x=price_counts.index,
    y=price_counts.values,
    ax=ax1
)
ax1.set_xlabel("Price Range")
ax1.set_ylabel("Number of Restaurants")

for i, v in enumerate(price_counts.values):
    ax1.text(i, v, v, ha="center", va="bottom")

st.pyplot(fig1)

# ================= TOP CUISINES (HORIZONTAL BAR) =================
st.subheader("🍕 Top 10 Cuisines")

cuisines = filtered_df["Cuisines"].str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(
    x=top_cuisines.values,
    y=top_cuisines.index,
    ax=ax2
)
ax2.set_xlabel("Number of Restaurants")
ax2.set_ylabel("Cuisine")

st.pyplot(fig2)

# ================= RATING CATEGORY =================
st.subheader("⭐ Rating Categories")

def rating_category(r):
    if r >= 4.5:
        return "Excellent"
    elif r >= 3.5:
        return "Good"
    else:
        return "Average"

filtered_df["Rating Category"] = filtered_df["Aggregate rating"].apply(rating_category)
st.bar_chart(filtered_df["Rating Category"].value_counts())

# ================= AVERAGE RATING BY PRICE RANGE =================
st.subheader("⭐ Average Rating by Price Range")

avg_rating = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig3, ax3 = plt.subplots()
sns.barplot(
    x=avg_rating.index,
    y=avg_rating.values,
    ax=ax3
)
ax3.set_ylim(0, 5)
ax3.set_xlabel("Price Range")
ax3.set_ylabel("Average Rating")

for i, v in enumerate(avg_rating.values):
    ax3.text(i, v + 0.05, f"{v:.2f}", ha="center")

st.pyplot(fig3)

# ================= DATA QUALITY =================
st.sidebar.subheader("🧹 Data Quality")
st.sidebar.write("Missing Ratings:", df["Aggregate rating"].isna().sum())
st.sidebar.write("Missing Cuisines:", df["Cuisines"].isna().sum())

# ================= DATA PREVIEW =================
with st.expander("📄 Dataset Preview"):
    st.dataframe(filtered_df.head(20))

# ================= AUTO INSIGHT =================
most_common_price = filtered_df["Price range"].mode()[0]
st.info(
    f"Most restaurants fall under price range {most_common_price}, indicating mid-range dominance."
)

# ================= CONCLUSION =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range restaurants dominate the market  
• Ratings are fairly consistent across price ranges  
• Few cuisines capture majority of customer interest  
• Online delivery increases restaurant reach  
• Data quality checks improve analysis reliability  
""")