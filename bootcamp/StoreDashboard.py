import streamlit as st
import pandas as pd
import numpy as np
from numerize import numerize 

# Siapkan data
st.set_page_config(layout="wide")
df = pd.read_csv("store.csv")

# Data preprocessing
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Membuat sidebar
with st.sidebar:
    st.title("Store Dashboard")
    freq = st.selectbox("Select Frequency", ('D', 'W', 'M', 'Q', 'Y'))
    
    years_available = sorted(df['Order Date'].dt.year.unique())
    year = st.selectbox(
        "Select year",
        years_available
    )

# Membuat metric
met1, met2, met3 = st.columns(3)
with met1:
    df_now = df[(df['Order Date'].dt.year == year) & (df['Ship Date'].dt.year == year)]
    df_last = df[(df['Order Date'].dt.year == year-1) & (df['Ship Date'].dt.year == year-1)]

    sales_delta = (df_now['Sales'].sum() - df_last['Sales'].sum()) / df_last['Sales'].sum()
    st.metric(
        "Total sale",
        numerize.numerize(df_now['Sales'].sum()),
        str(round(sales_delta*100,2)) + "%"
    )
with met2:
    st.metric("Total transaction",df['Order ID'].nunique())
with met3:
    st.metric("Number of customers",df['Customer ID'].nunique())

# Membuat grafik sales
st.subheader("Sales")
sales = df[['Order Date', 'Sales']].set_index('Order Date').resample(freq).sum()
st.line_chart(
    sales
)

# Membuat grafik kolom
cust_seg_bar, sales_seg = st.columns(2)
with cust_seg_bar:
    st.subheader("Product Category")
    product_counts = df.groupby('Category').nunique()['Product ID']
    target_product = 'Target Product'
    colors = ['#FFA500']
    st.bar_chart(
        product_counts,
        color=colors
    )
with sales_seg:
    sales_by_cat = pd.pivot_table(
        data=df,
        index='Order Date',
        columns='Category',
        values='Profit',
        aggfunc='sum'
    ).resample(freq).sum()

    st.subheader("Profit by Category")
    st.line_chart(
        pd.DataFrame(
            data = sales_by_cat.values,
            index = sales_by_cat.index,
            columns = list(sales_by_cat.columns)
        )
    )

# Membuat tabel
st.subheader("Year "+ str(year) + " Transaction")
st.dataframe(df_now)

st.subheader("Year " + str(year-1) +" Transaction")
st.dataframe(df_last)
