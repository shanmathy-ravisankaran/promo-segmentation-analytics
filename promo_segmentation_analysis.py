# Smart Promo Analytics - Year-wise Discount Segmentation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configure plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Simulate Data
np.random.seed(42)
n_customers = 500

data = pd.DataFrame({
    'customer_id': [f'C{str(i).zfill(4)}' for i in range(1, n_customers + 1)],
    'segment': np.random.choice(['Loyal', 'New', 'High-Value', 'At-Risk'], size=n_customers, p=[0.4, 0.3, 0.2, 0.1]),
    'discount': np.random.choice([0, 5, 10, 15, 20, 25, 30], size=n_customers),
    'order_value': np.round(np.random.uniform(20, 300, size=n_customers), 2),
    'year': np.random.choice([2021, 2022, 2023], size=n_customers)  # 👈 Add Year Column
})

data['profit_margin'] = np.where(
    data['discount'] == 0,
    0.3,
    np.maximum(0.05, 0.3 - (data['discount'] / 100))
)
data['profit'] = np.round(data['order_value'] * data['profit_margin'], 2)

def simulate_repeat(row):
    base = 0.6 if row['segment'] == 'Loyal' else 0.3
    modifier = -0.01 * row['discount']
    return np.random.rand() < (base + modifier)

data['repeat_purchase'] = data.apply(simulate_repeat, axis=1)

#  Group by segment and year
summary = data.groupby(['segment', 'year']).agg({
    'order_value': 'mean',
    'profit': 'mean',
    'discount': 'mean',
    'repeat_purchase': 'mean'
}).rename(columns={
    'order_value': 'Avg Order ($)',
    'profit': 'Avg Profit ($)',
    'discount': 'Avg Discount (%)',
    'repeat_purchase': 'Repeat Rate'
}).reset_index()

print("\nSegment Summary by Year:")
print(summary)

#  Plot: Avg Profit by Segment per Year
plt.figure(figsize=(12, 7))
ax = sns.barplot(data=summary, x='segment', y='Avg Profit ($)', hue='year', palette='Set2')
plt.title('Avg Profit by Segment Across Years')
plt.xlabel('Customer Segment')
plt.ylabel('Avg Profit ($)')

# Add value labels
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3)

plt.legend(title='Year')
plt.tight_layout()

#  Save the chart as PNG
plt.savefig("segment_profit_by_year.png", dpi=300)
plt.show()
# Additional metrics visualized in bar plots
metrics = ['Avg Order ($)', 'Avg Discount (%)', 'Repeat Rate']
for metric in metrics:
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=summary, x='segment', y=metric, hue='year', palette='pastel')
    plt.title(f'{metric} by Segment Across Years')
    plt.xlabel('Customer Segment')
    plt.ylabel(metric)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=3)
    plt.legend(title='Year')
    plt.tight_layout()
    plt.savefig(f"{metric.replace(' ', '_').replace('($)', '').strip()}.png", dpi=300)
    plt.show()
summary_by_year = data.groupby(['segment', 'year']).agg({
    'order_value': 'mean',
    'profit': 'mean',
    'discount': 'mean',
    'repeat_purchase': 'mean'
}).reset_index()

summary_by_year.columns = ['segment', 'year', 'Avg Order ($)', 'Avg Profit ($)', 'Avg Discount (%)', 'Repeat Rate']

print("\nSegment Summary by Year:")
print(summary_by_year)

summary_by_year.to_excel("segment_summary_by_year.xlsx", index=False)

# Identify top profit segment by year
top_profits = summary.loc[summary.groupby('year')['Avg Profit ($)'].idxmax()]
print("\nTop Segment by Year:")
print(top_profits[['year', 'segment', 'Avg Profit ($)']])

import os
print("Saved to:", os.getcwd())
