import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create sample data for visualization
np.random.seed(42)

# Generate sample royalty data
n_samples = 1000
artists = [f"Artist_{i:03d}" for i in range(1, 51)]
channels = ['Streaming', 'Radio', 'TV/Film', 'Digital Download', 'Physical Sales', 'Live Performance', 'Sync License']
regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa', 'Global']

data = {
    'artist_name': np.random.choice(artists, n_samples),
    'licensing_channel': np.random.choice(channels, n_samples, p=[0.4, 0.15, 0.1, 0.15, 0.05, 0.1, 0.05]),
    'region': np.random.choice(regions, n_samples, p=[0.3, 0.25, 0.2, 0.1, 0.05, 0.05, 0.05]),
    'royalty_amount': np.random.exponential(scale=50, size=n_samples) * np.random.choice([1, 2.5, 5, 3, 4, 1.5, 8], n_samples),
    'payment_status': np.random.choice(['Paid', 'Pending', 'Processing', 'Hold', 'Disputed'], n_samples, p=[0.7, 0.15, 0.08, 0.05, 0.02])
}

df = pd.DataFrame(data)

# Create images directory
os.makedirs('images', exist_ok=True)

# 1. Revenue by Licensing Channel
plt.figure(figsize=(12, 6))
channel_revenue = df.groupby('licensing_channel')['royalty_amount'].sum().sort_values(ascending=True)
bars = plt.barh(channel_revenue.index, channel_revenue.values, color=sns.color_palette("viridis", len(channel_revenue)))
plt.title('Total Revenue by Licensing Channel', fontsize=14, fontweight='bold')
plt.xlabel('Revenue ($)')
for i, (index, value) in enumerate(channel_revenue.items()):
    plt.text(value + max(channel_revenue) * 0.01, i, f'${value:,.0f}', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('images/revenue_by_channel.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Top Artists by Revenue
plt.figure(figsize=(12, 6))
top_artists = df.groupby('artist_name')['royalty_amount'].sum().nlargest(10)
plt.bar(range(len(top_artists)), top_artists.values, color=sns.color_palette("plasma", len(top_artists)))
plt.title('Top 10 Artists by Total Revenue', fontsize=14, fontweight='bold')
plt.ylabel('Revenue ($)')
plt.xticks(range(len(top_artists)), top_artists.index, rotation=45, ha='right')
plt.tight_layout()
plt.savefig('images/top_artists.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Regional Revenue Distribution
plt.figure(figsize=(10, 8))
region_data = df.groupby('region')['royalty_amount'].sum()
colors = sns.color_palette("Set3", len(region_data))
plt.pie(region_data.values, labels=region_data.index, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Revenue Distribution by Region', fontsize=14, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('images/regional_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Payment Status Distribution
plt.figure(figsize=(10, 6))
payment_data = df.groupby('payment_status').size()
plt.bar(payment_data.index, payment_data.values, color=sns.color_palette("coolwarm", len(payment_data)))
plt.title('Transaction Count by Payment Status', fontsize=14, fontweight='bold')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/payment_status.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Royalty Amount Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['royalty_amount'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribution of Royalty Amounts', fontsize=14, fontweight='bold')
plt.xlabel('Royalty Amount ($)')
plt.ylabel('Frequency')
plt.yscale('log')
plt.tight_layout()
plt.savefig('images/royalty_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Executive Dashboard
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Channel revenue (top left)
ax1 = fig.add_subplot(gs[0, :2])
channel_data = df.groupby('licensing_channel')['royalty_amount'].sum().sort_values(ascending=True)
bars = ax1.barh(channel_data.index, channel_data.values, color=sns.color_palette("viridis", len(channel_data)))
ax1.set_title('Revenue by Channel', fontweight='bold')
ax1.set_xlabel('Revenue ($)')

# Top artists (top right)
ax2 = fig.add_subplot(gs[0, 2])
top_5 = df.groupby('artist_name')['royalty_amount'].sum().nlargest(5)
ax2.bar(range(len(top_5)), top_5.values, color=sns.color_palette("plasma", len(top_5)))
ax2.set_title('Top 5 Artists', fontweight='bold')
ax2.set_xticks(range(len(top_5)))
ax2.set_xticklabels(top_5.index, rotation=45, ha='right', fontsize=8)

# Regional pie chart (middle left)  
ax3 = fig.add_subplot(gs[1, 0])
region_data = df.groupby('region')['royalty_amount'].sum()
ax3.pie(region_data.values, labels=region_data.index, autopct='%1.0f%%', 
        colors=sns.color_palette("Set3", len(region_data)))
ax3.set_title('Regional Revenue', fontweight='bold')

# Payment status (middle center)
ax4 = fig.add_subplot(gs[1, 1])
payment_data = df.groupby('payment_status').size()
ax4.bar(payment_data.index, payment_data.values, color=sns.color_palette("coolwarm", len(payment_data)))
ax4.set_title('Payment Status', fontweight='bold')
ax4.tick_params(axis='x', rotation=45)

# Revenue histogram (middle right)
ax5 = fig.add_subplot(gs[1, 2])
ax5.hist(df['royalty_amount'], bins=30, alpha=0.7, color='skyblue')
ax5.set_title('Revenue Distribution', fontweight='bold')
ax5.set_xlabel('Amount ($)')

# Summary stats (bottom)
ax6 = fig.add_subplot(gs[2, :])
stats_text = f"""
Key Statistics:
• Total Revenue: ${df['royalty_amount'].sum():,.0f}
• Average Transaction: ${df['royalty_amount'].mean():.2f}
• Total Transactions: {len(df):,}
• Unique Artists: {df['artist_name'].nunique()}
• Channels: {df['licensing_channel'].nunique()}
• Regions: {df['region'].nunique()}
"""
ax6.text(0.1, 0.5, stats_text, fontsize=12, transform=ax6.transAxes, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
ax6.axis('off')

plt.suptitle('Artist Royalty Analytics Dashboard', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('images/executive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations generated successfully!")
print("Images saved in 'images/' directory:")
print("- revenue_by_channel.png")
print("- top_artists.png") 
print("- regional_distribution.png")
print("- payment_status.png")
print("- royalty_distribution.png")
print("- executive_dashboard.png") 