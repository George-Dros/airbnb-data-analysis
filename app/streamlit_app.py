import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import numpy as np

# Data preparing

df = pd.read_csv("listings_cleaned.csv", parse_dates=["first_review", "last_review"])

neighbourhood_list = sorted(df['neighbourhood_cleansed'].unique())
room_types = df['room_type'].unique()
prices = df['price']
min_price = prices.min()
max_price = prices.max()

# Streamlit App

st. set_page_config(layout="wide",page_title="Airbnb EDA 📊",page_icon="🏠" )
st.title("Airbnb Listings Analysis")
st.markdown("Explore listings across neighbourhoods, prices, and availability in your city.")


# Sidebar
st.sidebar.markdown("👈 Use the filters here to customize the analysis.")

all_neighbourhoods_selected = st.sidebar.checkbox("Select All Neighbourhoods", value=True)

if all_neighbourhoods_selected:
    neighbourhoods = st.sidebar.multiselect("Neighbourhoods",
                                            options=neighbourhood_list,
                                            default=neighbourhood_list)
else:
    neighbourhoods = st.sidebar.multiselect("Neighbourhoods",
                                            options=neighbourhood_list)

all_rooms_selected = st.sidebar.checkbox("Select All Room Types", value=True)

if all_rooms_selected:
    rooms = list(room_types)
else:
    rooms = st.sidebar.multiselect("Room Type", options=room_types, default=[])
    
host_state = st.sidebar.checkbox(label="Owner is Superhost", value=False)

price_range = st.sidebar.slider(label="Price Range",
                                min_value=0.00,
                                max_value=max_price,
                                value = (0.00, max_price)
                                )

min_price_selected, max_price_selected = price_range

nights_range = st.sidebar.slider(label="Minimum Nights Filter",
                                 min_value=0,
                                 max_value=30,
                                 value = (0, 30),
                                )

min_nights, max_nights = nights_range

outliers_state = st.sidebar.checkbox(label="Hide Price Outliers (top 1%)", value=False)

df_filtered = df[
    (df['neighbourhood_cleansed'].isin(neighbourhoods)) &
    (df['room_type'].isin(rooms)) &
    (df['host_is_superhost'] == host_state) &
    (df['price'] >= min_price_selected) & (df['price'] <= max_price_selected) &
    (df['minimum_nights'] >= min_nights) & (df['maximum_nights'] <= max_nights)
]

if outliers_state:
    threshold = df_filtered['price'].quantile(0.99)
    df_filtered = df_filtered[df_filtered['price'] <= threshold]

df_filtered['log_price'] = np.log1p(df_filtered['price'])

mean_price = df_filtered['price'].mean()
total_listings = len(df_filtered)
mean_guests = df_filtered['accommodates'].mean()
avg_min_nights = df_filtered['minimum_nights'].mean()
avg_max_nights = df_filtered['maximum_nights'].mean()
avg_rating = df_filtered['review_scores_rating'].mean()
avg_rev_per_m = df_filtered['reviews_per_month'].mean()

# Headers
st.header("📊 Filter Listings")

if all_neighbourhoods_selected:
    neighbourhood_text = "all neighbourhoods"
elif len(neighbourhoods) == 1:
    neighbourhood_text = neighbourhoods[0]
elif len(neighbourhoods) <= 3:
    neighbourhood_text = ", ".join(neighbourhoods)
else:
    neighbourhood_text = f"{len(neighbourhoods)} neighbourhoods"


if all_rooms_selected:
    room_text = "all Room types"
elif len(rooms) == 1:
    room_text = rooms[0]
elif len(rooms) <= 3:
    room_text = ", ".join(rooms)
else:
    room_text = f"All {len(rooms)} room types"

    
st.markdown(f"Currently displaying listings in {neighbourhood_text} with {room_text} and price between €{min_price_selected} and €{max_price_selected}.") 

st.markdown("---") 
st.header("📌 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Listings", round(total_listings, 2))
    st.metric("Average Price (€)", round(mean_price, 2))

with col2:
    st.metric("Avg Guests Accommodated", round(mean_guests, 2))
    st.metric("Avg Minimum Nights", round(avg_min_nights, 2))

with col3:
    st.metric("Avg Rating", round(avg_rating,2 ))
    st.metric("Avg Reviews/Month", round(avg_rev_per_m, 2))

st.markdown("---") 
st.header("📈 Visualizations")

tab1, tab2, tab3, tab4 = st.tabs(["📦 Price by Room Type","🔹 Price Distribution" ,"📍 Price vs Availability","Avg Price per Neighbourhood"])

with tab1:
    log_scale1 = st.checkbox("Use log scale", value=False,key="log_1")

    if log_scale1:      
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_filtered, x='room_type', y='log_price', ax=ax1)
        ax1.set_title('Boxplot of Log(Price + 1) by Room Type')
        ax1.set_ylabel('Log(Price + 1)')
        ax1.set_xlabel('Room Type')
        st.pyplot(fig1)

    else:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_filtered, x='room_type', y='price', ax=ax1)
        ax1.set_title('Boxplot of Price by Room Type')
        ax1.set_ylabel('Price')
        ax1.set_xlabel('Room Type')
        st.pyplot(fig1)


with tab2:
    log_scale2 = st.checkbox("Use log scale", value=False,key="log_2")
    
    if log_scale2:
        price_data = df_filtered['log_price']
        x_label = "Log(Price + 1)"
        
    else:
        price_data = df_filtered['price']
        x_label = "Price (€)"

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(price_data, bins=50, kde=False, ax=ax2)
    ax2.set_title("Histogram of Price Distribution")   
    ax2.set_xlabel(x_label)
    ax2.set_ylabel("Count")
    st.pyplot(fig2)


with tab3:
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x='availability_365',
        y='price',
        hue='room_type',
        alpha=0.6,
        ax=ax3
    )
    ax3.set_title("Price vs Availability (365 days)")
    ax3.set_xlabel("Availability (Days per Year)")
    ax3.set_ylabel("Price (€)")
    st.pyplot(fig3)


with tab4:
    avg_price_by_neighbourhood = (
    df_filtered.groupby('neighbourhood_cleansed')['price']
    .mean()
    .sort_values(ascending=False)
)
    top_n = st.slider("Show top N neighbourhoods by avg price", 5, 30, 15)
    avg_price_df = avg_price_by_neighbourhood.reset_index()

    avg_price_df = avg_price_df.head(top_n)
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.barplot(
        data=avg_price_df,
        y='neighbourhood_cleansed',
        x='price',
        ax=ax4
    )
    ax4.set_title("Average Price by Neighbourhood")
    ax4.set_xlabel("Average Price (€)")
    ax4.set_ylabel("Neighbourhood")
    st.pyplot(fig4)

st.markdown("---") 
st.header("📋 Filtered Listings")

show_table = st.checkbox("Show filtered data table")

if show_table:
    st.dataframe(df_filtered.head(50))
    csv = df_filtered.to_csv(index=False)
    st.download_button("Download as CSV", csv, "filtered_listings.csv", "text/csv")

st.markdown("---") 
st.header("📎 Notes & Insights")

insights = []

# Expensive Neighborhoods
expensive_areas = df_filtered.groupby("neighbourhood_cleansed")["price"].mean().sort_values(ascending=False)
if expensive_areas.iloc[0] > 200:
    insights.append(f"🏙️ **{expensive_areas.index[0]}** has the highest average price at €{expensive_areas.iloc[0]:.0f}.")

# Superhost Performance
if host_state:
    avg_rating_superhost = df_filtered['review_scores_rating'].mean()
    if avg_rating_superhost > 4.7:
        insights.append("🌟 Superhosts have high ratings — averaging above 4.7.")

# Log price skew
if df_filtered['price'].skew() > 1.5:
    insights.append("📈 Price distribution is right-skewed. Consider using log-scale for better clarity.")

# Popular Room Type
most_common_room = df_filtered['room_type'].value_counts().idxmax()
count_most = df_filtered['room_type'].value_counts().max()
insights.append(f"🏠 The most common room type is **{most_common_room}**, appearing {count_most} times.")

# Listings Count Warning
if total_listings < 20:
    insights.append("⚠️ Too few listings — try widening the filters.")

# Show
st.markdown("### Key Observations")
for insight in insights:
    st.markdown(f"- {insight}")


