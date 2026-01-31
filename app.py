import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Hotel Industry Insights",
    page_icon="🍽️",
    layout="wide"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ================= BASIC CLEANING =================
df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")
df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")

# ================= RATING CATEGORY =================
def rating_category(r):
    if r >= 4.5:
        return "Excellent"
    elif r >= 3.5:
        return "Good"
    else:
        return "Average"

df["Rating Category"] = df["Aggregate rating"].apply(rating_category)

# ================= SIDEBAR =================
st.sidebar.title("📊 Dashboard Filters")

# City
city_list = sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("🏙️ Select City", ["All"] + city_list)

# Price Range
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect("💰 Price Range", price_list)

# ================= CUISINE (Top 10 Default Selected) =================
all_cuisines = (
    df["Cuisines"]
    .dropna()
    .str.split(", ")
    .explode()
)

top_10_cuisines = all_cuisines.value_counts().head(10).index.tolist()
cuisine_list = sorted(all_cuisines.unique())

selected_cuisine = st.sidebar.multiselect(
    "🍕 Select Cuisines",
    cuisine_list,
    default=top_10_cuisines
)

# Rating Range
rating_range = st.sidebar.slider(
    "⭐ Rating Range", 0.0, 5.0, (0.0, 5.0), step=0.1
)

# Online Delivery
delivery_option = st.sidebar.radio(
    "🚚 Online Delivery", ["All", "Yes", "No"]
)

# Votes
min_votes = st.sidebar.number_input(
    "🗳️ Minimum Votes", min_value=0, value=0, step=10
)

# ================= APPLY FILTERS =================
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

# ================= MAIN TITLE =================
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.caption("Professional Streamlit Dashboard with Rating Classification")

# ================= EMPTY CHECK =================
if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters.")
else:
    # ================= METRICS =================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🏨 Total Restaurants", len(filtered_df))
    c2.metric("⭐ Avg Rating", round(filtered_df["Aggregate rating"].mean(), 2))
    c3.metric("🗳️ Avg Votes", int(filtered_df["Votes"].mean()))
    c4.metric(
        "🚚 Online Delivery",
        filtered_df[filtered_df["Has Online delivery"].str.lower() == "yes"].shape[0]
    )

    st.divider()

    # ================= RATING CATEGORY BAR =================
    st.subheader("⭐ Rating Category Distribution")

    rating_fig = px.bar(
        filtered_df["Rating Category"].value_counts().reindex(
            ["Excellent", "Good", "Average"]
        ),
        labels={"index": "Rating Category", "value": "Number of Restaurants"},
        color=["Excellent", "Good", "Average"]
    )

    st.plotly_chart(rating_fig, use_container_width=True)

    st.divider()

    # ================= TOP 10 RESTAURANTS =================
    st.subheader("🏆 Top 10 Restaurants by Rating")

    top_restaurants = filtered_df.sort_values(
        "Aggregate rating", ascending=False
    ).head(10)

    fig = px.bar(
        top_restaurants,
        x="Aggregate rating",
        y="Restaurant Name",
        orientation="h",
        color="Aggregate rating",
        hover_data=["City", "Votes", "Price range"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ================= DATA TABLE =================
    st.subheader("📋 Restaurant Dataset")
    st.dataframe(
        filtered_df[
            [
                "Restaurant Name",
                "City",
                "Cuisines",
                "Price range",
                "Aggregate rating",
                "Rating Category",
                "Votes",
                "Has Online delivery",
            ]
        ]
    )

# ================= CONCLUSION =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Excellent rated restaurants attract higher customer engagement  
• Majority restaurants fall under Good and Average categories  
• Rating classification helps in better decision making  
• Cuisine popularity directly impacts restaurant success  
• Data-driven insights improve business strategies  
""")