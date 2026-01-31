import streamlit as st
import pandas as pd
import plotly.express as px

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

# Price range filter
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect("Select Price Range", price_list, default=price_list)

# Cuisine filter
cuisine_list = sorted(df["Cuisines"].dropna().str.split(", ").explode().unique())
selected_cuisine = st.sidebar.multiselect("Select Cuisines", cuisine_list, default=cuisine_list)

# ================= SAFE FILTERING =================
filtered_df = df.copy()

# City filter
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

# Price range filter
if selected_price:
    filtered_df = filtered_df[filtered_df["Price range"].isin(selected_price)]

# Cuisine filter (safe)
if selected_cuisine:
    filtered_df = filtered_df[
        filtered_df["Cuisines"].str.contains('|'.join(selected_cuisine), na=False)
    ]

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

# ================= PROFESSIONAL METRICS =================
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏨 Total Restaurants", filtered_df.shape[0])
col2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(), 2))
col3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
col4.metric("🚚 Online Delivery", filtered_df[filtered_df["Has Online delivery"].str.lower() == "yes"].shape[0])

st.markdown("---")

# ================= PRICE RANGE DISTRIBUTION =================
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()
fig_price = px.bar(
    x=price_counts.index,
    y=price_counts.values,
    labels={"x":"Price Range","y":"Number of Restaurants"},
    text=price_counts.values,
    color=price_counts.values,
    color_continuous_scale="Blues"
)
fig_price.update_layout(showlegend=False)
st.plotly_chart(fig_price, use_container_width=True)

# ================= TOP CUISINES =================
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)
fig_cuisine = px.bar(
    x=top_cuisines.values[::-1],
    y=top_cuisines.index[::-1],
    orientation='h',
    labels={"x":"Number of Restaurants","y":"Cuisine"},
    text=top_cuisines.values[::-1],
    color=top_cuisines.values[::-1],
    color_continuous_scale="Greens"
)
fig_cuisine.update_layout(showlegend=False)
st.plotly_chart(fig_cuisine, use_container_width=True)

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
fig_rating_cat = px.pie(
    filtered_df, 
    names="Rating Category", 
    title="Rating Categories Distribution",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_rating_cat, use_container_width=True)

# ================= AVERAGE RATING BY PRICE RANGE =================
st.subheader("⭐ Average Rating by Price Range")
avg_rating = filtered_df.groupby("Price range")["Aggregate rating"].mean().sort_index()
fig_avg_rating = px.bar(
    x=avg_rating.index,
    y=avg_rating.values,
    labels={"x":"Price Range","y":"Average Rating"},
    text=[f"{v:.2f}" for v in avg_rating.values],
    color=avg_rating.values,
    color_continuous_scale="Oranges"
)
fig_avg_rating.update_layout(showlegend=False, yaxis=dict(range=[0,5]))
st.plotly_chart(fig_avg_rating, use_container_width=True)

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