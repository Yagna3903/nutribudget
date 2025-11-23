import pandas as pd
import os
import numpy as np

# Paths
RAW_PATH = "data-ml/raw/canada_grocery_nutrition_5000.csv"
PROCESSED_DIR = "data-ml/processed"
OUTPUT_PATH = os.path.join(PROCESSED_DIR, "products_with_clusters.csv")

# Create directory if not exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Load raw data
print(f"Loading {RAW_PATH}...")
df = pd.read_csv(RAW_PATH)

# Add cluster columns
print("Adding cluster columns...")
# Assign random clusters 0-4
np.random.seed(42)
df["cluster"] = np.random.randint(0, 5, size=len(df))

# Map clusters to labels
cluster_labels = {
    0: "High-Protein Staples",
    1: "High-Sugar Snacks",
    2: "Balanced Meals",
    3: "Low-Carb Veggies",
    4: "Energy Dense"
}
df["cluster_label"] = df["cluster"].map(cluster_labels)

# Save
print(f"Saving to {OUTPUT_PATH}...")
df.to_csv(OUTPUT_PATH, index=True) # Keep index as it's used for product_id in planner.py
print("Done.")
