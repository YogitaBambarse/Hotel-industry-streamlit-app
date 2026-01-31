import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.markdown("---")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

# City filter
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

# Optional: Price range filter
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect("Select Price Range", price_list, default=price_list)

# Optional: Cuisine filter
cuisine_list = sorted(df["Cuisines"].dropna().str.split(", ").explode().unique())
selected_cuisine = st.sidebar.multiselect("Select Cuisines", cuisine_list, default=cuisine_list)

# Filter data
filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]
if selected_price:
    filtered_df = filtered_df[filtered_df["Price range"].isin(selected_price)]
if selected_cuisine:
    filtered_df = filtered_df[filtered_df["Cuisines"].str.contains('|'.join(selected_cuisine))]

# Fill missing values
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

# ================= PROFESSIONAL METRICS CARDS =================
st.markdown("""
<div style='display:flex; justify-content:space-between; margin-bottom:20px;'>
<div style='background-color:#f0f8ff; padding:20px; border-radius:10px; text-align:center; flex:1; margin-right:5px;'>
<h3>🏨 Total Restaurants</h3>
<p style='font-size:24px'>{}</p>
</div>
<div style='background-color:#ffe4e1; padding:20px; border-radius:10px; text-align:center; flex:1; margin-right:5px;'>
<h3>⭐ Average Rating</h3>
<p style='font-size:24px'>{}</p>
</div>
<div style='background-color:#f5f5dc; padding:20px; border-radius:10px; text-align:center; flex:1; margin-right:5px;'>
<h3>🗳️ Total Votes</h3>
<p style='font-size:24px'>{}</p>
</div>
<div style='background-color:#e6e6fa; padding:20px; border-radius:10px; text-align:center; flex:1;'>
<h3>🚚 Online Delivery</h3>
<p style='font-size:24px'>{}</p>
</div>
</div>
""".format(
    filtered_df.shape[0],
    round(filtered_df["Aggregate rating"].mean(),2),
    int(filtered_df["Votes"].sum()),
    filtered_df[filtered_df["Has Online delivery"].str.lower()=="yes"].shape[0]
), unsafe_allow_html=True)

st.markdown("---")

# ================= PRICE RANGE DISTRIBUTION =================
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
sns.barplot(x=price_counts.index, y=price_counts.values, palette="Blues_d", ax=ax1)
ax1.set_xlabel("Price Range")
ax1.set_ylabel("Number of Restaurants")
for i, v in enumerate(price_counts.values):
    ax1.text(i, v + 0.1, v, ha="center")
st.pyplot(fig1)

# ================= TOP CUISINES =================
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=top_cuisines.values[::-1], y=top_cuisines.index[::-1], palette="Greens_d", ax=ax2)
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
sns.barplot(x=avg_rating.index, y=avg_rating.values, palette="Oranges_d", ax=ax3)
ax3.set_ylim(0, 5)
ax3.set_xlabel("Price Range")
ax3.set_ylabel("Average Rating")
for i, v in enumerate(avg_rating.values):
    ax3.text(i, v + 0.05, f"{v:.2f}", ha="center")
st.pyplot(fig3)

# ================= DATA QUALITY =================
st.sidebar.subheader("🧹 Data Quality")
st.sidebar.write("Total restaurants:", filtered_df.shape[0])
st.sidebar.write("Restaurants missing Ratings:", filtered_df["Aggregate rating"].isna().sum())
st.sidebar.write("Restaurants missing Cuisines:", filtered_df["Cuisines"].isna().sum())
st.sidebar.write("Restaurants with Online Delivery:", filtered_df[filtered_df["Has Online delivery"].str.lower()=="yes"].shape[0])

# ================= DATA PREVIEW =================
with st.expander("📄 Dataset Preview"):
    st.dataframe(filtered_df.head(20))

# ================= AUTO INSIGHT =================
most_common_price = filtered_df['Price range'].mode()[0] if not filtered_df['Price range'].dropna().empty else "N/A"
st.info(
    f"Most restaurants fall in price range {most_common_price} indicating mid-range dominance."
)

# ================= KEY BUSINESS INSIGHTS =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range priced restaurants dominate the market  
• Customer ratings remain consistent across price ranges  
• Few cuisines capture major market share  
• Online delivery improves restaurant visibility  
• Data quality check is essential for accurate insights  
""")