import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# sns.set(style='dark')

# # Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum",
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "day",
        "cnt": "total_rental",
        "casual": "casual",
        "registered": "registered",
    }, inplace=True)
    
    return daily_orders_df

def create_corr_wind_cnt(df):
    corr_wind_cnt_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum",
        "windspeed": "sum",
        
    })
    corr_wind_cnt_df = corr_wind_cnt_df.reset_index()
    corr_wind_cnt_df.rename(columns={
        "instant": "day",
        "cnt": "total rental",
        "windspeed": "wind speed",
    }, inplace=True)
    
    return corr_wind_cnt_df

def create_corr_humid_cnt_df(df):
    corr_wind_humid_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum",
        "hum": "sum",
        
    })
    corr_wind_humid_df = corr_wind_humid_df.reset_index()
    corr_wind_humid_df.rename(columns={
        "instant": "day",
        "cnt": "total rental",
        "hum": "humidity",
    }, inplace=True)
    
    return corr_wind_humid_df

# # Load cleaned data
df = pd.read_csv("day.csv")

# datetime_columns = ["order_date", "delivery_date"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)

# for column in datetime_columns:
df["dteday"] = pd.to_datetime(df["dteday"])

# Filter data
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bicycle-logo.jpg")
    
    # Mengambil start_date & end_daFfte dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # # Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
corr_wind_cnt_df = create_corr_wind_cnt(main_df)
corr_wind_humid_df = create_corr_humid_cnt_df(main_df)


# plot number of daily orders (2021)
st.header('Analisis data "Bike Sharing Dataset" :sparkles:')
st.subheader('Rental Harian')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.day.sum()
    st.metric("Total Hari", value=total_orders)

with col2:
    total_revenue = daily_orders_df.total_rental.sum()
    st.metric("Total Rental", value=total_revenue)

columns_to_plot = ["total_rental", "casual", "registered"]

fig, ax = plt.subplots(figsize=(16, 8))
# Plot each column as a separate line
for col in columns_to_plot:
  ax.plot(daily_orders_df["dteday"], daily_orders_df[col], marker='o', linewidth=2)

# Set labels and customize the plot
ax.set_xlabel("Date", fontsize=18)
ax.set_ylabel("Value", fontsize=18)  # Generic label as values may differ
ax.tick_params(axis='y', labelsize=16)
ax.tick_params(axis='x', labelsize=14)

# Add a legend to distinguish the lines (optional)
if len(columns_to_plot) > 1:
  ax.legend(columns_to_plot, title="Metrics", loc='upper left', bbox_to_anchor=(1, 1))  # Adjust legend placement as needed

st.pyplot(fig)


#korelasi kecepatan angin dan total rental
st.subheader("Korelasi antara kecepaatn angin dengan total rental")

col_wind, col_rental = st.columns(2)

with col_wind:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        corr_wind_cnt_df["dteday"],
        corr_wind_cnt_df["wind speed"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

with col_rental:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        corr_wind_cnt_df["dteday"],
        corr_wind_cnt_df["total rental"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

#korelasi kecepatan Kelembapan dan total rental
st.subheader("Korelasi antara kecepaatn angin dengan total rental")

col_humid, col_rental = st.columns(2)

with col_humid:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        corr_wind_humid_df["dteday"],
        corr_wind_humid_df["humidity"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

with col_rental:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        corr_wind_cnt_df["dteday"],
        corr_wind_cnt_df["total rental"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    st.pyplot(fig)

# customer demographic
st.subheader("Jumlah Rental Berdasarkan Musim")


fig,ax=plt.subplots(figsize=(15,8))
sns.set_style('white')

main_df['season'] = main_df['season'].map({1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'})

#Bar plot for seasonwise monthly distribution of counts
sns.barplot(x='season',y='cnt',data=main_df[['season','cnt']],hue='season',ax=ax, palette='coolwarm', saturation=2)
ax.set_title('Perbandingan Peminjaman Sepada pada tiap musim')
ax.set(xlabel='Musim', ylabel='Total Peminjaman')
st.pyplot(fig)


st.subheader("Jumlah Rental Berdasarkan Cuaca")

fig,ax=plt.subplots(figsize=(15,8))
sns.set_style('white')

main_df['weathersit'] = main_df['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Snow', 4: 'Heavy Rain'})

#Bar plot for seasonwise monthly distribution of counts
sns.barplot(x='weathersit',y='cnt',data=main_df[['weathersit','cnt']],hue='weathersit',ax=ax, palette='coolwarm', saturation=2)
ax.set_title('Perbandingan Peminjaman Sepada pada tiap cuaca')
ax.set(xlabel='Cuaca', ylabel='Total Peminjaman')
st.pyplot(fig)  
    