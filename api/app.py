from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

from planner import load_dataset, planner

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to CSV (relative to backend folder)
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data-ml",
    "raw",
    "canada_grocery_nutrition_5000.csv",
)

# Load dataset once at startup
df = load_dataset(DATA_PATH)


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """
    return jsonify({"status": "ok"})


@app.route("/api/debug-products", methods=["GET"])
def debug_products():
    """
    Simple debug route to confirm backend + data loading work.
    Returns the first 20 rows as JSON.
    """
    sample = df.head(20).to_dict(orient="records")
    return jsonify(sample)


@app.route("/api/foods", methods=["GET"])
def api_foods():
    """
    GET /api/foods - Search and filter products.
    
    Query params:
    - veg_nonveg: filter by diet type (e.g., "veg")
    - max_price_per_100g: maximum price per 100g
    - cluster: filter by cluster ID
    - store: filter by store name
    - limit: max number of results (default 100)
    """
    try:
        filtered = df.copy()
        
        # Apply filters
        if "veg_nonveg" in request.args:
            veg_type = request.args.get("veg_nonveg").lower()
            filtered = filtered[filtered["veg_nonveg"].astype(str).str.lower().str.contains(veg_type)]
        
        if "max_price_per_100g" in request.args:
            max_price = float(request.args.get("max_price_per_100g"))
            filtered = filtered[filtered["price_per_100g"] <= max_price]
        
        if "cluster" in request.args:
            cluster_id = int(request.args.get("cluster"))
            filtered = filtered[filtered["cluster"] == cluster_id]
        
        if "store" in request.args:
            store_name = request.args.get("store").lower()
            filtered = filtered[filtered["store"].astype(str).str.lower().str.contains(store_name)]
        
        # Limit results
        limit = int(request.args.get("limit", 100))
        filtered = filtered.head(limit)
        
        results = filtered.to_dict(orient="records")
        return jsonify({"count": len(results), "items": results})
        
    except Exception as e:
        logger.error(f"Error in /api/foods: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/api/stats", methods=["GET"])
def api_stats():
    """
    GET /api/stats - High-level statistics for charts.
    
    Returns:
    - Cluster distribution (count and avg price per cluster)
    - Category distribution (count and avg price per category)
    - Overall stats (total products, avg price, etc.)
    """
    try:
        stats = {}
        
        # Overall stats
        stats["total_products"] = len(df)
        stats["avg_price_per_100g"] = round(df["price_per_100g"].mean(), 2)
        stats["avg_calories"] = round(df["calories"].mean(), 1)
        stats["avg_protein"] = round(df["protein"].mean(), 1)
        
        # Cluster distribution
        if "cluster" in df.columns:
            cluster_stats = df.groupby("cluster").agg({
                "product_id": "count",
                "price_per_100g": "mean"
            }).reset_index()
            cluster_stats.columns = ["cluster", "count", "avg_price"]
            
            # Add cluster labels if available
            if "cluster_label" in df.columns:
                labels = df.groupby("cluster")["cluster_label"].first()
                cluster_stats["label"] = cluster_stats["cluster"].map(labels)
            
            stats["cluster_distribution"] = cluster_stats.to_dict(orient="records")
        
        # Category distribution
        if "category" in df.columns:
            category_stats = df.groupby("category").agg({
                "product_id": "count",
                "price_per_100g": "mean"
            }).reset_index()
            category_stats.columns = ["category", "count", "avg_price"]
            category_stats = category_stats.sort_values("count", ascending=False).head(10)
            stats["category_distribution"] = category_stats.to_dict(orient="records")
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error in /api/stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/plan", methods=["POST"])
def api_plan():
    """
    POST /api/plan implementation for Phase 1.

    - Validates basic input (budget > 0, people >= 1).
    - Reads dietType and goal.
    - Delegates to planner() to build a response that matches API_CONTRACT.md.
    """
    body = request.get_json(force=True) or {}

    try:
        budget = float(body.get("budget", 0))
        people = int(body.get("people", 1))
        diet_type = str(body.get("dietType", "veg"))
        goal = str(body.get("goal", "balanced"))
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid request body: {e}")
        return jsonify({"error": "Invalid request body"}), 400

    if budget <= 0 or people < 1:
        logger.warning(f"Invalid parameters: budget={budget}, people={people}")
        return jsonify({"error": "budget must be > 0 and people must be >= 1"}), 400
    
    # Handle edge cases
    if budget < 5:
        logger.info(f"Very low budget: {budget}")
        return jsonify({
            "error": "Budget too low",
            "message": "Budget must be at least $5 to meet basic nutrition needs."
        }), 400
    
    logger.info(f"Planning for budget=${budget}, people={people}, diet={diet_type}, goal={goal}")
    
    try:
        result = planner(budget, people, diet_type, goal, df)
        logger.info(f"Plan generated: {len(result['basket'])} items, total cost=${result['totals']['cost']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in planner: {e}")
        return jsonify({"error": "Failed to generate plan", "details": str(e)}), 500


@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {
            "status": "NutriBudget backend running",
            "endpoints": ["/health", "/api/foods", "/api/plan", "/api/stats", "/api/debug-products"],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
