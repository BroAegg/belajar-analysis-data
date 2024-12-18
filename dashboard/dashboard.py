import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import matplotlib.image as mpimg
from babel.numbers import format_currency
import streamlit as st
from func import DataAnalyzer, BrazilMapPlotter

sns.set(style='whitegrid')

st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .sidebar .sidebar-content h1 {
            color: #333;
        }
        .sidebar .sidebar-content p {
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='font-size:25px;'>E-Commerce Insights</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Explore sales, customer data, and product trends with detailed visualizations.", unsafe_allow_html=True)

all_data = pd.read_csv("https://raw.githubusercontent.com/BroAegg/Belajar-Analysis-Data/main/data_E-commerce_Public/all_data.csv")
geolocation = pd.read_csv('https://raw.githubusercontent.com/BroAegg/Belajar-Analysis-Data/main/data_E-commerce_Public/geolocation.csv')

datetime_cols = ["order_approved_at", "order_delivered_carrier_date", 
                 "order_delivered_customer_date", "order_estimated_delivery_date", 
                 "order_purchase_timestamp", "shipping_limit_date"]

for col in datetime_cols:
    all_data[col] = pd.to_datetime(all_data[col])

# Sort and reset index
all_data.sort_values(by="order_approved_at", inplace=True)
all_data.reset_index(drop=True, inplace=True)

st.sidebar.markdown("## 📅 Select Date Range")
min_date = all_data["order_approved_at"].min()
max_date = all_data["order_approved_at"].max()
start_date, end_date = st.sidebar.date_input("Choose Date Range", 
                                               [min_date, max_date], 
                                               min_value=min_date, 
                                               max_value=max_date)

st.sidebar.markdown("---")  # Add a separator

st.sidebar.markdown("## 🛍️ Filter by Order Status")
order_status_options = all_data['order_status'].unique()
selected_status = st.sidebar.selectbox("Select Order Status", options=order_status_options)

main_df = all_data[(all_data["order_approved_at"] >= str(start_date)) & 
                 (all_data["order_approved_at"] <= str(end_date)) & 
                 (all_data["order_status"] == selected_status)]

st.sidebar.markdown("---")

# Sidebar
st.sidebar.markdown("## 📊 Data Summary")
total_orders = len(main_df)
total_revenue = main_df['payment_value'].sum()
st.sidebar.metric("Total Orders", total_orders)
st.sidebar.metric("Total Revenue", format_currency(total_revenue, "IDR", locale="id_ID"))

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(geolocation.drop_duplicates(subset='customer_unique_id'), 
                             plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

st.markdown("<h1 class='big-font'>E-Commerce Dashboard</h1>", unsafe_allow_html=True)

# Question 1: Top 5 Products Sold
st.markdown("<h2 class='header-font'>Top 5 Products Sold</h2>", unsafe_allow_html=True)
sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False).head(5)

# Plot Top 5 Products Sold
fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", n_colors=5)
sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df, palette=colors, ax=ax)
ax.set_xlabel("Number of Products Sold", fontsize=14)
ax.set_ylabel("Product Category", fontsize=14)
ax.set_title("Top 5 Products Sold", loc="center", fontsize=18)
st.pyplot(fig)

# Question 2: Monthly Orders
st.markdown("<h2 class='header-font'>Monthly Orders</h2>", unsafe_allow_html=True)
if 'order_approved_at' in all_data.columns:
    all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'], errors='coerce')
    monthly_df = all_data.resample(rule='M', on='order_approved_at').agg({"order_id": "nunique"})
    monthly_df.index = monthly_df.index.strftime('%B')
    monthly_df = monthly_df.reset_index().rename(columns={"order_id": "order_count"})
    month_mapping = {month: i for i, month in enumerate(monthly_df['order_approved_at'].unique(), 1)}
    monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
    monthly_df = monthly_df.sort_values("month_numeric").drop("month_numeric", axis=1)

    # Plot Monthly Orders
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_df["order_approved_at"], y=monthly_df["order_count"], color="#068DA9", ax=ax)
    ax.set_title("Number of Orders per Month (2018)", loc="center", fontsize=20)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Number of Orders", fontsize=12)
    st.pyplot(fig)
else:
    st.write("'order_approved_at' does not exist in the DataFrame.")

# Question 3: Orders by Day and Hour
st.markdown("<h2 class='header-font'>Orders by Day and Hour</h2>", unsafe_allow_html=True)
all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'])
all_data['day_of_week'] = all_data['order_approved_at'].dt.day_name()
all_data['hour_of_day'] = all_data['order_approved_at'].dt.hour

daily_sales = all_data.groupby('day_of_week')['order_id'].count().reset_index().rename(columns={"order_id": "total_orders"})
hourly_sales = all_data.groupby('hour_of_day')['order_id'].count().reset_index().rename(columns={"order_id": "total_orders"})

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_sales['day_of_week'] = pd.Categorical(daily_sales['day_of_week'], categories=days_order, ordered=True)
daily_sales = daily_sales.sort_values('day_of_week')

# Plot Orders by Day
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='day_of_week', y='total_orders', data=daily_sales, palette='viridis', ax=ax)
ax.set_title('Total Orders by Day of the Week', fontsize=20)
ax.set_xlabel('Day of the Week', fontsize=14)
ax.set_ylabel('Total Orders', fontsize=14)
st.pyplot(fig)

# Plot Orders by Hour
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='hour_of_day', y='total_orders', data=hourly_sales, palette='viridis', ax=ax)
ax.set_title('Total Orders by Hour of the Day', fontsize=20)
ax.set_xlabel('Hour of the Day', fontsize=14)
ax.set_ylabel('Total Orders', fontsize=14)
st.pyplot(fig)

# Question 4: Geographical Distribution of Customers
st.markdown("<h2 class='header-font'>Geographical Distribution of Customers</h2>", unsafe_allow_html=True)
def plot_brazil_map(data):
    brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
    fig, ax = plt.subplots(figsize=(10, 10))
    extent = [-73.98283055, -33.8, -33.75116944, 5.4]
    heatmap_data = data[['geolocation_lat', 'geolocation_lng']]
    sns.kdeplot(data=heatmap_data, x='geolocation_lng', y='geolocation_lat', fill=True, cmap='Reds', alpha=0.5, thresh=0, ax=ax)
    ax.imshow(brazil, extent=extent, aspect='auto')
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.axis('off')

    return fig

fig = plot_brazil_map(geolocation.drop_duplicates(subset='customer_unique_id'))
st.pyplot(fig)
