import plotly.express as px

def rating_category_chart(df):
    return px.bar(
        df["Rating Category"].value_counts().reindex(
            ["Excellent", "Good", "Average"]
        ),
        labels={"index": "Rating Category", "value": "Restaurants"}
    )

def cuisine_chart(df):
    cuisine_count = (
        df["Cuisines"].dropna()
        .str.split(", ").explode()
        .value_counts().head(10).sort_values()
    )
    return px.bar(
        cuisine_count,
        orientation="h",
        labels={"value": "Restaurants", "index": "Cuisine"}
    )

def top_restaurants_chart(df):
    top = df.sort_values("Aggregate rating", ascending=False).head(10)
    return px.bar(
        top,
        x="Aggregate rating",
        y="Restaurant Name",
        orientation="h",
        hover_data=["City", "Votes", "Price range"]
    )
