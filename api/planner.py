import pandas as pd
import numpy as np
from typing import Dict, Any
import ml_utils

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

def planner(budget: float, people: int, diet_type: str, goal: str, df: pd.DataFrame, use_ml: bool = True) -> Dict[str, Any]:
    """
    Generates a grocery plan using ML-powered intelligent selection or greedy fallback.
    
    Args:
        budget: Weekly budget in dollars
        people: Number of people
        diet_type: Diet preference (veg/non-veg/vegan)
        goal: Health goal (balanced/high_protein/low_sugar)
        df: Product dataframe
        use_ml: Use ML models for selection (default True)
    """
    
    # 1. Filter by Diet
    filtered = df.copy()
    diet_lower = diet_type.lower()
    
    # Map "vegan" or "vegetarian" to the "Vegetarian" value in dataset
    # Ensure we don't accidentally match "non-vegetarian"
    if "veg" in diet_lower and "non" not in diet_lower:
        if "veg_nonveg" in filtered.columns:
            filtered = filtered[filtered["veg_nonveg"].astype(str).str.lower().str.contains("veg")]
    
    # 2. Calculate Value Metric with ML or Fallback
    filtered = filtered[filtered["price_per_100g"] > 0.01].copy()
    
    # Try ML-based scoring
    if use_ml and ml_utils.models_available():
        print("🤖 Using ML-powered product selection")
        
        # Get ML predictions
        ml_score = ml_utils.calculate_ml_score(filtered)
        
        if ml_score is not None:
            # Use ML score as base
            filtered["value_metric"] = ml_score
            
            # Goal-specific ML adjustments
            if goal == "high_protein":
                if "protein" in filtered.columns:
                    protein_bonus = (filtered["protein"] / filtered["price_per_100g"]) * 0.7
                    filtered["value_metric"] += protein_bonus
                    
            elif goal == "low_sugar":
                if "sugar" in filtered.columns:
                    sugar_penalty = (filtered["sugar"] / filtered["price_per_100g"]) * 0.7
                    filtered["value_metric"] -= sugar_penalty
            
            # UX: Boost non-veg items if requested
            if "non" in diet_lower and "veg_nonveg" in filtered.columns:
                mask = filtered["veg_nonveg"] == "Non-Vegetarian"
                filtered.loc[mask, "value_metric"] *= 5.0
        else:
            # ML failed, fall back to traditional method
            use_ml = False
    else:
        use_ml = False
    
    # Fallback to traditional greedy method
    if not use_ml:
        print("📊 Using traditional greedy selection")
        filtered["value_metric"] = filtered["nutri_score_app"] / filtered["price_per_100g"]
        
        # Goal Adjustments
        if goal == "high_protein":
            if "protein" in filtered.columns:
                filtered["value_metric"] += (filtered["protein"] / filtered["price_per_100g"]) * 0.5
                
        elif goal == "low_sugar":
            if "sugar" in filtered.columns:
                filtered["value_metric"] -= (filtered["sugar"] / filtered["price_per_100g"]) * 0.5

        # UX Improvement for non-veg
        if "non" in diet_lower and "veg_nonveg" in filtered.columns:
            mask = filtered["veg_nonveg"] == "Non-Vegetarian"
            filtered.loc[mask, "value_metric"] *= 10.0
    
    # 3. Sort by Value Metric (Descending)
    candidates = filtered.sort_values(by="value_metric", ascending=False)
    
    # 4. Intelligent Selection with Variety Optimization
    basket = []
    current_spend = 0.0
    
    # Cluster tracking for variety
    cluster_spending = {}
    max_cluster_budget = budget * 0.35 # Max 35% of budget per cluster
    
    if use_ml and "cluster_label" in filtered.columns:
        max_cluster_budget = budget * 0.35
    else:
        max_cluster_budget = budget
        
    print(f"DEBUG: Starting selection loop. Budget: {budget}, Max Cluster: {max_cluster_budget}")
    
    for i, (_, product) in enumerate(candidates.iterrows()):
        # Use item price if available, otherwise fallback (shouldn't happen with enhanced data)
        price = product.get("price_per_item", product["price_per_100g"])
        
        # Debug first few items
        if i < 5:
            print(f"DEBUG Item {i}: {product.get('product_name')} - Price: {price} - Cluster: {product.get('cluster_label')}")
        
        # Skip if price is missing or zero
        if pd.isna(price) or price <= 0:
            if i < 5: print("DEBUG: Skipped due to invalid price")
            continue
            
        if current_spend + price <= budget:
            # Check cluster limit
            cluster = product.get("cluster_label", "Uncategorized")
            current_cluster_spend = cluster_spending.get(cluster, 0.0)
            
            if current_cluster_spend + price <= max_cluster_budget:
                # Add to basket
                cluster_spending[cluster] = cluster_spending.get(cluster, 0) + price
        
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
    processing_counts = {}
    
    for item in basket:
        qty = item["quantity_units"]
        totals["calories"] += item["_calories"] * qty
        totals["protein"] += item["_protein"] * qty
        totals["fiber"] += item["_fiber"] * qty
        
        # Cluster breakdown
        c_lbl = item.get("cluster_label", "Unknown")
        cluster_counts[c_lbl] = cluster_counts.get(c_lbl, 0) + qty
        
        # Processing breakdown (estimate based on category)
        category = item.get("category", "Unknown")
        if "Frozen" in category or "Snack" in category:
            processing_level = "Processed"
        elif "Meat" in category or "Dairy" in category:
            processing_level = "Minimally Processed"
        else:
            processing_level = "Whole Foods"
        processing_counts[processing_level] = processing_counts.get(processing_level, 0) + qty

    # Round totals
    totals["calories"] = round(totals["calories"])
    totals["protein"] = round(totals["protein"])
    totals["fiber"] = round(totals["fiber"])
    
    # Calculate coverage (daily needs for 'people' over a week)
    # Assume 2000 cal/day, 50g protein/day per person
    daily_cal_per_person = 2000
    daily_protein_per_person = 50
    total_days = 7  # weekly plan
    
    target_calories = daily_cal_per_person * people * total_days
    target_protein = daily_protein_per_person * people * total_days
    
    coverage = {
        "calories": {
            "actual": totals["calories"],
            "target": target_calories,
            "percentage": round((totals["calories"] / target_calories) * 100, 1) if target_calories > 0 else 0
        },
        "protein": {
            "actual": totals["protein"],
            "target": target_protein,
            "percentage": round((totals["protein"] / target_protein) * 100, 1) if target_protein > 0 else 0
        }
    }
    
    # Calculate cost savings
    # Estimate: typical basket with same nutrition would cost ~18% more
    # (based on users buying branded/convenience items vs optimized selection)
    typical_cost = totals["total_spent"] * 1.18
    savings_amount = typical_cost - totals["total_spent"]
    savings_percentage = round((savings_amount / typical_cost) * 100, 1) if typical_cost > 0 else 0
    
    savings = {
        "amount": round(savings_amount, 2),
        "percentage": savings_percentage,
        "typical_cost": round(typical_cost, 2)
    }
    
    # Clean up basket (remove internal fields)
    for item in basket:
        item["estimated_cost"] = round(item["estimated_cost"], 2)
        del item["_calories"]
        del item["_protein"]
        del item["_fiber"]

    return {
        "inputs": { "budget": budget, "people": people, "dietType": diet_type, "goal": goal },
        "items": basket,
        "totals": totals,
        "coverage": coverage,
        "savings": savings,
        "clusterBreakdown": cluster_counts,
        "processingBreakdown": processing_counts
    }
