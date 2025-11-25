from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

from planner import load_dataset, planner

app = Flask(__name__)

# CORS configuration for local dev and production
CORS(app, origins=[
    "http://localhost:3000",  # Local development
    "https://nutribudget-web.vercel.app",  # Production (update this after Vercel deployment)
    "https://*.vercel.app",  # Vercel preview deployments
], supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to CSV (in api/data folder for deployment)
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "foods_enhanced.csv",
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

    - Validates all input parameters comprehensively
    - Reads dietType and goal with validation
    - Delegates to planner() to build a response that matches API_CONTRACT.md.
    """
    body = request.get_json(force=True) or {}

    # Validate required fields
    required_fields = ["budget", "people", "dietType", "goal"]
    missing_fields = [field for field in required_fields if field not in body]
    if missing_fields:
        logger.warning(f"Missing required fields: {missing_fields}")
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    try:
        budget = float(body.get("budget", 0))
        people = int(body.get("people", 1))
        diet_type = str(body.get("dietType", "veg")).lower()
        goal = str(body.get("goal", "balanced")).lower()
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid request body: {e}")
        return jsonify({
            "error": "Invalid data types",
            "message": "budget must be a number, people must be an integer"
        }), 400

    # Validate budget
    if budget <= 0:
        logger.warning(f"Invalid budget: {budget}")
        return jsonify({
            "error": "Invalid budget",
            "message": "Budget must be greater than 0"
        }), 400
    
    if budget <= 5:
        logger.info(f"Very low budget: {budget}")
        return jsonify({
            "error": "Budget too low",
            "message": "Budget must be greater than $5 to meet basic nutrition needs."
        }), 400
    
    if budget > 1000:
        logger.warning(f"Very high budget: {budget}")
        return jsonify({
            "error": "Budget too high",
            "message": "Budget must be less than $1000. Please contact support for larger budgets."
        }), 400

    # Validate people
    if people < 1:
        logger.warning(f"Invalid people count: {people}")
        return jsonify({
            "error": "Invalid people count",
            "message": "Number of people must be at least 1"
        }), 400
    
    if people > 20:
        logger.warning(f"Very large household: {people}")
        return jsonify({
            "error": "Household too large",
            "message": "Maximum supported household size is 20 people"
        }), 400

    # Validate diet type
    valid_diet_types = ["veg", "vegetarian", "nonveg", "non-veg", "non_veg", "mixed", "vegan"]
    if diet_type not in valid_diet_types:
        logger.warning(f"Invalid diet type: {diet_type}")
        return jsonify({
            "error": "Invalid diet type",
            "message": f"dietType must be one of: {', '.join(valid_diet_types)}",
            "received": diet_type
        }), 400

    # Validate goal
    valid_goals = ["balanced", "high_protein", "low_sugar"]
    if goal not in valid_goals:
        logger.warning(f"Invalid goal: {goal}")
        return jsonify({
            "error": "Invalid goal",
            "message": f"goal must be one of: {', '.join(valid_goals)}",
            "received": goal
        }), 400
    
    logger.info(f"Planning for budget=${budget}, people={people}, diet={diet_type}, goal={goal}")
    
    try:
        result = planner(budget, people, diet_type, goal, df)
        logger.info(f"Plan generated: {len(result['items'])} items, total cost=${result['totals']['total_spent']:.2f}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in planner: {e}")
        return jsonify({
            "error": "Failed to generate plan",
            "message": "An error occurred while generating your meal plan. Please try again.",
            "details": str(e) if app.debug else None
        }), 500


# --- Smart Chef Integration ---
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
# Ideally, this should be an environment variable.
# For now, we'll check for the env var, and if missing, log a warning.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY not found in environment variables. Smart Chef features will fail.")

@app.route("/api/recipes", methods=["POST"])
def api_recipes():
    """
    POST /api/recipes
    Generates recipes based on the provided list of ingredients (from the basket).
    """
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "Configuration Error",
            "message": "Smart Chef is not configured (missing API Key)."
        }), 503

    body = request.get_json(force=True) or {}
    items = body.get("items", [])
    
    if not items or len(items) == 0:
        return jsonify({
            "error": "No items provided",
            "message": "Please provide a list of ingredients."
        }), 400

    # Extract just the product names for the prompt
    # Handle both string list and object list (if full basket items are sent)
    ingredient_names = []
    for item in items:
        if isinstance(item, str):
            ingredient_names.append(item)
        elif isinstance(item, dict) and "product_name" in item:
            ingredient_names.append(item["product_name"])
    
    ingredients_str = ", ".join(ingredient_names[:20]) # Limit to top 20 to avoid huge prompts

    try:
        # Switching to gemini-flash-latest as it is explicitly available for this key
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are a creative chef helping a budget-conscious user.
        Create 3 simple, healthy, and delicious recipes using a subset of these ingredients: {ingredients_str}.
        You can assume they have basic pantry staples (oil, salt, pepper, water).
        
        Format the output strictly as a JSON list of objects with these keys:
        - name: Recipe Name
        - time: Preparation time (e.g., "30 mins")
        - difficulty: "Easy", "Medium", or "Hard"
        - ingredients: List of strings (ingredients used)
        - instructions: List of strings (step-by-step instructions)
        - calories: Approximate calories per serving (number)
        
        Do not include markdown formatting (like ```json). Just return the raw JSON string.
        """
        
        response = model.generate_content(prompt)
        
        # Clean up response if it contains markdown code blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        import json
        recipes = json.loads(text)
        
        return jsonify({"recipes": recipes})
        
    except Exception as e:
        logger.error(f"Smart Chef Error: {e}", exc_info=True)
        return jsonify({
            "error": "Generation Failed",
            "message": f"Chef is busy! Error: {str(e)}",
            "details": str(e)
        }), 500


@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {
            "status": "NutriBudget backend running",
            "endpoints": ["/health", "/api/foods", "/api/plan", "/api/stats", "/api/debug-products"],
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
