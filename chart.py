import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate realistic synthetic data for customer segments
# Creating different customer segments with varying purchase behaviors
segments = []
purchase_amounts = []

# Premium Segment - Higher spending customers
premium_purchases = np.random.gamma(shape=5, scale=50, size=150)
segments.extend(["Premium"] * 150)
purchase_amounts.extend(premium_purchases)

# Standard Segment - Medium spending customers
standard_purchases = np.random.gamma(shape=3, scale=30, size=200)
segments.extend(["Standard"] * 200)
purchase_amounts.extend(standard_purchases)

# Budget Segment - Lower spending customers
budget_purchases = np.random.gamma(shape=2, scale=20, size=180)
segments.extend(["Budget"] * 180)
purchase_amounts.extend(budget_purchases)

# VIP Segment - Highest spending customers
vip_purchases = np.random.gamma(shape=6, scale=70, size=100)
segments.extend(["VIP"] * 100)
purchase_amounts.extend(vip_purchases)

# Create DataFrame
data = pd.DataFrame(
    {"Customer Segment": segments, "Purchase Amount ($)": purchase_amounts}
)

# Set Seaborn style and context for professional appearance
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=0.9)

# Create figure with specified size for 512x512 output
plt.figure(figsize=(8, 8))

# Create boxplot with professional styling
ax = sns.boxplot(
    data=data,
    x="Customer Segment",
    y="Purchase Amount ($)",
    palette="Set2",
    linewidth=2,
    order=["Budget", "Standard", "Premium", "VIP"],
)

# Customize the plot
plt.title(
    "Purchase Amount Distribution by Customer Segment",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.xlabel("Customer Segment", fontsize=13, fontweight="bold")
plt.ylabel("Purchase Amount ($)", fontsize=13, fontweight="bold")

# Rotate x-axis labels for better readability
plt.xticks(rotation=0, ha="center")

# Add grid for better readability
ax.yaxis.grid(True, alpha=0.3)
ax.set_axisbelow(True)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the chart with exact dimensions (512x512 pixels)
# Remove bbox_inches='tight' to maintain exact dimensions
plt.savefig("chart.png", dpi=64)

print("Chart generated successfully: chart.png (512x512 pixels)")
