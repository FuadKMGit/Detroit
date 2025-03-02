import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Reporting Tool", layout="wide")

st.title("📊 Sales Reporting Tool Prototype")

# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.fillna(0, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.to_period('M')
    
    st.sidebar.header("Filters")
    manufacturers = st.sidebar.multiselect("Select Manufacturer(s)", options=df['Manufacturer'].unique(), default=df['Manufacturer'].unique())
    start_date = st.sidebar.date_input("Start Date", value=df['Date'].min())
    end_date = st.sidebar.date_input("End Date", value=df['Date'].max())

    filtered_df = df[(df['Manufacturer'].isin(manufacturers)) & (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    st.subheader("Sales Trend Over Time")
    monthly_sales = filtered_df.groupby('Month')['Total amount'].sum()
    st.line_chart(monthly_sales)

    st.subheader("Top Manufacturers by Total Sales")
    top_manufacturers = filtered_df.groupby('Manufacturer')['Total amount'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_manufacturers)

    st.subheader("Distribution of Purchase Prices")
    st.hist_chart(filtered_df['Purchase price'])
else:
    st.write("Please upload an Excel file to proceed.")
