# -*- coding: utf-8 -*-
"""Copy of Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wy0EaE6hpsU3cqycGbRcj_Bw_IOCsVrJ

# Proyek Analisis Data: [Platform E-commerce Public]
- **Nama:** [Aegner Billik]
- **Email:** [m491b4ky0145@bangkit.academy]
- **ID Dicoding:** [31230]

## Menentukan Pertanyaan Bisnis

- Produk Apa Saja yang Memiliki Pertumbuhan Penjualan Terbanyak?
- Bagaimana penjualan pada platform E-Commerce Public tersebut?
- Dimana lokasi dengan penjualan terbanyak? [secara geografis]
- Apakah ada hari dengan penjualan tertinggi di E-commerce Public tersebut?

## Import Semua Packages/Library yang Digunakan
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
# %pip install pandas
# %pip install unidecode
import pandas as pd
import matplotlib.pyplot as plt
import urllib
# %pip uninstall unidecode
# %pip install unidecode
import unidecode
import matplotlib.image as mpimg
# %pip install seaborn
import seaborn as sns

"""## Data Wrangling

### Gathering Data
"""

customers_df = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/customers_dataset.csv')
customers_df.head()

geo_df = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/geolocation_dataset.csv')
geo_df.head()

order_items = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/order_items_dataset.csv')
order_items.head()

order_pay = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/order_payments_dataset.csv')
order_pay.head()

order_rev = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/order_reviews_dataset.csv')
order_rev.head()

orders_df = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/orders_dataset.csv')
orders_df.head()

product_cat = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/product_category_name_translation.csv')
product_cat.head()

products_df = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/products_dataset.csv')
products_df.head()

sellers_df = pd.read_csv('Belajar Analysis Data/data_E-commerce_Public/sellers_dataset.csv')
sellers_df.head()

"""**Insight:**
Memanggil Semua Data dari file data_e-commerce_Public

### Assessing Data
"""

# Function to display info, null values, duplicate entries, and summary stats for each DataFrame
def assess_dataframe(df, name):
    print(f"\n### {name} DataFrame ###")
    print(f"\nInfo for {name}:")
    print(df.info())

    print(f"\nNull values in {name}:\n{df.isnull().sum()}")

    print(f"\nDuplicate entries in {name}: {df.duplicated().sum()}")

    print(f"\nSummary statistics for {name}:\n{df.describe(include='all')}")
    print("\n" + "-"*50 + "\n")


# List of DataFrames to assess
dataframes = {
    "Customers": customers_df,
    "Geolocation": geo_df,
    "Order Items": order_items,
    "Order Payments": order_pay,
    "Order Reviews": order_rev,
    "Orders": orders_df,
    "Product Categories": product_cat,
    "Products": products_df,
    "Sellers": sellers_df
}

# Loop through and assess each DataFrame
for name, df in dataframes.items():
    assess_dataframe(df, name)

# Display geolocation info separately
print("\nAdditional Info for Geolocation DataFrame:")
geo_df.info()

"""**Insight:**
Mengakses semua data tadi

### Cleaning Data
"""

order_rev[order_rev.review_comment_title.isna()]

order_rev.review_comment_title.value_counts()

order_rev[order_rev.review_comment_message.isna()]

order_rev.review_comment_message.value_counts()

order_rev.fillna(value="no comment", inplace=True)

orders_df[orders_df.order_approved_at.isna()]

datetime_oi = ["shipping_limit_date"]

for column in datetime_oi:
  order_items[column] = pd.to_datetime(order_items[column])

datetime_or = ["review_creation_date","review_answer_timestamp"]

for column in datetime_or:
  order_rev[column] = pd.to_datetime(order_rev[column])

datetime_oo = ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]

for column in datetime_oo:
  orders_df[column] = pd.to_datetime(orders_df[column])

order_items.info()

order_rev.info()

orders_df.info()

"""**Insight:**
Membersihkan data

## Exploratory Data Analysis (EDA)

### Explore ...
"""

customers_df.sample(5)

customers_df.describe(include='all')

customers_df.customer_id.is_unique

# Memeriksa nilai yang duplikat pada kolom 'customer_id' di DataFrame 'customers_df'
duplicated_customers = customers_df.customer_id.duplicated()

# Menampilkan hasil
print(duplicated_customers)

customers_df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False)

customers_df.groupby(by="customer_state").customer_id.nunique().sort_values(ascending=False)

order_pay.sample(5)

order_pay.describe(include='all')

order_pay.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False)

orders_df.sample(5)

delivery_time = orders_df["order_delivered_customer_date"] - orders_df["order_delivered_carrier_date"]
delivery_time = delivery_time.apply(lambda x: x.total_seconds())
orders_df["delivery_time"] = round(delivery_time/86400)

orders_df.sample(5)

orders_df.delivery_time.hist()

customer_id_in_orders_df = orders_df.customer_id.values

customers_df["status"] = customers_df["customer_id"].apply(lambda x: "Active" if x in customer_id_in_orders_df else "Non Active")

customers_df.sample(5)

customers_df.groupby(by="status").customer_id.count()

"""Merge customers_df & orders_df"""

cust_orders_df = pd.merge(
    left=customers_df,
    right=orders_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
)
cust_orders_df.head()

cust_orders_df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).head(10)

cust_orders_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).head(10)

cust_orders_df.groupby(by="customer_zip_code_prefix").order_id.nunique().sort_values(ascending=False).head(10)

cust_orders_df.groupby(by="order_status").order_id.nunique().sort_values(ascending=False).head(10)

"""Merge order_pay & order_rev"""

order_payrev_df = pd.merge(
    left=order_pay,
    right=order_rev,
    how="left",
    left_on="order_id",
    right_on="order_id"
)
order_payrev_df.head()

order_payrev_df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False).head(10)

order_payrev_df.sort_values(by="payment_value", ascending=False)

order_payrev_df.groupby(by="payment_type").agg({
    "order_id": "nunique",
    "payment_value":  ["min", "max"]
})

"""Merge cust_orders_df & order_payrev"""

customers_df = pd.merge(
    left=cust_orders_df,
    right=order_payrev_df,
    how="left",
    left_on="order_id",
    right_on="order_id"
)
customers_df.head()

"""Explore order_items & sellers_df

Merge order_items & sellers_df
"""

item_seller_df = pd.merge(
    left=order_items,
    right=sellers_df,
    how="left",
    left_on="seller_id",
    right_on="seller_id"
)
item_seller_df.head()

item_seller_df.groupby(by="seller_city").seller_id.nunique().sort_values(ascending=False).head(10)

"""Explore products_df & product_cat

Merge products_df & product_cat
"""

product_df = pd.merge(
    left=products_df,
    right=product_cat,
    how="left",
    left_on="product_category_name",
    right_on="product_category_name"
)
product_df.head()

product_df.groupby(by="product_category_name").product_id.nunique().sort_values(ascending=False).head(10)

product_df.groupby(by="product_category_name_english").product_id.nunique().sort_values(ascending=False).head(10)

"""Merge item_seller_df & product_df"""

sellers_df = pd.merge(
    left=product_df,
    right=item_seller_df,
    how="left",
    left_on="product_id",
    right_on="product_id"
)
sellers_df.head()

sellers_df.sort_values(by="price", ascending=False)

sellers_df.groupby(by="product_category_name_english").agg({
    "order_id": "nunique",
    "price":  ["min", "max"]
})

geo_df.sample(5)

def pretty_string(column):
    column_space = ' '.join(column.split())
    return unidecode.unidecode(column_space.lower())

geo_df['geolocation_city'] = geo_df['geolocation_city'].apply(pretty_string)

geo_df.groupby('geolocation_zip_code_prefix').size().sort_values(ascending=False)

geo_df[geo_df['geolocation_zip_code_prefix'] == 24220].head()

"""Explore all data

Merge semua data, kecuali geolocation karna tidak kita perlukan.
"""

all_data = pd.merge(
    left=customers_df,
    right=sellers_df,
    how="left",
    left_on="order_id",
    right_on="order_id"
)
all_data.head()

all_data.info()

all_data.groupby(by=["customer_city", "product_category_name_english"]).agg({
    "price": "sum",
    "freight_value": "sum"
})

all_data.groupby(by=["customer_state", "product_category_name_english"]).agg({
    "price": "sum",
    "freight_value": "sum"
})

all_data.groupby(by="customer_state").agg({
    "order_id": "nunique",
    "payment_value": "sum"
}).sort_values(by="payment_value", ascending=False)

all_data.groupby(by="product_category_name_english").agg({
    "order_id": "nunique",
    "review_score":  ["min", "max"]
})

"""Convert all_data ke .csv"""

import os

dir_path = 'Belajar Analysis Data/data_E-commerce_Public'

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

all_data.to_csv('Belajar Analysis Data/data_E-commerce_Public/all_data.csv', index=False)

"""## Visualization & Explanatory Analysis

Pertanyaan 1 : Produk Apa Saja yang Memiliki Pertumbuhan Penjualan Terbanyak?
"""

sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
sum_order_items_df = sum_order_items_df.head(10)  # Get top 10 categories

plt.figure(figsize=(12, 6))
colors = sns.color_palette("viridis", n_colors=5)  # Using a different color palette

# Create a barplot for the top-selling products
sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors)
plt.xlabel("Number of Products Sold", fontsize=14)
plt.ylabel("Product Category", fontsize=14)
plt.title("Top 5 Products Sold", loc="center", fontsize=18)
plt.tick_params(axis='y', labelsize=12)
plt.show()

"""Pertanyaan 2 : Bagaimana penjualan pada platform E-Commerce Public tersebut?"""

import pandas as pd

# Display the columns to find 'order_approved_at'
print("Columns in all_data:", all_data.columns.tolist())

# If necessary, strip whitespace from column names
all_data.columns = all_data.columns.str.strip()

# Display the first few rows to check the data
print(all_data.head())

# Convert 'order_approved_at' to datetime if it exists
if 'order_approved_at' in all_data.columns:
    all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'], errors='coerce')

    # Check for NaT values
    print("Number of NaT values in 'order_approved_at':", all_data['order_approved_at'].isna().sum())

    # Resample the data by month
    monthly_df = all_data.resample(rule='M', on='order_approved_at').agg({
        "order_id": "nunique",
    })

    # Change the index format to Year-Month
    monthly_df.index = monthly_df.index.strftime('%B')
    monthly_df = monthly_df.reset_index()

    # Rename the columns for clarity
    monthly_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)

    # Display the result
    print(monthly_df.head())
else:
    print("'order_approved_at' does not exist in the DataFrame.")

monthly_df = monthly_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last').reset_index(drop=True)

monthly_df.head()

monthly_df.sort_values(by='order_count')

month_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
monthly_df = monthly_df.sort_values("month_numeric")
monthly_df = monthly_df.drop("month_numeric", axis=1)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=monthly_df["order_approved_at"],
    y=monthly_df["order_count"],
    color="#068DA9"
)
plt.title("Number of Orders per Month (2018)", loc="center", fontsize=20)
plt.xticks(fontsize=10, rotation=25)
plt.yticks(fontsize=10)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Orders", fontsize=12)
plt.show()

"""Pertanyaan 3: Apakah ada hari dengan penjualan tertinggi di E-commerce Public tersebut?"""

# Convert 'order_approved_at' to datetime if not already in that format
all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'])

# Extract day of the week and hour
all_data['day_of_week'] = all_data['order_approved_at'].dt.day_name()
all_data['hour_of_day'] = all_data['order_approved_at'].dt.hour

# Count the number of orders by day of the week
daily_sales = all_data.groupby('day_of_week')['order_id'].count().reset_index()
daily_sales = daily_sales.rename(columns={"order_id": "total_orders"})
daily_sales = daily_sales[['day_of_week', 'total_orders']]

# Count the number of orders by hour of the day
hourly_sales = all_data.groupby('hour_of_day')['order_id'].count().reset_index()
hourly_sales = hourly_sales.rename(columns={"order_id": "total_orders"})
hourly_sales = hourly_sales[['hour_of_day', 'total_orders']]

# Create the DataFrame. Replace the sample data with your actual data
monthly_spend_df = pd.DataFrame({
    'order_approved_at': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25'],
    'total_spend': [100, 150, 200, 120]
})

# Convert 'order_approved_at' to datetime
monthly_spend_df['order_approved_at'] = pd.to_datetime(monthly_spend_df['order_approved_at'])

# Now you can sort and drop duplicates
monthly_spend_df = monthly_spend_df.sort_values('total_spend').drop_duplicates('order_approved_at', keep='last')

monthly_spend_df.head()

# Sort days of the week for better visualization
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_sales['day_of_week'] = pd.Categorical(daily_sales['day_of_week'], categories=days_order, ordered=True)
daily_sales = daily_sales.sort_values('day_of_week')

plt.figure(figsize=(10, 5))
sns.barplot(x='day_of_week', y='total_orders', data=daily_sales, palette='viridis')
plt.title('Total Orders by Day of the Week', fontsize=20)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Total Orders', fontsize=14)
plt.xticks(rotation=45)
plt.show()

"""Dari diagram batang diatas hari selasa merupakan puncak pemesanan dengan >20000 pemesanan

Pertanyaan 4 : Dimana lokasi dengan penjualan terbanyak? [secara geografis]
"""

other_state_geolocation = geo_df.groupby(['geolocation_zip_code_prefix'])['geolocation_state'].nunique().reset_index(name='count')
other_state_geolocation[other_state_geolocation['count']>= 2].shape
max_state = geo_df.groupby(['geolocation_zip_code_prefix','geolocation_state']).size().reset_index(name='count').drop_duplicates(subset = 'geolocation_zip_code_prefix').drop('count',axis=1)

geolocation_silver = geo_df.groupby(['geolocation_zip_code_prefix','geolocation_city','geolocation_state'])[['geolocation_lat','geolocation_lng']].median().reset_index()
geolocation_silver = geolocation_silver.merge(max_state,on=['geolocation_zip_code_prefix','geolocation_state'],how='inner')

customers_silver = customers_df.merge(geolocation_silver,left_on='customer_zip_code_prefix',right_on='geolocation_zip_code_prefix',how='inner')

customers_silver.head()

customers_silver.to_csv("Belajar Analysis Data/data_E-commerce_Public/geolocation.csv", index=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import matplotlib.image as mpimg

def plot_brazil_map(data):
    # Load the map image
    brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')

    # Set the figure size
    plt.figure(figsize=(10, 10))

    # Set the bounds for the map
    extent = [-73.98283055, -33.8, -33.75116944, 5.4]

    # Create the heatmap using seaborn
    heatmap_data = data[['geolocation_lat', 'geolocation_lng']]

    # Plotting the heatmap
    ax = plt.gca()  # Get the current axis
    sns.kdeplot(data=heatmap_data, x='geolocation_lng', y='geolocation_lat', fill=True, cmap='Reds', alpha=0.5, thresh=0, ax=ax)

    # Display the base map
    plt.imshow(brazil, extent=extent, aspect='auto')

    # Set the limits to match the extent of the map image
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])

    # Remove axis
    plt.axis('off')
    plt.show()

# Plotting the heatmap with unique customer data
plot_brazil_map(customers_silver.drop_duplicates(subset='customer_unique_id'))

"""## Analisis Lanjutan (Opsional)"""

cust_orders_df = pd.merge(
    left=cust_orders_df,
    right=order_payrev_df[['order_id', 'payment_value']],
    how='left',
    on='order_id'
)

# Membuat kolom baru untuk RFM analysis
cust_orders_df['Recency'] = (cust_orders_df['order_purchase_timestamp'].max() - cust_orders_df['order_purchase_timestamp']).dt.days
cust_orders_df['Frequency'] = cust_orders_df.groupby('customer_id')['order_id'].transform('count')
cust_orders_df['Monetary'] = cust_orders_df.groupby('customer_id')['payment_value'].transform('sum')

# Menampilkan hasil RFM
cust_orders_df[['customer_id', 'Recency', 'Frequency', 'Monetary']].drop_duplicates().head()

"""## Conclusion

- Produk Apa Saja yang Memiliki Pertumbuhan Penjualan Terbanyak?
Hasil analisis menunjukkan bahwa produk dengan pertumbuhan penjualan tercepat adalah bed_bath_table. Meskipun terjadi penurunan pada bulan September dan Oktober, penjualan kembali naik pada bulan November.


- Bagaimana penjualan pada platform E-Commerce Public tersebut?
Penjualan di platform E-Commerce Public menunjukkan pencapaian yang konsisten. Dari Januari hingga Agustus, penjualan relatif stabil, dengan penurunan yang signifikan pada bulan September dan Oktober, lalu ada kenaikan tajam pada bulan November. pada bulan Desember terlihat mengalami Penurunan.

- Dimana lokasi dengan penjualan terbanyak? [secara geografis]
Berdasarkan visualisasi data geografis, mayoritas pelanggan berasal dari wilayah tenggara dan selatan Brasil.

- Apakah ada hari dengan penjualan tertinggi di E-commerce Public tersebut?
Analisis terhadap data penjualan berdasarkan hari menunjukkan bahwa hari Selasa menjadi puncak pemesanan, dengan total lebih dari 20.000 pesanan.
"""

pip show unidecode

