# NutriBudget API

Flask backend for the NutriBudget application. This API provides endpoints for searching grocery products, generating optimized meal plans, and retrieving nutritional statistics.

## Table of Contents
- [Setup](#setup)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Development](#development)

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will start on `http://127.0.0.1:5000` in debug mode.

For production, use:
```bash
flask run --host=0.0.0.0 --port=5000
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Get Products

**Endpoint:** `GET /api/foods`

**Description:** Search and filter grocery products

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `veg_nonveg` | string | Filter by diet type | `veg`, `non-veg` |
| `max_price_per_100g` | float | Maximum price per 100g | `1.0` |
| `cluster` | integer | Filter by cluster ID (0-4) | `0` |
| `store` | string | Filter by store name | `costco` |
| `limit` | integer | Max number of results (default: 100) | `20` |

**Response:**
```json
{
  "count": 10,
  "items": [
    {
      "product_id": 123,
      "product_name": "Organic Spinach",
      "store": "Costco Canada",
      "brand": "Kirkland",
      "category": "Produce",
      "veg_nonveg": "Vegetarian",
      "calories": 23,
      "protein": 2.9,
      "price_per_100g": 0.45,
      "cluster": 3,
      "cluster_label": "Low-Carb Veggies"
    }
  ]
}
```

**Examples:**
```bash
# Get vegetarian products
curl "http://localhost:5000/api/foods?veg_nonveg=veg&limit=10"

# Get affordable products
curl "http://localhost:5000/api/foods?max_price_per_100g=0.8&limit=20"

# Get products from specific cluster
curl "http://localhost:5000/api/foods?cluster=0&limit=15"

# Combined filters
curl "http://localhost:5000/api/foods?veg_nonveg=veg&max_price_per_100g=1.0&store=costco&limit=10"
```

---

### 3. Get Statistics

**Endpoint:** `GET /api/stats`

**Description:** Get overall statistics about the product database

**Response:**
```json
{
  "total_products": 4900,
  "avg_price_per_100g": 0.89,
  "avg_calories": 285.4,
  "avg_protein": 12.3,
  "cluster_distribution": [
    {
      "cluster": 0,
      "label": "High-Protein Staples",
      "count": 980,
      "avg_price": 1.15
    }
  ],
  "category_distribution": [
    {
      "category": "Produce",
      "count": 650,
      "avg_price": 0.65
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/stats
```

---

### 4. Generate Meal Plan

**Endpoint:** `POST /api/plan`

**Description:** Generate an optimized grocery basket based on budget and dietary preferences

**Request Body:**
```json
{
  "budget": 50,
  "people": 2,
  "dietType": "veg",
  "goal": "balanced"
}
```

**Parameters:**
| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `budget` | number | Yes | Weekly budget in dollars | > 5 |
| `people` | integer | Yes | Number of people | >= 1 |
| `dietType` | string | Yes | Dietary preference | `veg`, `nonveg`, `mixed` |
| `goal` | string | Yes | Nutritional goal | `balanced`, `high_protein`, `low_sugar` |

**Response:**
```json
{
  "basket": [
    {
      "product_id": 123,
      "product_name": "Organic Spinach",
      "store": "Costco Canada",
      "quantity_g": 500,
      "cost": 2.25,
      "calories": 115,
      "protein": 14.5,
      "cluster_label": "Low-Carb Veggies"
    }
  ],
  "totals": {
    "budget": 50,
    "cost": 48.30,
    "calories": 14000,
    "protein": 350,
    "fiber": 125,
    "items": 15
  },
  "clusterBreakdown": {
    "High-Protein Staples": 5,
    "Low-Carb Veggies": 4,
    "Balanced Meals": 6
  }
}
```

**Examples:**
```bash
# Budget-conscious student
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"budget": 30, "people": 1, "dietType": "veg", "goal": "balanced"}'

# Family meal plan
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"budget": 100, "people": 4, "dietType": "mixed", "goal": "high_protein"}'
```

---

### 5. Debug Endpoint

**Endpoint:** `GET /api/debug-products`

**Description:** Get first 20 products from the dataset (for debugging)

**Response:**
```json
[
  {
    "product_id": 0,
    "product_name": "Bacon",
    "store": "IGA",
    ...
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/debug-products
```

## Testing

### Automated Testing

Run the comprehensive test suite:

```bash
# Make sure the API is running first
python app.py

# In another terminal, run tests
python test_api.py
```

The test suite includes:
- Health check validation
- Product filtering with various parameters
- Statistics endpoint verification
- Plan generation with different scenarios
- Edge case and error handling tests
- Performance benchmarking

### Manual Testing

Use the provided curl commands above, or use tools like:
- **Postman**: Import the endpoints as a collection
- **Thunder Client** (VS Code extension)
- **HTTPie**: `http POST localhost:5000/api/plan budget:=50 people:=2 dietType=veg goal=balanced`

## Error Handling

### Error Response Format

All errors return JSON with an `error` field:

```json
{
  "error": "Error message description"
}
```

### Common Error Codes

| Status Code | Description | Example |
|-------------|-------------|---------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid parameters, budget too low |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Internal server error |

### Validation Rules

**POST /api/plan:**
- `budget` must be > 0 (returns 400 if not)
- `budget` must be >= 5 (returns 400 with message if too low)
- `people` must be >= 1 (returns 400 if not)
- All fields are required (returns 400 if missing)

**Example Error Response:**
```json
{
  "error": "Budget too low",
  "message": "Budget must be at least $5 to meet basic nutrition needs."
}
```

## Development

### Technology Stack

- **Flask** - Web framework
- **PuLP** - Linear Programming optimization for meal planning
- **pandas** - Data manipulation and analysis
- **flask-cors** - Cross-origin resource sharing
- **NumPy** - Numerical computations

### Project Structure

```
api/
├── app.py              # Main Flask application
├── planner.py          # Meal planning logic
├── requirements.txt    # Python dependencies
├── test_api.py         # Automated test suite
└── README.md          # This file
```

### Data Source

The API loads product data from:
```
../data-ml/processed/products_with_clusters.csv
```

This file contains ~4900 grocery products with:
- Nutritional information (calories, protein, carbs, fat, etc.)
- Pricing data (price per gram, per 100g, per serving)
- ML-generated clusters (0-4) with descriptive labels
- Product metadata (store, brand, category)

### Adding New Features

1. **New Endpoint**: Add route in `app.py`
2. **New Logic**: Update `planner.py` for planning algorithms
3. **New Tests**: Add test cases in `test_api.py`
4. **Documentation**: Update this README

### Logging

The API logs important events:
- Plan generation requests
- Errors and exceptions
- Performance metrics

Logs are output to console in debug mode.

## Future Enhancements

- [ ] Add caching for frequently requested plans
- [ ] Implement user accounts and saved plans
- [ ] Add more sophisticated optimization algorithms
- [ ] Support for multiple currencies
- [ ] Integration with real-time store APIs
- [ ] Nutritional constraint customization
- [ ] Recipe suggestions based on selected items
