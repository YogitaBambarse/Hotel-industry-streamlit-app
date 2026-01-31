import streamlit as st

def apply_filters(df):
    st.sidebar.title("📊 Dashboard Filters")

    # City
    city_list = sorted(df["City"].dropna().unique())
    selected_city = st.sidebar.selectbox("🏙️ Select City", ["All"] + city_list)

    # Price Range
    price_list = sorted(df["Price range"].dropna().unique())
    selected_price = st.sidebar.multiselect("💰 Price Range", price_list)

    # Cuisine
    all_cuisines = df["Cuisines"].dropna().str.split(", ").explode()
    top_10 = all_cuisines.value_counts().head(10).index.tolist()

    selected_cuisine = st.sidebar.multiselect(
        "🍕 Select Cuisines",
        sorted(all_cuisines.unique()),
        default=top_10
    )

    rating_range = st.sidebar.slider("⭐ Rating Range", 0.0, 5.0, (0.0, 5.0), 0.1)
    delivery_option = st.sidebar.radio("🚚 Online Delivery", ["All", "Yes", "No"])
    min_votes = st.sidebar.number_input("🗳️ Minimum Votes", 0, value=0, step=10)

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

    return filtered_df
