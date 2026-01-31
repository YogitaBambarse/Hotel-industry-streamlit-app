st.subheader("🏨 City-wise Restaurants by Average Rating")

if selected_city != "All":
    city_df = filtered_df.copy()
    
    # Sort hotels by rating
    city_df = city_df.sort_values(by="Aggregate rating", ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, max(6, len(city_df)*0.3)))  # height dynamic based on number of restaurants
    bars = ax.barh(city_df["Hotel Name"], city_df["Aggregate rating"], color='purple')
    
    ax.set_xlabel("Average Rating", fontsize=12)
    ax.set_ylabel("Hotel Name", fontsize=12)
    ax.set_title(f"Restaurants in {selected_city} by Average Rating", fontsize=14)
    ax.set_xlim(0, 5)  # Rating scale
    
    # Add rating labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f"{width:.2f}", 
                va='center', color='red', fontweight='bold')
    
    st.pyplot(fig)
else:
    st.info("Please select a specific city to see restaurant-wise graph.")
