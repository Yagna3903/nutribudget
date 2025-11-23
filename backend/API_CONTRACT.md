# NutriBudget API Contract

## Purpose

The NutriBudget API provides a budget-constrained nutrition optimization service. Given a budget, household size, diet type, and nutrition goal, it returns an optimized grocery basket that maximizes nutrition while staying within budget constraints.

---

## POST /api/plan

### Request Body

```json
{
  "budget": 40,
  "people": 2,
  "dietType": "veg",
  "goal": "balanced"
}
```

#### Allowed Values

- **budget** (number, required): Budget in CAD. Must be > 0.
- **people** (integer, required): Number of people in household. Must be >= 1.
- **dietType** (string, required): One of:
  - `"veg"` - Vegetarian  
- `"non_veg"` - Non-vegetarian  
- `"vegan"` - Vegan
- **goal** (string, required): Nutrition optimization goal. One of:
  - `"balanced"` - Balanced nutrition
  - `"high_protein"` - High protein focus
  - `"low_sugar"` - Low sugar focus

### Response JSON Shape

```json
{
  "basket": [
    {
      "product_id": 123,
      "name": "Romaine Lettuce 250g",
      "store": "Costco Canada",
      "brand": "Coca-Cola",
      "category": "Produce",
      "sub_category": "Vegetables",
      "quantity": 2,
      "unit": "item",
      "cost": 3.36,
      "calories": 138.4,
      "protein": 7.4,
      "carbs": 22.2,
      "fat": 0.6,
      "sugar": 7.8,
      "fiber": 7.2,
      "cluster": 0,
      "cluster_label": "High-Protein Staples",
      "FPro": 0.285
    }
  ],
  "totals": {
    "cost": 38.5,
    "calories": 4200,
    "protein": 180,
    "carbs": 520,
    "fat": 120,
    "sugar": 95,
    "fiber": 85
  },
  "coverage": {
    "calories": {
      "target": 4800,
      "actual": 4200,
      "percentage": 87.5
    },
    "protein": {
      "target": 200,
      "actual": 180,
      "percentage": 90.0
    }
  },
  "cluster_breakdown": [
    {
      "cluster": 0,
      "label": "High-Protein Staples",
      "count": 5,
      "cost": 15.2,
      "percentage": 39.5
    },
    {
      "cluster": 1,
      "label": "High-Sugar Snacks",
      "count": 2,
      "cost": 8.5,
      "percentage": 22.1
    }
  ],
  "processing_breakdown": [
    {
      "level": "Minimally Processed",
      "count": 4,
      "cost": 12.3,
      "percentage": 31.9
    },
    {
      "level": "Ultra-Processed",
      "count": 3,
      "cost": 26.2,
      "percentage": 68.1
    }
  ]
}

```

#### Response Fields

- **basket** (array): List of selected products with:
- `product_id` - Unique integer identifier for the product (created from the dataframe index in the backend)
  - `name`, `store`, `brand`, `category`, `sub_category` - Product metadata
  - `quantity` - Number of units
  - `unit` - Unit type (typically "item" or "g")
  - `cost` - Total cost in CAD for this item
  - `calories`, `protein`, `carbs`, `fat`, `sugar`, `fiber` - Total nutrients for this item
  - `cluster` - Cluster ID (integer)
  - `cluster_label` - Human-readable cluster name
  - `FPro` - Processing score (0-1, where higher = more processed)

- **totals** (object): Aggregated totals across all basket items
  - `cost` - Total cost in CAD
  - `calories`, `protein`, `carbs`, `fat`, `sugar`, `fiber` - Total nutrients

- **coverage** (object): Target vs actual nutrition coverage
  - Each nutrient has `target`, `actual`, and `percentage` fields

- **cluster_breakdown** (array): Summary by health cluster
  - `cluster` - Cluster ID
  - `label` - Cluster name
  - `count` - Number of items
  - `cost` - Total cost in CAD
  - `percentage` - Percentage of total cost

- **processing_breakdown** (array): Summary by processing level
  - `level` - Processing level name
  - `count` - Number of items
  - `cost` - Total cost in CAD
  - `percentage` - Percentage of total cost

---

## Price Units

All prices are in **CAD (Canadian Dollars)**. Prices are derived from the `price_per_100g` column in the dataset (`data-ml/raw/canada_grocery_nutrition_5000.csv`). The `cost` field in basket items and totals represents the total cost for the specified quantity.

---

## Column Mapping

The API maps dataset columns to response fields as follows:

| Dataset Column | Response Field | Notes |
|---------------|----------------|-------|

| `product_name` | `name` | Product name |
| `store` | `store` | Store name |
| `brand` | `brand` | Brand name |
| `category` | `category` | Product category |
| `sub_category` | `sub_category` | Product subcategory |
| `food_type` | Used for `processing_breakdown.level` | Processing level |
| `veg_nonveg` | Used for filtering | Diet type filter |
| `calories` | `calories` | Calories per 100g |
| `protein` | `protein` | Protein per 100g (g) |
| `carbs` | `carbs` | Carbohydrates per 100g (g) |
| `fat` | `fat` | Fat per 100g (g) |
| `sugar` | `sugar` | Sugar per 100g (g) |
| `fiber` | `fiber` | Fiber per 100g (g) |
| `price_per_100g` | Used to calculate `cost` | Price in CAD per 100g |
| `FPro` | `FPro` | Processing score (0-1) |
| `nutriscore` | Not included in response | Available in dataset |

---

## Backend Stack Notes

- **Language**: Python
- **Framework**: Flask
- **CORS**: flask-cors (enabled for cross-origin requests)
- **Core Function**: `planner()` function handles the optimization logic:
  - Takes request parameters (budget, people, dietType, goal)
  - Loads product data from `data-ml/raw/canada_grocery_nutrition_5000.csv`
  - Applies diet type and goal filters
  - Runs budget-constrained optimization algorithm
  - Returns structured response with basket, totals, coverage, and breakdowns
