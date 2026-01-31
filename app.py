import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= LOGIN SYSTEM =================
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Hotel Industry Insights Dashboard</p>", unsafe_allow_html=True)

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()

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
logout_button()

city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

search = st.sidebar.text_input("🔎 Search Restaurant")

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# ================= METRICS =================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Avg Rating", round(filtered_df["Aggregate rating"].mean(), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum()))
c4.metric("🚚 Online Delivery",
          filtered_df[filtered_df["Has Online delivery"].str.strip() == "Yes"].shape[0])

# ================= DOWNLOAD =================
st.sidebar.download_button(
    "⬇️ Download Data",
    filtered_df.to_csv(index=False),
    file_name="hotel_analysis.csv"
)

# ================= SEARCH =================
if search:
    st.subheader("🔎 Search Result")
    st.dataframe(filtered_df[filtered_df.iloc[:,0].str.contains(search, case=False, na=False)])

st.divider()

# ================= PRICE RANGE GRAPH =================
st.subheader("💰 Price Range Distribution")
price_counts = filtered_df["Price range"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.bar(price_counts.index, price_counts.values)
ax.set_xlabel("Price Range")
ax.set_ylabel("Restaurants")
for i, v in enumerate(price_counts.values):
    ax.text(price_counts.index[i], v, v, ha='center')
st.pyplot(fig)

# ================= CUISINES =================
st.subheader("🍕 Top 10 Cuisines")
cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
top_cuisines = cuisines.value_counts().head(10)

fig, ax = plt.subplots()
ax.barh(top_cuisines.index[::-1], top_cuisines.values[::-1])
st.pyplot(fig)

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

# ================= AVG RATING =================
st.subheader("⭐ Average Rating by Price Range")
avg = filtered_df.groupby("Price range")["Aggregate rating"].mean()

fig, ax = plt.subplots()
ax.bar(avg.index, avg.values)
ax.set_ylim(0,5)
for i,v in enumerate(avg.values):
    ax.text(avg.index[i], v+0.05, f"{v:.2f}", ha='center')
st.pyplot(fig)

# ================= CITY-WISE RESTAURANTS =================
st.subheader("🏙️ City-wise Restaurant Ratings")

if selected_city != "All":
    city_df = filtered_df.sort_values("Aggregate rating", ascending=False)

    # Restaurant name column auto-detect
    name_col = None
    for c in city_df.columns:
        if "restaurant" in c.lower() or "hotel" in c.lower():
            name_col = c
            break

    if name_col:
        top_n = st.slider("Select Top Restaurants", 5, 20, 10)

        top_city_df = city_df.head(top_n)

        fig, ax = plt.subplots(figsize=(10, top_n * 0.5))
        bars = ax.barh(
            top_city_df[name_col][::-1],
            top_city_df["Aggregate rating"][::-1],
            color="skyblue"
        )

        ax.set_xlabel("Rating")
        ax.set_ylabel("Restaurant Name")
        ax.set_xlim(0, 5)
        ax.set_title(f"Top {top_n} Restaurants in {selected_city}")

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
                    f"{w:.2f}", va='center')

        st.pyplot(fig)
else:
    st.info("Please select a city to view restaurant-wise ratings.")
# ================= AUTO INSIGHT =================
st.info(
    f"In {selected_city}, most restaurants fall in price range "
    f"{filtered_df['Price range'].mode()[0]} indicating mid-range dominance."
)

# ================= DATA QUALITY =================
st.sidebar.write("🧹 Data Quality")
st.sidebar.write("Missing Ratings:", filtered_df["Aggregate rating"].isna().sum())

# ================= DATA PREVIEW =================
with st.expander("📄 Dataset Preview"):
    st.dataframe(filtered_df.head(20))

# ================= CONCLUSION =================
st.subheader("📌 Key Business Insights")
st.markdown("""
• Mid-range priced restaurants dominate the market  
• Ratings are consistent across price ranges  
• Few cuisines capture most market share  
• Strong competition among top restaurants  
• Online delivery improves visibility  
""")