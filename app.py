import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

# Restaurant name column auto-detect
name_col = None
for col in df.columns:
    if "restaurant" in col.lower() or "hotel" in col.lower():
        name_col = col
        break

st.sidebar.subheader("🔎 Search Restaurant")
search = st.sidebar.text_input("Type restaurant name")

# ================= FILTER DATA =================
if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# ================= DOWNLOAD =================
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="hotel_filtered_data.csv"
)

# ================= DATA QUALITY =================
st.sidebar.subheader("🧹 Data Quality")
st.sidebar.write("Missing Ratings:", filtered_df["Aggregate rating"].isna().sum())

# ================= SEARCH RESULT =================
if search and name_col:
    st.subheader("🔍 Search Results")

    result_df = filtered_df[
        filtered_df[name_col]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

    if result_df.empty:
        st.warning("No restaurant found")
    else:
        st.dataframe(result_df)
# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.strip() == "Yes"].shape[0]
)

st.divider()

# ================= PRICE RANGE DISTRIBUTION =================
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(price_counts.index, price_counts.values, color="skyblue")
ax1.set_xlabel("Price Range")
ax1.set_ylabel("Number of Restaurants")

for i, v in enumerate(price_counts.values):
    ax1.text(price_counts.index[i], v, v, ha="center")

st.pyplot(fig1)

# ================= TOP CUISINES =================
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_cuisines.index[::-1], top_cuisines.values[::-1], color="lightgreen")
ax2.set_xlabel("Number of Restaurants")
st.pyplot(fig2)

# ================= RATING CATEGORY =================
def rating_category(r):
    if r >= 4.5:
        return "Excellent"
    elif r >= 3.5:
        return "Good"
    else:
        return "Average"

filtered_df["Rating Category"] = filtered_df["Aggregate rating"].apply(rating_category)

st.subheader("⭐ Rating Categories")
st.bar_chart(filtered_df["Rating Category"].value_counts())

# ================= AVERAGE RATING GRAPH =================
st.subheader("⭐ Average Rating by Price Range")
avg_rating = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig3, ax3 = plt.subplots()
ax3.bar(avg_rating.index, avg_rating.values, color="orange")
ax3.set_ylim(0, 5)
ax3.set_xlabel("Price Range")
ax3.set_ylabel("Average Rating")

for i, v in enumerate(avg_rating.values):
    ax3.text(avg_rating.index[i], v + 0.05, f"{v:.2f}", ha="center")

st.pyplot(fig3)

# ================= CITY-WISE RESTAURANT NAMES =================
st.subheader("🏙️ City-wise Restaurant Ratings")

if selected_city != "All" and name_col:
    city_df = filtered_df.sort_values("Aggregate rating", ascending=False)

    top_n = st.slider("Select Top Restaurants", 5, 20, 10)

    top_city_df = city_df.head(top_n)

    fig4, ax4 = plt.subplots(figsize=(10, top_n * 0.5))
    bars = ax4.barh(
        top_city_df[name_col][::-1],
        top_city_df["Aggregate rating"][::-1],
        color="purple"
    )

    ax4.set_xlim(0, 5)
    ax4.set_xlabel("Rating")
    ax4.set_ylabel("Restaurant Name")

    for bar in bars:
        w = bar.get_width()
        ax4.text(w + 0.05, bar.get_y() + bar.get_height()/2,
                 f"{w:.2f}", va="center")

    st.pyplot(fig4)
else:
    st.info("Please select a city to view restaurant-wise ratings.")

# ================= AUTO INSIGHT =================
st.info(
    f"In {selected_city}, most restaurants fall in price range "
    f"{filtered_df['Price range'].mode()[0]} indicating mid-range dominance."
)

# ================= DATA PREVIEW =================
with st.expander("📄 Dataset Preview"):
    st.dataframe(filtered_df.head(20))

# ================= CONCLUSION =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range priced restaurants dominate the market  
• Customer ratings remain consistent across price ranges  
• Few cuisines capture major market share  
• City-wise analysis shows strong competition  
• Online delivery improves restaurant visibility  
""")