# NutriBudget – Budget-Aware Nutrition Optimizer

> **Maximize nutrition within your budget** using real grocery data, machine learning, and smart optimization.

NutriBudget helps users (especially budget-conscious households) get the **best possible nutrition** for their grocery budget. It combines real product data with ML-based scoring and greedy optimization to recommend grocery baskets that maximize nutritional value while respecting dietary preferences and budget constraints.

---

## 📋 Overview

**What it does:**
- Takes user inputs: budget ($), household size, diet type (veg/non-veg/vegan), nutrition goal
- Returns an optimized grocery basket with real products, prices, and nutritional breakdown
- Shows cost savings vs typical shopping and SDG impact (Zero Hunger, Good Health)

**Tech Stack:**
- **Backend**: Flask (Python) with CORS enabled
- **Frontend**: Next.js 16 with React 19, Tailwind CSS v4
- **Data/ML**: pandas, scikit-learn (K-Means clustering, MinMaxScaler)
- **Animations**: Framer Motion, GSAP
- **Data**: Canadian grocery dataset (~5000 products with nutrition + prices)

**Components:**
1. **`data-ml/`** - Python pipeline that cleans data, engineers features, and clusters products
2. **`api/`** - Flask REST API with meal planning logic
3. **`web/`** - Next.js frontend with beautiful UI and animations

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (for backend and data pipeline)
- **Node.js 18+** and npm (for frontend)
- **Canada grocery dataset** (placed in `data-ml/raw/` - see Data Setup below)

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd nutribudget
```

### 2. Data Setup

Place your grocery dataset in `data-ml/raw/`:
```bash
# You should have this file (not included in repo):
data-ml/raw/canada_grocery_nutrition_5000.csv
```

> **Note**: This project uses a Canadian grocery dataset with ~5000 products containing nutrition facts and prices. If you don't have this dataset, you can use your own CSV with similar columns (product_name, category, calories, protein, carbs, fat, sugar, fiber, price_per_100g, etc.)

### 3. Run Data Pipeline

Process the raw data to create scored products:

```bash
cd data-ml

# Optional: Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas numpy scikit-learn

# Step 1: Clean the data
python clean_data.py

# Step 2: Run feature engineering and clustering
python run_pipeline.py

# This creates: outputs/foods_scored.csv
cd ..
```

**What happens:**
1. `clean_data.py` - Fixes brand mismatches, winsorizes prices → `outputs/canada_grocery_nutrition_clean.csv`
2. `run_pipeline.py` - Calculates health/affordability scores, applies K-Means clustering → `outputs/foods_scored.csv`

### 4. Start Backend API

```bash
cd api

# Create virtual environment (recommended)
python3 -m venv venv-backend
source venv-backend/bin/activate  # On Windows: venv-backend\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

**Backend runs on:** `http://localhost:5000`

**Available endpoints:**
- `GET /health` - Health check
- `GET /api/debug-products` - View sample products
- `GET /api/foods` - Search/filter products
- `GET /api/stats` - Dataset statistics
- `POST /api/plan` - Generate meal plan (main endpoint)

### 5. Start Frontend

```bash
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs on:** `http://localhost:3000`

**Open in browser:** Navigate to http://localhost:3000 to use the app!

---

## 💻 Usage

### Via Web Interface (Recommended)

1. Open http://localhost:3000
2. Fill in the form:
   - **Budget**: e.g., $50
   - **People**: e.g., 2
   - **Diet Type**: Vegetarian / Non-vegetarian / Vegan
   - **Goal**: Balanced / High Protein / Low Sugar
3. Click "Generate Plan"
4. View your optimized grocery basket with:
   - Product list with quantities and costs
   - Nutrition coverage (calories, protein)
   - Cost savings analysis
   - SDG impact section
   - Meal suggestions
   - Export shopping list

### Via API (For Developers)

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 40,
    "people": 2,
    "dietType": "veg",
    "goal": "high_protein"
  }'
```

**Example Response:**
```json
{
  "inputs": {
    "budget": 40,
    "people": 2,
    "dietType": "veg",
    "goal": "high_protein"
  },
  "items": [
    {
      "product_id": 123,
      "product_name": "Lentils, Red",
      "store": "Walmart",
      "category": "Dry Goods",
      "cluster_label": "Veg & Wholefoods",
      "health_score": 85.3,
      "nutri_score_app": 78.9,
      "price_per_100g": 0.42,
      "quantity_units": 3,
      "estimated_cost": 1.26
    }
    // ... more items
  ],
  "totals": {
    "total_spent": 38.50,
    "budget": 40,
    "calories": 28000,
    "protein": 950,
    "fiber": 140
  },
  "coverage": {
    "calories": {
      "actual": 28000,
      "target": 28000,
      "percentage": 100.0
    },
    "protein": {
      "actual": 950,
      "target": 700,
      "percentage": 135.7
    }
  },
  "savings": {
    "amount": 6.93,
    "percentage": 15.3,
    "typical_cost": 45.43
  },
  "clusterBreakdown": {
    "Veg & Wholefoods": 15,
    "Staples / Mixed": 8
  },
  "processingBreakdown": {
    "Whole Foods": 18,
    "Minimally Processed": 5
  }
}
```

---

## 📁 Project Structure

```
nutribudget/
├── data-ml/                      # Data processing pipeline
│   ├── raw/                      # Raw CSV data (not in repo)
│   │   └── canada_grocery_nutrition_5000.csv
│   ├── outputs/                  # Generated outputs
│   │   ├── canada_grocery_nutrition_clean.csv
│   │   └── foods_scored.csv     # ⭐ Final dataset used by API
│   ├── clean_data.py            # Step 1: Data cleaning
│   ├── run_pipeline.py          # Step 2: Feature engineering & ML
│   └── *.ipynb                  # Exploratory notebooks
│
├── api/                          # Flask backend
│   ├── app.py                   # Flask server with endpoints
│   ├── planner.py               # Core meal planning logic
│   ├── requirements.txt         # Python dependencies
│   ├── API_CONTRACT.md          # API documentation
│   └── test_api.py              # API tests
│
├── web/                          # Next.js frontend
│   ├── app/                     # Next.js app directory
│   │   ├── page.tsx            # Main landing page
│   │   └── layout.tsx          # Root layout
│   ├── components/              # React components
│   │   ├── BudgetForm.tsx      # User input form
│   │   ├── PlanShell.tsx       # Main container
│   │   ├── BasketCard.tsx      # Product cards
│   │   ├── CoverageBar.tsx     # Nutrition bars
│   │   └── ...
│   ├── types/                   # TypeScript types
│   ├── utils/                   # Utility functions
│   ├── package.json
│   └── tailwind.config.js
│
└── README.md                     # This file
```

---

## 🧠 How It Works

### 1. Data Pipeline (`data-ml/`)

**Input:** Raw grocery CSV with products, nutrition facts, prices

**Process:**
1. **Clean data** (`clean_data.py`):
   - Fix brand mismatches (e.g., "Coke" → "Coca-Cola")
   - Winsorize prices by category (remove outliers)
   - Clean produce categorization

2. **Feature engineering & clustering** (`run_pipeline.py`):
   - Calculate **health_score** (0-100):
     - Rewards: protein, fiber, nutriscore
     - Penalties: sugar, saturated fat, trans fat, sodium, processing (FPro)
   - Calculate **affordability_score** (0-100):
     - Based on inverse of price_per_100g
   - Combine into **nutri_score_app**:
     - `nutri_score_app = 0.6 × health_score + 0.4 × affordability_score`
   - Apply **K-Means clustering** (4 clusters):
     - Cluster 0: Staples / Mixed
     - Cluster 1: Veg & Wholefoods
     - Cluster 2: Processed / Snacks
     - Cluster 3: High Energy / Fatty

**Output:** `foods_scored.csv` with all products scored and clustered

### 2. Backend API (`api/`)

**Flask Server** (`app.py`):
- Loads `foods_scored.csv` on startup
- Exposes REST endpoints for searching and planning

**Meal Planner** (`planner.py`):
- **Algorithm:** Greedy value-based selection
- **Steps:**
  1. Filter by diet type (veg/non-veg/vegan)
  2. Calculate value metric: `nutri_score_app / price_per_100g`
  3. Adjust for goal (high protein → boost protein-rich items, low sugar → penalize sugary items)
  4. Sort by value (descending)
  5. Greedily add items to basket until budget exhausted (max 5 units per item for variety)
  6. Calculate totals, coverage, and savings

### 3. Frontend (`web/`)

**Next.js App:**
- Modern React 19 with TypeScript
- Tailwind CSS v4 for styling
- Framer Motion for animations
- Glassmorphism UI design

**User Flow:**
1. User fills form (budget, people, diet, goal)
2. Submits → POST to `/api/plan`
3. Receives optimized basket
4. Displays results with beautiful visualizations

---

## 🎯 Features

### Current Features
✅ Budget-constrained meal planning  
✅ 3 diet types (vegetarian, non-vegetarian, vegan)  
✅ 3 nutrition goals (balanced, high protein, low sugar)  
✅ ML-based product clustering  
✅ Cost savings analysis  
✅ Nutrition coverage tracking (calories, protein)  
✅ SDG impact section (Zero Hunger, Good Health)  
✅ Smart meal suggestions  
✅ Export shopping list  
✅ Beautiful, animated UI with glassmorphism  

### Potential Enhancements
🔮 Recipe suggestions using basket items  
🔮 Micronutrient tracking (vitamins, minerals)  
🔮 Linear programming optimization (instead of greedy)  
🔮 User preferences (allergies, dislikes)  
🔮 Multi-store comparison  
🔮 Historical tracking and refill suggestions  

---

## 🧪 Testing

### Test Backend API
```bash
cd api
python test_api.py
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test debug products
curl http://localhost:5000/api/debug-products

# Test plan endpoint
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"budget": 30, "people": 1, "dietType": "veg", "goal": "balanced"}'
```

---

## 🐛 Troubleshooting

### Backend won't start
- **Error:** `FileNotFoundError: foods_scored.csv`
  - **Solution:** Run the data pipeline first (`clean_data.py` → `run_pipeline.py`)

- **Error:** `ModuleNotFoundError: No module named 'flask'`
  - **Solution:** Install dependencies: `pip install -r api/requirements.txt`

### Frontend won't start
- **Error:** `Cannot find module 'next'`
  - **Solution:** Install dependencies: `cd web && npm install`

- **Error:** `Failed to fetch from http://localhost:5000`
  - **Solution:** Make sure backend is running on port 5000

### Data pipeline fails
- **Error:** `FileNotFoundError: canada_grocery_nutrition_5000.csv`
  - **Solution:** Place your dataset in `data-ml/raw/`

### No products in basket
- **Error:** Empty basket returned
  - **Solution:** Check if dataset has products matching your diet type filter

---

## 📊 Dataset Requirements

If using your own dataset, ensure it has these columns:

**Required:**
- `product_name` - Product name (string)
- `category` - Food category (string)
- `price_per_100g` - Price per 100 grams (float, CAD or USD)
- `calories` - Calories per 100g (float)
- `protein` - Protein in grams per 100g (float)
- `carbs` - Carbohydrates in grams per 100g (float)
- `fat` - Fat in grams per 100g (float)
- `sugar` - Sugar in grams per 100g (float)
- `fiber` - Fiber in grams per 100g (float)

**Optional but recommended:**
- `store` - Store name (string)
- `brand` - Brand name (string)
- `veg_nonveg` - "Vegetarian" or "Non-Vegetarian" (string)
- `FPro` - Processing score 0-1 (float, 0=whole food, 1=ultra-processed)
- `nutriscore` - Nutri-Score A-E or numeric (string/int)
- `saturated_fat`, `trans_fat`, `sodium` - For health scoring

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better optimization algorithms (linear programming with PuLP)
- More nutrition goals (low carb, high fiber, keto, etc.)
- Recipe database integration
- User authentication and saved plans
- Mobile app (React Native)
- Multi-language support

---

## 📄 License

MIT License - feel free to use this project for learning, research, or commercial purposes.

---

## 🌍 SDG Impact

This project contributes to:
- **SDG 2**: Zero Hunger (making nutrition accessible to budget-constrained households)
- **SDG 3**: Good Health and Well-being (promoting nutritious food choices)

---

## 🙏 Acknowledgments

- Dataset inspired by grocery nutrition databases
- Built with Flask, Next.js, pandas, and scikit-learn
- UI animations powered by Framer Motion and GSAP

---

**Made with ❤️ for healthier, more affordable grocery shopping**
