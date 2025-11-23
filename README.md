# nutribudget
Price-aware nutrition planner using GroceryDB (nutrition + prices) with ML clustering, optimization, a Flask API, and a Next.js dashboard.

# NutriBudget – Global Grocery Optimizer

NutriBudget is a price-aware, nutrition-aware grocery planner.  
It uses real product data (nutrients + price per gram/calorie) from GroceryDB, applies ML clustering and scoring, and recommends a grocery basket that maximizes nutrition under a user’s budget.

- **Inputs:** Budget, household size, diet type, and nutrition goal  
- **Output:** An optimized basket of foods with real prices, nutrient coverage, and health personas  
- **Stack:** Python (pandas, scikit-learn), Flask API, Next.js frontend

---

## 1. Problem & Motivation

Households with tight budgets often end up buying the **cheapest calories**, which are frequently ultra-processed, high in sugar, and low in fibre or protein.  
They rarely see a clear, data-driven answer to questions like:

- “What is the **best nutrition** I can get for **\$X**?”
- “Which products give me **good protein and fibre** without blowing my budget?”
- “How much of my cart is ultra-processed snacks vs staples?”

This affects food security, health outcomes, and inequality.

---

## 2. Solution – What NutriBudget Does

NutriBudget turns grocery data into a **budget-constrained nutrition optimizer**:

1. Uses **GroceryDB (CleanedData)**:
   - Thousands of real supermarket products
   - Nutrients per 100 g (calories, protein, fat, carbs, sugar, fibre, etc.)
   - **Price per gram / price per calorie**
   - Processing score (how ultra-processed each product is)

2. Performs **feature engineering & ML**:
   - Computes a **health score** for each product (protein/fibre up, sugar/fat down)
   - Computes an **affordability score** from price per gram/calorie
   - Combines them into a **nutri_score**
   - Uses **K-Means clustering** to group products into “health personas”  
     (e.g., high-protein staples, high-sugar snacks, low-calorie items, high-fat items)

3. Runs a **budget planner**:
   - Inputs: `budget`, `household size`, `dietType` (veg / non-veg / vegan), `goal` (balanced / high protein / low sugar)
   - Selects products under budget to:
     - Reach calorie and protein targets
     - Maximize overall `nutri_score`
     - Respect diet type and goal preference

4. Exposes this via a **Flask API** and a **Next.js dashboard**:
   - Shows the recommended basket
   - Shows cost vs budget
   - Shows coverage of calories, protein (and optionally fibre)
   - Shows breakdown by health clusters and processing level

---

## 3. Features

**Data & ML**

- Real product-level **nutrient data** and **price per gram/calorie**
- Feature engineering:
  - `health_score` (0–100)
  - `affordability_score` (0–100)
  - `nutri_score` (combined)
- **K-Means clustering** of foods into 4 “health personas”

**Planner**

- Budget-constrained selection of items
- Targets daily calories and protein for the given household size and planning horizon
- Goals:
  - Balanced
  - High protein
  - Low sugar
- Diet filters (veg / non-veg / vegan via category rules)

**API & UI**

- `POST /api/plan` returns a full plan:
  - Basket items (products with units, cost, calories, protein, cluster info)
  - Totals and coverage
  - Cluster breakdown and (optionally) processing breakdown
- Next.js frontend:
  - Input form (budget, people, diet, goal)
  - Basket cards
  - Nutrition coverage bars
  - Simple charts for cost and cluster composition
  - Short explainer & SDG section

---

## 4. Data Source

This project uses the **GroceryDB** dataset by Barabási Lab, specifically the **CleanedData** table.

- Thousands of products from major grocery chains  
- Detailed nutrient information per 100 g  
- **Price per gram** and **price per calorie**  
- Processing score (FPro) and product metadata

> Note: Due to licensing and size, the raw GroceryDB data is **not** included in this repository.  
> You must obtain it yourself from the official GroceryDB source and export the **CleanedData** collection as a CSV.

Place the exported CSV here:

```text
data-ml/raw/grocerydb_cleaned.csv
