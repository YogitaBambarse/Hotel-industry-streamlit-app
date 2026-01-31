import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.markdown("Interactive & Professional Business Dashboard")
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

# City filter
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

# Price Range filter
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect(
    "Select Price Range",
    price_list,
    default=price_list
)

# Cuisine filter
cuisine_list = sorted(
    df["Cuisines"].dropna().str.split(", ").explode().unique()
)
selected_cuisine = st.sidebar.multiselect(
    "Select Cuisines",
    cuisine_list,
    default=cuisine_list
)

# ================= SAFE FILTERING =================
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
fig_price = px.bar(
    x=price_counts.index,
    y=price_counts.values,
    text=price_counts.values,
    labels={"x": "Price Range", "y": "Number of Restaurants"},
    color=price_counts.values,
    color_continuous_scale="Blues"
)
fig_price.update_layout(showlegend=False)
st.plotly_chart(fig_price, use_container_width=True)

# ================= TOP CUISINES (HORIZONTAL BAR) =================
st.subheader("🍕 Top 10 Cuisines")

cuisines = filtered_df["Cuisines"].str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig_cuisine = px.bar(
    x=top_cuisines.values[::-1],
    y=top_cuisines.index[::-1],
    orientation="h",
    text=top_cuisines.values[::-1],
    labels={"x": "Number of Restaurants", "y": "Cuisine"},
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

fig_pie = px.pie(
    filtered_df,
    names="Rating Category",
    title="Rating Distribution",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_pie, use_container_width=True)

# ================= AVERAGE RATING BY PRICE RANGE =================
st.subheader("⭐ Average Rating by Price Range")

avg_rating = filtered_df.groupby("Price range")["Aggregate rating"].mean().sort_index()

fig_avg = px.bar(
    x=avg_rating.index,
    y=avg_rating.values,
    text=[f"{v:.2f}" for v in avg_rating.values],
    labels={"x": "Price Range", "y": "Average Rating"},
    color=avg_rating.values,
    color_continuous_scale="Oranges"
)
fig_avg.update_layout(yaxis=dict(range=[0, 5]), showlegend=False)
st.plotly_chart(fig_avg, use_container_width=True)

# ================= DATA PREVIEW =================
with st.expander("📄 Dataset Preview"):
    st.dataframe(filtered_df.head(20))

# ================= AUTO INSIGHT =================
most_common_price = filtered_df["Price range"].mode()[0]
st.info(
    f"Most restaurants belong to price range {most_common_price}, indicating strong mid-range market dominance."
)

# ================= CONCLUSION =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range restaurants dominate the market  
• Customer ratings remain stable across price ranges  
• Limited cuisines capture majority market share  
• Online delivery enhances customer reach  
• Interactive dashboards support better business decisions  
""")