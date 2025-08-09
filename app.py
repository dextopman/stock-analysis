import streamlit as st

import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


company_list =[
    r'E:\\stock\\individual_stocks_5yr\\AMZN_data.csv',
    r'E:\\stock\\individual_stocks_5yr\\AAPL_data.csv',
    r'E:\\stock\\individual_stocks_5yr\\GOOGL_data.csv',
    r'E:\\stock\\individual_stocks_5yr\\IBM_data.csv'
    
]

all_data = pd.DataFrame()

for file in company_list:
    
    current_df = pd.read_csv(file)
    
    all_data = current_df._append(all_data, ignore_index=True)


all_data['date'] = pd.to_datetime(all_data['date'])

st.set_page_config(page_title="Stock Analysis Application", layout="wide")
st.title("Stock Analysis App")

techlist = all_data['Name'].unique()

st.sidebar.title("Choose a Company")



selected_company = st.sidebar.selectbox("Select a stock", techlist)

company_df = all_data[all_data['Name'] == selected_company]
company_df.sort_values(by='date', inplace=True)

#plotting the data
st.subheader("1. Closing Price of {selected_company} Over Time")
fig1 = px.line(company_df, x='date', y='close', title=selected_company + ' Closing price over time ')
st.plotly_chart(fig1, use_container_width=True)

#second plot
st.subheader("2. Moving Averages (10, 20, 50 days)")

ma_day = [10, 20, 50]

for ma in ma_day:
    company_df['close_' + str(ma)] = company_df['close'].rolling(ma).mean()

fig2 = px.line(company_df, x='date', y=['close', 'close_10', 'close_20', 'close_50'], title=selected_company + ' Closing price with moving average')

#third plot
st.subheader("3. Daily Returns for" + selected_company)
company_df['Daily return(in %)'] = company_df['close'].pct_change() * 100

fig3 = px.line(company_df, x='date', y='Daily return(in %)', title= 'Daily return(%)')
st.plotly_chart(fig3, use_container_width=True)

#fourth plot
st.subheader("4. Resampled Closing Price Quarterly / Monthly / Yearly")

company_df.set_index('date', inplace=True)
Resample_option = st.radio("Select Resample Frequency", ["Monthly", "Quarterly", "Yearly"])

if Resample_option == "Monthly":
   resampled = company_df['close'].resample('M').mean()
elif Resample_option == "Quarterly":
    resampled = company_df['close'].resample('Q').mean()
else:
    resampled = company_df['close'].resample('Y').mean()

fig4 = px.line(resampled, title= selected_company + ' ' + Resample_option + 'Average Closing Price')
st.plotly_chart(fig4, use_container_width=True)

#fifth plot
amzn = pd.read_csv(company_list[0])
apple   = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
ibm = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['amazon_close'] = amzn['close']
closing_price['apple_close'] = apple['close']
closing_price['google_close'] = google['close']
closing_price['ibm_close'] = ibm['close']

fig5 , ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig5)


st.markdown("....")


    