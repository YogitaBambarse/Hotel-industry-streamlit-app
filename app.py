import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Hotel Industry Insights Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ---------------- Title ----------------
st.markdown(
    "<h1 style='text-align: center;'>🍽️ Hotel Industry Insights Through Data Analytics</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: grey;'>Professional Data Analytics Dashboard for Restaurant Business Insights</p>",
    unsafe_allow_html=True
)

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("🔍 Filter Options")
city_list = ["All"] + sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select City", city_list)

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df
# ---------------- LOGOUT ----------------
def logout_button():
    st.sidebar.markdown("### 👤 User")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:grey;'>Hotel Industry Insights Dashboard</p>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")


# ---------------- LOGOUT ----------------
def logout_button():
    st.sidebar.markdown("### 👤 User")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# ---------------- SESSION CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()
# ====================== OVERVIEW ======================
st.markdown("## 📊 Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏨 Total Restaurants", filtered_df.shape[0])
c2.metric("⭐ Average Rating", round(filtered_df["Aggregate rating"].mean(skipna=True), 2))
c3.metric("🗳️ Total Votes", int(filtered_df["Votes"].sum(skipna=True)))
c4.metric(
    "🚚 Online Delivery",
    filtered_df[filtered_df["Has Online delivery"].str.strip() == "Yes"].shape[0]
)

st.divider()

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(
    ["💰 Price Analysis", "🍕 Cuisine Analysis", "⭐ Rating Analysis", "🏙️ City-wise Restaurants"]
)

# ---------------- TAB 1: Price Analysis ----------------
with tab1:
    st.subheader("Restaurants Distribution by Price Range")

    price_counts = filtered_df["Price range"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(price_counts.index, price_counts.values, color="#4DA8DA")

    ax.set_xlabel("Price Range")
    ax.set_ylabel("Number of Restaurants")
    ax.set_title("Price Range Distribution")

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h, str(h),
                ha='center', va='bottom', fontweight='bold')

    st.pyplot(fig)

# ---------------- TAB 2: Cuisine Analysis ----------------
with tab2:
    st.subheader("Top 10 Popular Cuisines")

    cuisines = filtered_df["Cuisines"].dropna().str.split(", ").explode()
    top_cuisines = cuisines.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.barh(top_cuisines.index[::-1], top_cuisines.values[::-1], color="#7ED957")

    ax.set_xlabel("Number of Restaurants")
    ax.set_ylabel("Cuisine")
    ax.set_title("Top 10 Cuisines")

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1, bar.get_y() + bar.get_height()/2, str(w),
                va='center', fontweight='bold')

    st.pyplot(fig)

# ---------------- TAB 3: Rating Analysis ----------------
with tab3:
    st.subheader("Average Rating by Price Range")

    avg_rating = filtered_df.groupby("Price range")["Aggregate rating"].mean()

    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(avg_rating.index, avg_rating.values, color="#FFA500")

    ax.set_xlabel("Price Range")
    ax.set_ylabel("Average Rating")
    ax.set_ylim(0,5)
    ax.set_title("Average Rating vs Price Range")

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f"{h:.2f}",
                ha='center', color='red', fontweight='bold')

    st.pyplot(fig)

# ---------------- TAB 4: City-wise Restaurants ----------------
with tab4:
    if selected_city == "All":
        st.info("Please select a specific city from sidebar to view restaurant-wise ratings.")
    else:
        st.subheader(f"Top Restaurants in {selected_city} by Rating")

        city_df = filtered_df.sort_values("Aggregate rating")

        fig, ax = plt.subplots(figsize=(10, max(6, len(city_df)*0.3)))
        bars = ax.barh(city_df["Restaurant Name"], city_df["Aggregate rating"], color="#9B59B6")

        ax.set_xlabel("Rating")
        ax.set_ylabel("Restaurant Name")
        ax.set_xlim(0,5)

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.05, bar.get_y() + bar.get_height()/2, f"{w:.2f}",
                    va='center', fontweight='bold')

        st.pyplot(fig)

# ====================== DATASET ======================
with st.expander("📄 View Dataset Sample"):
    st.dataframe(filtered_df.head(20))

# ====================== INSIGHTS ======================
st.markdown("## 📌 Key Business Insights")
st.markdown("""
• Mid-range priced restaurants dominate the market  
• Customer ratings remain consistent across price ranges  
• Limited cuisines capture major market share  
• City-wise analysis shows strong competition among top restaurants  
• Online delivery improves restaurant visibility and reach  
""")

st.markdown(
    "<p style='text-align:center; color:grey;'>Dashboard created using Python, Pandas, Matplotlib & Streamlit</p>",
    unsafe_allow_html=True
)