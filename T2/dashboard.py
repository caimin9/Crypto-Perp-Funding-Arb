import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("Perp Funding Arb Dashboard")

# Load data
def load_data():
    df = pd.read_csv('T2/historical_funding_rates.csv')
    df['fundingRate'] = df['fundingRate'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

df = load_data()

# Sidebar controls
time_window = st.sidebar.selectbox(
    'Select time window',
    ['7 days', '14 days', '30 days', '90 days'],
    index=2
)
window_days = int(time_window.split()[0])

end_time = df['timestamp'].max()
start_time = end_time - pd.Timedelta(days=window_days)
df_window = df[df['timestamp'] >= start_time]

# Calculate metrics
def calc_metrics(df):
    summary = df.groupby('coin').agg(
        avg_abs_spread = ('fundingRate', lambda x: np.mean(np.abs(x))),
        sharpe_ratio = ('fundingRate', lambda x: np.mean(x) / np.std(x) if np.std(x) > 0 else 0)
    ).reset_index()
    return summary

summary = calc_metrics(df_window)
summary_sorted_sharpe = summary.sort_values('sharpe_ratio', ascending=False)
summary_sorted_spread = summary.sort_values('avg_abs_spread', ascending=False)

# Layout
col1, col2 = st.columns(2)

# Bar chart: Sharpe Ratio
with col1:
    st.subheader('Sharpe Ratio by Coin')
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(summary_sorted_sharpe['coin'], summary_sorted_sharpe['sharpe_ratio'], color='royalblue')
    ax.set_xlabel('Coin')
    ax.set_ylabel('Sharpe Ratio')
    ax.set_title('Sharpe Ratio by Coin')
    plt.xticks(rotation=60)
    st.pyplot(fig)

# Bar chart: Average Absolute Spread
with col2:
    st.subheader('Average Absolute Spread by Coin')
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(summary_sorted_spread['coin'], summary_sorted_spread['avg_abs_spread'], color='skyblue')
    ax.set_xlabel('Coin')
    ax.set_ylabel('Average Absolute Spread')
    ax.set_title('Average Absolute Spread by Coin')
    plt.xticks(rotation=60)
    st.pyplot(fig)

# Scatter plot: Sharpe vs Average Abs Spread
st.subheader('Sharpe vs Average Abs Spread')
fig, ax = plt.subplots(figsize=(10,5))
ax.scatter(summary['avg_abs_spread'], summary['sharpe_ratio'], color='blue')
for i, row in summary.iterrows():
    ax.text(row['avg_abs_spread'], row['sharpe_ratio'], row['coin'], fontsize=8, alpha=0.7)

# Regression line
X = summary['avg_abs_spread'].values.reshape(-1, 1)
y = summary['sharpe_ratio'].values
if len(X) > 1:
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)
    ax.plot(summary['avg_abs_spread'], y_pred, color='red', linestyle='dashed')

ax.set_xlabel('Average Absolute Spread')
ax.set_ylabel('Sharpe Ratio')
ax.set_title('Sharpe vs Average Abs Spread')
st.pyplot(fig)

# Data table
st.subheader('Summary Table')
st.dataframe(summary.sort_values('sharpe_ratio', ascending=False).reset_index(drop=True))

st.caption('Data auto-refreshes on rerun. Select time window in sidebar.') 