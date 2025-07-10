# 🏠 Airbnb Listings Analysis Dashboard

This is an interactive Streamlit web application for **exploratory data analysis (EDA)** of Airbnb listings.  
It allows users to filter listings, explore summary statistics, generate insightful visualizations, and download filtered datasets.

---

## 🚀 Features

- **Sidebar filters** for:
  - Neighbourhoods
  - Room types
  - Superhost status
  - Price range
  - Minimum nights
  - Outlier removal (top 1% by price)

- **Summary statistics**:
  - Average price, reviews, ratings, accommodation, etc.

- **Interactive visualizations**:
  - 📦 Price by Room Type (log scale optional)
  - 🔹 Price Distribution Histogram (log scale optional)
  - 📍 Price vs Availability
  - 🏙️ Average Price per Neighbourhood (top N toggle)

- **Filtered listings viewer** with CSV download

- **Dynamic automated insights** based on the current filtered dataset

---

## 📦 Installation

```bash
git clone https://github.com/George-Dros/airbnb-data-analysis.git
cd airbnb-data-analysis
pip install -r requirements.txt
```

## ▶️ Run the App

```
streamlit run app.py
```

## 🗂️ Files

* app.py — main Streamlit application

* listings_cleaned.csv — preprocessed dataset (Airbnb listings)

* requirements.txt — required Python libraries

## 📊 Dataset

This app uses a cleaned version of Airbnb listings data.
You can download the raw version from Airbnb.

## 👤 Author

Georgios Drosogiannis
