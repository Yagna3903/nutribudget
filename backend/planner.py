import pandas as pd
import pulp
from typing import Dict, Any


def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the Canada grocery dataset and add a product_id column.

    Called once from app.py at startup.
    """
    # Option 1: Load pre-clustered dataset directly
    # Note: csv_path argument is currently ignored in favor of the hardcoded path below,
    # or we could update app.py to pass the new path. For now, we override here.
    import os
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "..", "data-ml", "processed", "products_with_clusters.csv")
    
    df = pd.read_csv(csv_path)
    df = df.reset_index().rename(columns={"index": "product_id"})
    return df


def solve_optimization_problem(df: pd.DataFrame, budget: float, people: int, goal: str) -> pd.DataFrame:
    """
    Solves the diet problem using Linear Programming (PuLP).
    
    Variables:
        quantity[i] (Integer) >= 0
        
    Constraints:
        1. Total Cost <= Budget
        2. Total Calories >= Target (2000 * people)
        3. Total Protein >= Target (50g * people)
        
    Objective:
        Maximize Nutritional Value (simplified as Protein/Fiber for now) 
        OR Minimize Cost (if goal is 'budget')
    """
    # Filter out items with missing critical data or zero price
    candidates = df[
        (df["price_per_100g"] > 0) & 
        (df["calories"] > 0)
    ].copy()
    
    # Limit candidates to speed up solver (e.g., top 500 by some metric or random subset)
    # For now, we take a random sample if it's too large to keep it fast for the hackathon
    if len(candidates) > 500:
        candidates = candidates.sample(500, random_state=42)
        
    candidates = candidates.reset_index(drop=True)
    products = candidates.to_dict("records")
    
    # --- 1. Define Problem ---
    prob = pulp.LpProblem("NutriBudget_Optimization", pulp.LpMaximize)
    
    # --- 2. Define Variables ---
    # quantity of each product (integer units)
    # We assume '1 unit' in the dataset is roughly 100g for simplicity in this phase,
    # or we treat the row as "1 serving". 
    # Since prices are "price_per_100g", let's assume decision variable is "number of 100g units".
    quantities = pulp.LpVariable.dicts(
        "qty", 
        [p["product_id"] for p in products], 
        lowBound=0, 
        upBound=10, # Cap at 10 units per item to enforce variety
        cat="Integer"
    )
    
    # --- 3. Define Constraints ---
    
    # Cost Constraint
    prob += pulp.lpSum(
        [p["price_per_100g"] * quantities[p["product_id"]] for p in products]
    ) <= budget, "Total_Cost_Limit"
    
    # Nutrition Targets (Daily * people)
    # Let's plan for 1 day for simplicity
    min_calories = 2000 * people
    min_protein = 50 * people
    
    prob += pulp.lpSum(
        [p["calories"] * quantities[p["product_id"]] for p in products]
    ) >= min_calories, "Min_Calories"
    
    prob += pulp.lpSum(
        [p["protein"] * quantities[p["product_id"]] for p in products]
    ) >= min_protein, "Min_Protein"
    
    # --- 4. Define Objective ---
    # Goal-based objectives
    if goal == "high_protein":
        # Maximize Protein
        prob += pulp.lpSum(
            [p["protein"] * quantities[p["product_id"]] for p in products]
        ), "Maximize_Protein"
        
    elif goal == "low_sugar":
        # Minimize Sugar (which is Maximize negative Sugar)
        # But we need a primary maximization. Let's Maximize (Protein - Sugar)
        prob += pulp.lpSum(
            [(p["protein"] - p["sugar"]) * quantities[p["product_id"]] for p in products]
        ), "Maximize_Protein_Minimize_Sugar"
        
    else: # balanced
        # Maximize a balanced score: Protein + Fiber - Saturated Fat
        prob += pulp.lpSum(
            [
                (p["protein"] + p["fiber"] - p.get("saturated_fat", 0)) * quantities[p["product_id"]] 
                for p in products
            ]
        ), "Maximize_Balanced_Score"
        
    # --- 5. Solve ---
    # Suppress solver output
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # --- 6. Extract Results ---
    if pulp.LpStatus[prob.status] != "Optimal":
        # If infeasible (e.g. budget too low), return empty or fallback
        # For now, return empty to trigger fallback in caller
        return pd.DataFrame()
        
    selected_indices = []
    for p in products:
        qty = quantities[p["product_id"]].varValue
        if qty and qty > 0:
            # We need to store the quantity in the dataframe
            # Since we are returning a dataframe, we'll just return the rows
            # and add a 'quantity' column.
            # Note: The original df might not have 'quantity'.
            p_copy = p.copy()
            p_copy["quantity"] = int(qty)
            selected_indices.append(p_copy)
            
    return pd.DataFrame(selected_indices)


def planner(budget: float, people: int, diet_type: str, goal: str, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Phase 4 Optimized Planner.
    
    Uses Linear Programming to find the optimal basket.
    """

    # --- 1. Basic diet filter ---
    filtered = df.copy()

    # veg / vegan → try to keep vegetarian items if possible
    if diet_type in ("veg", "vegan") and "veg_nonveg" in filtered.columns:
        veg_mask = filtered["veg_nonveg"].astype(str).str.lower().str.contains("veg")
        tmp = filtered[veg_mask]
        if not tmp.empty:
            filtered = tmp

    # if filter removed everything, fall back to full dataset
    if filtered.empty:
        filtered = df.copy()

    # --- 2. Optimization ---
    # Try to solve
    result_df = solve_optimization_problem(filtered, budget, people, goal)
    
    # Fallback if optimization failed (e.g. budget too low)
    if result_df.empty:
        # Fallback to random sample logic (Phase 1 logic)
        sample_size = min(5, len(filtered))
        result_df = filtered.sample(sample_size, random_state=42).copy()
        result_df["quantity"] = 1 # Default to 1 unit
    
    basket = []

    for _, row in result_df.iterrows():
        quantity = int(row.get("quantity", 1))
        unit = "100g" # Since we optimized for 100g units

        price_per_100g = float(row.get("price_per_100g", 0.0))
        cost = price_per_100g * quantity

        calories = float(row.get("calories", 0.0)) * quantity
        protein = float(row.get("protein", 0.0)) * quantity
        carbs = float(row.get("carbs", 0.0)) * quantity
        fat = float(row.get("fat", 0.0)) * quantity
        sugar = float(row.get("sugar", 0.0)) * quantity
        fiber = float(row.get("fiber", 0.0)) * quantity
        fpro = float(row.get("FPro", 0.0))
        
        cluster_id = int(row.get("cluster", 0))
        cluster_lbl = str(row.get("cluster_label", "Placeholder Cluster"))

        basket.append(
            {
                "product_id": int(row["product_id"]),
                "name": str(row.get("product_name", "")),
                "store": str(row.get("store", "")),
                "brand": str(row.get("brand", "")),
                "category": str(row.get("category", "")),
                "sub_category": str(row.get("sub_category", "")),
                "quantity": quantity,
                "unit": unit,
                "cost": round(cost, 2),
                "calories": round(calories, 1),
                "protein": round(protein, 1),
                "carbs": round(carbs, 1),
                "fat": round(fat, 1),
                "sugar": round(sugar, 1),
                "fiber": round(fiber, 1),
                "cluster": cluster_id,
                "cluster_label": cluster_lbl,
                "FPro": round(fpro, 3),
            }
        )

    # --- 3. Totals ---
    totals = {
        "cost": round(sum(item["cost"] for item in basket), 2),
        "calories": round(sum(item["calories"] for item in basket), 1),
        "protein": round(sum(item["protein"] for item in basket), 1),
        "carbs": round(sum(item["carbs"] for item in basket), 1),
        "fat": round(sum(item["fat"] for item in basket), 1),
        "sugar": round(sum(item["sugar"] for item in basket), 1),
        "fiber": round(sum(item["fiber"] for item in basket), 1),
    }

    # --- 4. Coverage (simple targets) ---
    calories_target = 2000 * people
    protein_target = 50 * people

    coverage = {
        "calories": {
            "target": calories_target,
            "actual": totals["calories"],
            "percentage": round((totals["calories"] / calories_target) * 100, 1)
            if calories_target > 0
            else 0.0,
        },
        "protein": {
            "target": protein_target,
            "actual": totals["protein"],
            "percentage": round((totals["protein"] / protein_target) * 100, 1)
            if protein_target > 0
            else 0.0,
        },
    }

    # --- 5. Cluster breakdown ---
    cluster_counts = {}
    cluster_costs = {}
    
    for item in basket:
        c_id = item["cluster"]
        c_lbl = item["cluster_label"]
        key = (c_id, c_lbl)
        
        cluster_counts[key] = cluster_counts.get(key, 0) + 1
        cluster_costs[key] = cluster_costs.get(key, 0.0) + item["cost"]

    cluster_breakdown = []
    total_basket_cost = totals["cost"]
    
    for (c_id, c_lbl), count in cluster_counts.items():
        c_cost = cluster_costs[(c_id, c_lbl)]
        cluster_breakdown.append(
            {
                "cluster": c_id,
                "label": c_lbl,
                "count": count,
                "cost": round(c_cost, 2),
                "percentage": round((c_cost / total_basket_cost) * 100, 1) if total_basket_cost > 0 else 0.0
            }
        )
    
    cluster_breakdown.sort(key=lambda x: x["cluster"])

    # --- 6. Processing breakdown by food_type ---
    processing_breakdown = []
    # Note: 'sample' variable from old code is gone, we use result_df
    if "food_type" in result_df.columns and not result_df.empty:
        tmp = result_df.copy()
        # Cost in result_df is per unit * quantity? No, result_df has 'quantity' and 'price_per_100g'
        # Let's calculate total cost per row for breakdown
        tmp["total_row_cost"] = tmp["price_per_100g"] * tmp["quantity"]
        total_cost = tmp["total_row_cost"].sum()

        for level, grp in tmp.groupby("food_type"):
            lvl_cost = grp["total_row_cost"].sum()
            processing_breakdown.append(
                {
                    "level": str(level),
                    "count": int(grp["quantity"].sum()), # Count is total units
                    "cost": round(lvl_cost, 2),
                    "percentage": round((lvl_cost / total_cost) * 100, 1)
                    if total_cost > 0
                    else 0.0,
                }
            )

    return {
        "basket": basket,
        "totals": totals,
        "coverage": coverage,
        "cluster_breakdown": cluster_breakdown,
        "processing_breakdown": processing_breakdown,
    }
