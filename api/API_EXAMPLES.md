# NutriBudget API - Quick Reference & Examples

## Base URL
```
http://localhost:5000
```

## Quick Test Commands

### 1. Health Check
```bash
curl http://localhost:5000/health
```

Expected Response:
```json
{"status": "ok"}
```

---

## GET /api/foods - Search Products

### Get 10 vegetarian products
```bash
curl "http://localhost:5000/api/foods?veg_nonveg=veg&limit=10"
```

### Get affordable products (under $1 per 100g)
```bash
curl "http://localhost:5000/api/foods?max_price_per_100g=1.0&limit=20"
```

### Get high-protein products (cluster 0)
```bash
curl "http://localhost:5000/api/foods?cluster=0&limit=15"
```

### Get products from Costco
```bash
curl "http://localhost:5000/api/foods?store=costco&limit=10"
```

### Combined filters
```bash
curl "http://localhost:5000/api/foods?veg_nonveg=veg&max_price_per_100g=0.8&store=costco&limit=10"
```

---

## GET /api/stats - Get Statistics

```bash
curl http://localhost:5000/api/stats
```

Expected Response includes:
- Total products
- Average price per 100g
- Cluster distribution
- Category distribution

---

## POST /api/plan - Generate Meal Plan

### Budget-Conscious Student ($30, veg, balanced)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 30,
    "people": 1,
    "dietType": "veg",
    "goal": "balanced"
  }'
```

### Family of 3 ($50, mixed, balanced)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50,
    "people": 3,
    "dietType": "mixed",
    "goal": "balanced"
  }'
```

### Athlete ($40, non-veg, high protein)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 40,
    "people": 1,
    "dietType": "nonveg",
    "goal": "high_protein"
  }'
```

### Health-Conscious Couple ($60, veg, low sugar)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 60,
    "people": 2,
    "dietType": "veg",
    "goal": "low_sugar"
  }'
```

### Large Family ($100, mixed, balanced)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 100,
    "people": 5,
    "dietType": "mixed",
    "goal": "balanced"
  }'
```

---

## Edge Cases & Error Testing

### Budget too low (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 3,
    "people": 1,
    "dietType": "veg",
    "goal": "balanced"
  }'
```

### Negative budget (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": -10,
    "people": 1,
    "dietType": "veg",
    "goal": "balanced"
  }'
```

### Zero people (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50,
    "people": 0,
    "dietType": "veg",
    "goal": "balanced"
  }'
```

### Invalid diet type (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50,
    "people": 2,
    "dietType": "invalid",
    "goal": "balanced"
  }'
```

### Invalid goal (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50,
    "people": 2,
    "dietType": "veg",
    "goal": "invalid_goal"
  }'
```

### Missing required fields (should return 400)
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 50
  }'
```

---

## Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:5000/health")
print(response.json())

# Get vegetarian products
response = requests.get(
    "http://localhost:5000/api/foods",
    params={"veg_nonveg": "veg", "limit": 10}
)
print(response.json())

# Generate meal plan
response = requests.post(
    "http://localhost:5000/api/plan",
    json={
        "budget": 50,
        "people": 2,
        "dietType": "veg",
        "goal": "balanced"
    }
)
print(response.json())
```

---

## Using JavaScript/Fetch

```javascript
// Health check
fetch('http://localhost:5000/health')
  .then(res => res.json())
  .then(data => console.log(data));

// Get products
fetch('http://localhost:5000/api/foods?veg_nonveg=veg&limit=10')
  .then(res => res.json())
  .then(data => console.log(data));

// Generate meal plan
fetch('http://localhost:5000/api/plan', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    budget: 50,
    people: 2,
    dietType: 'veg',
    goal: 'balanced'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Valid Values Reference

### dietType
- `veg` or `vegetarian`
- `nonveg` or `non-veg`
- `mixed`

### goal
- `balanced` - Balanced nutrition
- `high_protein` - Maximize protein
- `low_sugar` - Minimize sugar

### Constraints
- Budget: $5 - $1000
- People: 1 - 20
- All fields are required for `/api/plan`

---

## Response Examples

### Successful Plan Response
```json
{
  "basket": [
    {
      "product_id": 123,
      "product_name": "Organic Spinach",
      "store": "Costco Canada",
      "brand": "Kirkland",
      "quantity_g": 500,
      "cost": 2.25,
      "calories": 115,
      "protein": 14.5,
      "fiber": 18,
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

### Error Response
```json
{
  "error": "Budget too low",
  "message": "Budget must be at least $5 to meet basic nutrition needs."
}
```
