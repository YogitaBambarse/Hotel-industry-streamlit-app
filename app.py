import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")

# ================= DATA LOAD =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()  # कॉलम नामातील extra spaces काढणे
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

# शहर filter
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

# ================= FILTER DATA =================
if selected_city != "All":
    filtered_df = df[df["City"] == selected_city].copy()
else:
    filtered_df = df.copy()

# ================= HANDLE MISSING VALUES =================
filtered_df["Aggregate rating"] = filtered_df["Aggregate rating"].fillna(0)
filtered_df["Votes"] = filtered_df["Votes"].fillna(0)
filtered_df["Has Online delivery"] = filtered_df["Has Online delivery"].fillna("No")
filtered_df["Price range"] = filtered_df["Price range"].fillna("N/A")
filtered_df["Cuisines"] = filtered_df["Cuisines"].fillna("Unknown")

# ================= DOWNLOAD =================
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="hotel_filtered_data.csv"
)

# ================= DATA QUALITY =================
st.sidebar.subheader("🧹 Data Quality")
st.sidebar.write("Missing Ratings:", filtered_df["Aggregate rating"].isna().sum())

# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.strip().str.lower() == "yes"].shape[0]
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
    ax1.text(price_counts.index[i], v + 0.1, v, ha="center")
st.pyplot(fig1)

# ================= TOP CUISINES =================
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].str.split(", ").explode()
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

# ================= AVERAGE RATING BY PRICE RANGE =================
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

st.subheader("🏙️ City-wise Top Restaurant Ratings (Horizontal Bar)")

# Auto detect restaurant name column
name_col = None
for col in df.columns:
    if "restaurant" in col.lower() or "hotel" in col.lower() or "name" in col.lower():
        name_col = col
        break

if not name_col:
    st.warning("Dataset मध्ये restaurant/hotel name column सापडला नाही.")
else:
    # Filter by city
    if selected_city != "All":
        city_df = filtered_df[filtered_df["City"] == selected_city].copy()
    else:
        city_df = filtered_df.copy()

    # Drop rows with NaN in name or rating
    city_df = city_df[[name_col, "Aggregate rating"]].dropna()

    if city_df.empty:
        st.warning("Selected city मध्ये डेटा उपलब्ध नाही.")
    else:
        # Sort by rating
        city_df = city_df.sort_values("Aggregate rating", ascending=True)  # horizontal bars low -> high

        # Top N restaurants
        top_n = st.slider("Select Top Restaurants", 5, 20, 10)
        top_city_df = city_df.tail(top_n)  # tail because ascending sort

        # Horizontal Bar Graph
        fig, ax = plt.subplots(figsize=(10, top_n * 0.6))
        bars = ax.barh(top_city_df[name_col], top_city_df["Aggregate rating"], color="purple")
        ax.set_xlim(0, 5)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Restaurant Name")
        ax.set_title(f"Top {top_n} Restaurants in {selected_city}")

        # Add text on bars
        for bar in bars:
            width = bar.get_width()
            if width < 1:
                ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"{width:.2f}", va="center")
            else:
                ax.text(width - 0.2, bar.get_y() + bar.get_height()/2, f"{width:.2f}", va="center", color="white")

        plt.tight_layout()
        st.pyplot(fig)
# ================= AUTO INSIGHT =================
if not filtered_df['Price range'].dropna().empty:
    most_common_price = filtered_df['Price range'].mode()[0]
else:
    most_common_price = "N/A"

st.info(
    f"In {selected_city}, most restaurants fall in price range "
    f"{most_common_price} indicating mid-range dominance."
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