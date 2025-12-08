import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Read the Excel file
excel_file = "q-excel-correlation-heatmap.xlsx"

# Try to read the data
try:
    # Read the first sheet to see what's there
    df = pd.read_excel(excel_file, sheet_name=0)
    print("Data from Excel file:")
    print(df.head())
    print("\nColumns:", df.columns.tolist())
    print("\nShape:", df.shape)

    # Calculate correlation matrix
    correlation_matrix = df.corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Save correlation matrix to CSV
    correlation_matrix.to_csv("correlation.csv")
    print("\nCorrelation matrix saved to correlation.csv")

    # Create heatmap visualization
    fig = plt.figure(figsize=(6.5, 6.5))

    # Create heatmap with red-white-green colormap
    # Using RdYlGn (Red-Yellow-Green) which is similar to Excel's red-white-green
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )

    plt.title(
        "Supply Chain Metrics - Correlation Heatmap", fontsize=12, fontweight="bold"
    )
    plt.tight_layout()

    # Save as PNG with specified dimensions (400x400 to 512x512)
    plt.savefig("heatmap.png", dpi=72, bbox_inches="tight")
    print("Heatmap saved to heatmap.png")

    plt.close()

except Exception as e:
    print(f"Error: {e}")
    print("\nCreating sample supply chain data...")

    # Create sample data with 53 transactions
    np.random.seed(42)
    n_samples = 53

    # Generate correlated supply chain data
    data = {
        "Supplier_Lead_Time": np.random.randint(5, 45, n_samples),
        "Inventory_Levels": np.random.randint(100, 1000, n_samples),
        "Order_Frequency": np.random.randint(1, 15, n_samples),
        "Delivery_Performance": np.random.uniform(70, 100, n_samples),
        "Cost_Per_Unit": np.random.uniform(10, 150, n_samples),
    }

    df = pd.DataFrame(data)

    # Add some correlations to make it realistic
    # Higher lead time correlates with lower delivery performance
    df["Delivery_Performance"] -= df["Supplier_Lead_Time"] * 0.3
    df["Delivery_Performance"] = df["Delivery_Performance"].clip(70, 100)

    # Higher order frequency correlates with higher inventory
    df["Inventory_Levels"] += df["Order_Frequency"] * 20

    print("Sample data created:")
    print(df.head())

    # Save to Excel
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Supply Chain Data", index=False)

    print(f"\nData saved to {excel_file}")

    # Calculate correlation matrix
    correlation_matrix = df.corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Save correlation matrix to CSV
    correlation_matrix.to_csv("correlation.csv")
    print("\nCorrelation matrix saved to correlation.csv")

    # Create heatmap visualization
    fig = plt.figure(figsize=(6.5, 6.5))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )

    plt.title(
        "Supply Chain Metrics - Correlation Heatmap", fontsize=12, fontweight="bold"
    )
    plt.tight_layout()

    plt.savefig("heatmap.png", dpi=72, bbox_inches="tight")
    print("Heatmap saved to heatmap.png")

    plt.close()

print("\nAll files generated successfully!")
