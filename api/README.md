# NutriBudget API

Flask backend for the NutriBudget application.

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

The API will start on `http://127.0.0.1:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns: `{"status": "ok"}`

### Get Products
- **GET** `/api/foods`
- Query params:
  - `veg_nonveg`: Filter by diet type (e.g., "veg")
  - `max_price_per_100g`: Maximum price per 100g
  - `cluster`: Filter by cluster ID
  - `store`: Filter by store name
  - `limit`: Max results (default 100)
- Returns: `{"count": number, "items": [...]}`

### Get Statistics
- **GET** `/api/stats`
- Returns: Overall stats, cluster distribution, category distribution

### Generate Meal Plan
- **POST** `/api/plan`
- Body:
```json
{
  "budget": 50,
  "people": 2,
  "dietType": "veg",
  "goal": "balanced"
}
```
- Returns: Optimized grocery basket with totals and breakdowns

### Debug
- **GET** `/api/debug-products`
- Returns: First 20 products from the dataset

## Development

The API uses:
- **Flask** for the web framework
- **PuLP** for Linear Programming optimization
- **pandas** for data manipulation
- **flask-cors** for cross-origin requests
