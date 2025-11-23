import pandas as pd
import numpy as np
from typing import Dict, Any

def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the scored dataset.
    """
    try:
        df = pd.read_csv(csv_path)
        # Ensure product_id is int
        if "product_id" in df.columns:
            df["product_id"] = df["product_id"].astype(int)
        return df
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return pd.DataFrame()

def planner(budget: float, people: int, diet_type: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates a grocery plan using greedy selection based on value-for-money.
    """
    
    # 1. Filter by Diet
    filtered = df.copy()
    diet_lower = diet_type.lower()
    
    # Map "vegan" or "vegetarian" to the "Vegetarian" value in dataset
    # Ensure we don't accidentally match "non-vegetarian"
    if "veg" in diet_lower and "non" not in diet_lower:
        if "veg_nonveg" in filtered.columns:
            filtered = filtered[filtered["veg_nonveg"].astype(str).str.lower().str.contains("veg")]
    
    # 2. Calculate Value Metric
    # Metric = nutri_score_app / price_per_100g
    # Avoid division by zero
    filtered = filtered[filtered["price_per_100g"] > 0.01].copy()
    filtered["value_metric"] = filtered["nutri_score_app"] / filtered["price_per_100g"]
    
    # UX Improvement: If diet is explicitly Non-Vegetarian, boost non-veg items
    # so they actually appear in the basket (otherwise cheap staples dominate)
    if "non" in diet_lower and "veg_nonveg" in filtered.columns:
        mask = filtered["veg_nonveg"] == "Non-Vegetarian"
        filtered.loc[mask, "value_metric"] *= 10.0 # 10x boost to ensure meat is picked
    
    # 3. Sort by Value Metric (Descending)
    candidates = filtered.sort_values(by="value_metric", ascending=False)
    
    # 4. Greedy Selection
    basket = []
    total_spent = 0.0
    
    # We want some variety, so let's limit quantity per item
    # And maybe try to pick from different clusters?
    # For now, simple greedy loop
    
    # Convert to list of dicts for faster iteration
    candidate_items = candidates.to_dict("records")
    
    # Track counts to ensure variety (max 5 units per item)
    item_counts = {}
    
    for item in candidate_items:
        price = item["price_per_100g"]
        
        # If we can afford it
        if total_spent + price <= budget:
            p_id = item["product_id"]
            current_count = item_counts.get(p_id, 0)
            
            if current_count < 5: # Max 5 units
                # Add to basket
                # Check if already in basket to update quantity
                existing = next((x for x in basket if x["product_id"] == p_id), None)
                
                if existing:
                    existing["quantity_units"] += 1
                    existing["estimated_cost"] += price
                else:
                    basket.append({
                        "product_id": p_id,
                        "product_name": item.get("product_name"),
                        "store": item.get("store"),
                        "category": item.get("category"),
                        "cluster_label": item.get("cluster_label"),
                        "health_score": item.get("health_score"),
                        "nutri_score_app": item.get("nutri_score_app"),
                        "price_per_100g": price,
                        "quantity_units": 1,
                        "estimated_cost": price,
                        # Keep raw data for totals
                        "_calories": item.get("calories", 0),
                        "_protein": item.get("protein", 0),
                        "_fiber": item.get("fiber", 0)
                    })
                
                total_spent += price
                item_counts[p_id] = current_count + 1
        
        # Stop if we are very close to budget (e.g. < $0.5 left)
        if budget - total_spent < 0.5:
            break
            
    # 5. Compute Totals
    totals = {
        "total_spent": round(total_spent, 2),
        "budget": budget,
        "calories": 0,
        "protein": 0,
        "fiber": 0
    }
    
    cluster_counts = {}
    
    for item in basket:
        qty = item["quantity_units"]
        totals["calories"] += item["_calories"] * qty
        totals["protein"] += item["_protein"] * qty
        totals["fiber"] += item["_fiber"] * qty
        
        # Cluster breakdown
        c_lbl = item.get("cluster_label", "Unknown")
        cluster_counts[c_lbl] = cluster_counts.get(c_lbl, 0) + qty

    # Round totals
    totals["calories"] = round(totals["calories"])
    totals["protein"] = round(totals["protein"])
    totals["fiber"] = round(totals["fiber"])
    
    # Clean up basket (remove internal fields)
    for item in basket:
        item["estimated_cost"] = round(item["estimated_cost"], 2)
        del item["_calories"]
        del item["_protein"]
        del item["_fiber"]

    return {
        "inputs": { "budget": budget, "people": people, "dietType": diet_type },
        "items": basket,
        "totals": totals,
        "clusterBreakdown": cluster_counts
    }
