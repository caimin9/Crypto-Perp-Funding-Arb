import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load historical funding rates
df = pd.read_csv('T2/historical_funding_rates.csv')

# Convert fundingRate to float and timestamp to datetime
df['fundingRate'] = df['fundingRate'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Group by coin and calculate metrics
summary = df.groupby('coin').agg(
    avg_abs_spread = ('fundingRate', lambda x: np.mean(np.abs(x))),
    sharpe_ratio = ('fundingRate', lambda x: np.mean(x) / np.std(x) if np.std(x) > 0 else 0)
).reset_index()

# Sort for plotting
summary_sorted_sharpe = summary.sort_values('sharpe_ratio', ascending=False)
summary_sorted_spread = summary.sort_values('avg_abs_spread', ascending=False)

# Bar chart: Sharpe Ratio
plt.figure(figsize=(12,5))
plt.bar(summary_sorted_sharpe['coin'], summary_sorted_sharpe['sharpe_ratio'], color='royalblue')
plt.title('Sharpe Ratio by Coin')
plt.xlabel('Coin')
plt.ylabel('Sharpe Ratio')
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig('T2/sharpe_ratio_bar.png')
plt.close()

# Bar chart: Average Absolute Spread
plt.figure(figsize=(12,5))
plt.bar(summary_sorted_spread['coin'], summary_sorted_spread['avg_abs_spread'], color='skyblue')
plt.title('Average Absolute Spread by Coin')
plt.xlabel('Coin')
plt.ylabel('Average Absolute Spread')
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig('T2/avg_abs_spread_bar.png')
plt.close()

# Scatter plot: Sharpe vs Average Abs Spread
plt.figure(figsize=(10,5))
plt.scatter(summary['avg_abs_spread'], summary['sharpe_ratio'], color='blue')
for i, row in summary.iterrows():
    plt.text(row['avg_abs_spread'], row['sharpe_ratio'], row['coin'], fontsize=8, alpha=0.7)

# Regression line
X = summary['avg_abs_spread'].values.reshape(-1, 1)
y = summary['sharpe_ratio'].values
reg = LinearRegression().fit(X, y)
y_pred = reg.predict(X)
plt.plot(summary['avg_abs_spread'], y_pred, color='red', linestyle='dashed')

plt.title('Sharpe vs Average Abs Spread')
plt.xlabel('Average Absolute Spread')
plt.ylabel('Sharpe Ratio')
plt.tight_layout()
plt.savefig('T2/sharpe_vs_spread_scatter.png')
plt.close()

print('Analysis complete. Plots saved in T2/') 