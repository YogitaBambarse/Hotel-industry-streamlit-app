import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Hotel Industry Insights",
    page_icon="🍽️",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("zomato.csv")   # तुमचं dataset नाव
    return df

df = load_data()

# -----------------------------
# Basic Cleaning
# -----------------------------
df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")
df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📊 Dashboard Controls")

# City Filter
city_list = sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox(
    "🏙️ Select City",
    ["All"] + city_list
)

# Price Range (NO default selection)
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect(
    "💰 Price Range",
    price_list
)

# Cuisine (NO default selection)
cuisine_list = sorted(
    set(
        cuisine
        for cuisines in df["Cuisines"].dropna()
        for cuisine in cuisines.split(", ")
    )
)

selected_cuisine = st.sidebar.multiselect(
    "🍕 Cuisines",
    cuisine_list
)

st.sidebar.divider()

# Rating Filter
rating_range = st.sidebar.slider(
    "⭐ Rating Range",
    0.0, 5.0, (0.0, 5.0), step=0.1
)

# Online Delivery
delivery_option = st.sidebar.radio(
    "🚚 Online Delivery",
    ["All", "Yes", "No"]
)

# Votes Filter
min_votes = st.sidebar.number_input(
    "🗳️ Minimum Votes",
    min_value=0,
    value=0,
    step=10
)

st.sidebar.divider()

# Sort Option
sort_option = st.sidebar.selectbox(
    "🔽 Sort By",
    ["Aggregate rating", "Votes", "Price range"]
)

# Reset Button
if st.sidebar.button("🔄 Reset Filters"):
    st.experimental_rerun()

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_price:
    filtered_df = filtered_df[filtered_df["Price range"].isin(selected_price)]

if selected_cuisine:
    filtered_df = filtered_df[
        filtered_df["Cuisines"].str.contains("|".join(selected_cuisine), na=False)
    ]

filtered_df = filtered_df[
    (filtered_df["Aggregate rating"] >= rating_range[0]) &
    (filtered_df["Aggregate rating"] <= rating_range[1])
]

if delivery_option != "All":
    filtered_df = filtered_df[
        filtered_df["Has Online delivery"].str.lower() == delivery_option.lower()
    ]

filtered_df = filtered_df[filtered_df["Votes"] >= min_votes]

filtered_df = filtered_df.sort_values(sort_option, ascending=False)

# -----------------------------
# Main Title
# -----------------------------
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.caption("Professional Data Analytics Dashboard")

# -----------------------------
# No Data Message
# -----------------------------
if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters.")
else:
    # -----------------------------
    # KPIs
    # -----------------------------
    c1, c2, c3 = st.columns(3)

    c1.metric("📦 Total Restaurants", len(filtered_df))
    c2.metric("⭐ Avg Rating", round(filtered_df["Aggregate rating"].mean(), 2))
    c3.metric("🗳️ Avg Votes", int(filtered_df["Votes"].mean()))

    st.divider()

    # -----------------------------
    # Horizontal Bar Chart
    # -----------------------------
    top_restaurants = filtered_df.head(10)

    fig = px.bar(
        top_restaurants,
        x="Aggregate rating",
        y="Restaurant Name",
        orientation="h",
        title="🏆 Top 10 Restaurants by Rating",
        hover_data=["City", "Votes", "Price range"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -----------------------------
    # Data Table
    # -----------------------------
    st.subheader("📋 Restaurant Details")
    st.dataframe(
        filtered_df[
            ["Restaurant Name", "City", "Cuisines",
             "Price range", "Aggregate rating", "Votes",
             "Has Online delivery"]
        ]
    )