import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Financial Asset Dashboard')

tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')

dropdown = st.multiselect('Pick your assests', tickers)

start = st.date_input('Start', value = pd.to_datetime('2020-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))

# getting the relative return of the chosen stock
def relativeret(df):
    rel = df.pct_change()
    cumret = (1+rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

# plotting the relative return on the figure
if len(dropdown) > 0:
    df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown[0]))
    st.line_chart(df)