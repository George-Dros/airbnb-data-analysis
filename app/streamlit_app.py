import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

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
                                min_value=0.0,
                                max_value=max_price,
                                value = (0.0, max_price)
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



st.markdown("---") 
st.header("📋 Filtered Listings (Optional)")


st.markdown("---") 
st.header("📎 Notes & Insights")


