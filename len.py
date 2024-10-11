import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# load the trained model
model = load_model('stock_price_prediction_model.h5')

# Function to get stock data
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to prepare data
def prepare_data(data, scaler, time_step=60):
    # Ensure 'Close' column exists
    if 'Close' not in data.columns:
        st.error("The selected stock does not have 'Close' price data.")
        return None, None
    
    close_prices = data['Close'].values.reshape(-1, 1)
    
    # Scale the data
    scaled_data = scaler.fit_transform(close_prices)
    
    # Create x_data (input sequences) and corresponding output data
    x_data = []
    for i in range(time_step, len(scaled_data)):
        x_data.append(scaled_data[i-time_step:i, 0])
    
    x_data = np.array(x_data)
    x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], 1))
    
    # Return x_data and data (from time_step onwards)
    return x_data, data[time_step:]

# Streamlit app
st.title('📈 Stock Price Prediction App')

# Sidebar for user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    ticker = st.sidebar.text_input('Stock Ticker', 'AAPL')
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2015-01-01'))
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('2021-01-01'))
    prediction_start_date = st.sidebar.date_input('Prediction Start Date', pd.to_datetime('2021-01-02'))
    return ticker, start_date, end_date, prediction_start_date

ticker, start_date, end_date, prediction_start_date = user_input_features()

# Load and prepare data when button is clicked
if st.button('Predict'):
    # Load data
    data = get_stock_data(ticker, start_date, end_date)
    if data.empty:
        st.error('No data found for the provided stock ticker and date range.')
    else:
        # Display raw data
        st.subheader('Raw Data')
        st.write(data.tail())

        # Prepare data
        scaler = MinMaxScaler(feature_range=(0, 1))
        x_data, data_for_plot = prepare_data(data, scaler)
        
        if x_data is not None:
            # Make predictions
            predictions = model.predict(x_data)
            predictions = scaler.inverse_transform(predictions)
            
            # Define train_data_len based on the total dataset
            train_data_len = len(data) - len(predictions)
            
            # Create a DataFrame for predictions (align index with data_for_plot)
            pred_df = pd.DataFrame(predictions, index=data_for_plot.index, columns=['Predictions'])
            
            # Combine original data with predictions
            data_for_plot['Predictions'] = pred_df['Predictions']
            
            # Display predictions from the user-selected start date
            pred_data = data_for_plot[data_for_plot.index >= pd.to_datetime(prediction_start_date)]
            st.subheader(f'Predicted Prices from {prediction_start_date}')
            st.write(pred_data[['Close', 'Predictions']])
            
            # Plot the data
            st.subheader('Prediction vs Actual')
            plt.figure(figsize=(12,6))
            plt.plot(data['Close'], label='Actual Price')
            plt.plot(data_for_plot.index, data_for_plot['Predictions'], label='Predicted Price', color='red')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            st.pyplot(plt)
