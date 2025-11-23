import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
import os

# 1. Load Data
DATA_PATH = "outputs/canada_grocery_nutrition_clean.csv"
# Adjust path to be relative to where we run the script (data-ml folder)
if not os.path.exists(DATA_PATH):
    # Try absolute path or relative to project root if run from there
    DATA_PATH = "data-ml/outputs/canada_grocery_nutrition_clean.csv"

if not os.path.exists(DATA_PATH):
    # Fallback for safety
    DATA_PATH = "/Users/yagna/Documents/NutriBudget/nutribudget/data-ml/raw/canada_grocery_nutrition_5000.csv"

print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH)

# 2. Create product_id
df["product_id"] = df.index.astype(int)
print(f"Loaded {len(df)} rows.")

# 3. Engineer Health Score (0-100)
def calculate_raw_health(row):
    score = 0
    # Rewards
    score += row.get("protein", 0) * 2
    score += row.get("fiber", 0) * 3
    # Handle nutriscore if it's not numeric (just in case, though we assume it is)
    ns = row.get("nutriscore", 0)
    if isinstance(ns, str):
        ns_map = {'a': 40, 'b': 30, 'c': 20, 'd': 10, 'e': 0} # Example mapping
        ns = ns_map.get(ns.lower(), 0)
    score += ns * 5
    
    # Penalties
    score -= row.get("sugar", 0) * 1
    score -= row.get("saturated_fat", 0) * 2
    score -= row.get("trans_fat", 0) * 5
    score -= (row.get("sodium", 0) / 100) * 1
    score -= row.get("FPro", 0) * 20
    
    return score

df["raw_health"] = df.apply(calculate_raw_health, axis=1)

# Scale to 0-100
scaler = MinMaxScaler(feature_range=(0, 100))
df["health_score"] = scaler.fit_transform(df[["raw_health"]]).round(1)

# 4. Engineer Affordability Score (0-100)
price_col = "price_per_100g"
# Handle potential zeros
df = df[df[price_col] > 0].copy()

df["price_inv"] = 1 / df[price_col]
scaler_afford = MinMaxScaler(feature_range=(0, 100))
df["affordability_score"] = scaler_afford.fit_transform(df[["price_inv"]]).round(1)

# 5. NutriScore App
df["nutri_score_app"] = (0.6 * df["health_score"] + 0.4 * df["affordability_score"]).round(1)

# 6. Clustering
features = ["calories", "protein", "carbs", "fat", "sugar", "fiber", "FPro", "nutriscore"]
# Ensure all features are numeric
for f in features:
    df[f] = pd.to_numeric(df[f], errors='coerce').fillna(0)

X = df[features]
scaler_cluster = StandardScaler()
X_scaled = scaler_cluster.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

cluster_map = {
    0: "Staples / Mixed",
    1: "Veg & Wholefoods",
    2: "Processed / Snacks",
    3: "High Energy / Fatty"
}
df["cluster_label"] = df["cluster"].map(cluster_map)

# 7. Export
output_cols = [
    "product_id", "product_name", "store", "brand",
    "category", "sub_category", "food_type", "veg_nonveg",
    "calories", "protein", "carbs", "fat", "sugar", "fiber",
    "price_per_gram", "price_per_100g",
    "FPro", "nutriscore",
    "health_score", "affordability_score", "nutri_score_app", "cluster", "cluster_label"
]

# Ensure output directory exists
os.makedirs("outputs", exist_ok=True)
# Also try absolute path if running from weird location
abs_output_dir = "/Users/yagna/Documents/NutriBudget/nutribudget/data-ml/outputs"
os.makedirs(abs_output_dir, exist_ok=True)

final_cols = [c for c in output_cols if c in df.columns]

output_path = "outputs/foods_scored.csv"
df[final_cols].to_csv(output_path, index=False)
# Also save to absolute path to be sure
df[final_cols].to_csv(os.path.join(abs_output_dir, "foods_scored.csv"), index=False)

print(f"Saved to {output_path}")
