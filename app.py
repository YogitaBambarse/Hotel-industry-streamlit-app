import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Hotel Industry Insights", layout="wide")
st.title("🍽️ Hotel Industry Insights Through Data Analytics")
st.markdown("Professional & Interactive Business Dashboard")
st.divider()

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ================= SIDEBAR =================
st.sidebar.title("📊 Dashboard Controls")

# ---- City Filter ----
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("🏙️ Select City", city_list)

# ---- Price Range Filter ----
price_list = sorted(df["Price range"].dropna().unique())
selected_price = st.sidebar.multiselect(
    "💰 Price Range",
    price_list,
    default=price_list
)

# ---- Cuisine Filter ----
cuisine_list = sorted(
    df["Cuisines"].dropna().str.split(", ").explode().unique()
)
selected_cuisine = st.sidebar.multiselect(
    "🍕 Cuisines",
    cuisine_list,
    default=cuisine_list
)

st.sidebar.divider()

# ---- Rating Range ----
rating_range = st.sidebar.slider(
    "⭐ Rating Range",
    0.0, 5.0, (0.0, 5.0), step=0.1
)

# ---- Online Delivery ----
delivery_option = st.sidebar.radio(
    "🚚 Online Delivery",
    ["All", "Online Delivery Only", "No Online Delivery"]
)

# ---- Minimum Votes ----
min_votes = st.sidebar.number_input(
    "🗳️ Minimum Votes",
    min_value=0,
    value=0,
    step=10
)

st.sidebar.divider()

# ---- Sort Option ----
sort_option = st.sidebar.selectbox(
    "🔽 Sort By",
    ["Aggregate rating", "Votes", "Price range"]
)

# ---- Reset Button ----
if st.sidebar.button("🔄 Reset Filters"):
    st.experimental_rerun()

# ================= FILTERING =================
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

if delivery_option == "Online Delivery Only":
    filtered_df = filtered_df[
        filtered_df["Has Online delivery"].str.lower() == "yes"
    ]
elif delivery_option == "No Online Delivery":
    filtered_df = filtered_df[
        filtered_df["Has Online delivery"].str.lower() == "no"
    ]

filtered_df = filtered_df[filtered_df["Votes"] >= min_votes]

filtered_df = filtered_df.sort_values(sort_option, ascending=False)

# ================= DOWNLOAD =================
st.sidebar.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="hotel_filtered_data.csv"
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

# ================= TOP CUISINES =================
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
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_pie, use_container_width=True)

# ================= AVERAGE RATING BY PRICE =================
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

# ================= INSIGHTS =================
most_common_price = filtered_df["Price range"].mode()[0]
st.info(
    f"Most restaurants fall in price range {most_common_price}, showing mid-range market dominance."
)

st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range restaurants dominate the market  
• Higher votes increase rating reliability  
• Few cuisines capture major demand  
• Online delivery boosts visibility  
• Filters help in better decision making  
""")