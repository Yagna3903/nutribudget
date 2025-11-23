# Data & ML Notes

## Dataset
- **Source**: `canada_grocery_nutrition_5000.csv`
- **Rows**: ~5000
- **Columns**: Includes metadata (name, store, brand), nutrients (calories, protein, etc.), and price.

## Scores

### Health Score (0-100)
A composite score derived from nutritional values.
- **Rewards**: Protein, Fiber, Nutriscore.
- **Penalties**: Sugar, Saturated Fat, Trans Fat, Sodium, Processing Level (FPro).
- **Formula**: Scaled result of `(Protein*2 + Fiber*3 + Nutriscore*5) - (Sugar + SatFat*2 + TransFat*5 + Sodium/100 + FPro*20)`

### Affordability Score (0-100)
Based on `price_per_100g`.
- **Formula**: Inverse of price (`1 / price_per_100g`), scaled to 0-100.
- Higher score = Cheaper item.

### NutriScore App
The final metric used for ranking items in the planner.
- **Formula**: `0.6 * Health Score + 0.4 * Affordability Score`
- Balances health benefits with cost effectiveness.

## Clusters (K-Means)
Foods are grouped into 4 personas based on nutritional profile:
1. **Staples / Mixed**: Balanced items.
2. **Veg & Wholefoods**: High fiber/vitamins, low processing.
3. **Processed / Snacks**: High sugar/sodium, high processing.
4. **High Energy / Fatty**: Calorie dense.

## Assumptions & Limitations
- **Price**: Assumes `price_per_100g` is accurate and available.
- **Portions**: Optimization uses 100g units, which may not match actual package sizes.
- **Availability**: Does not account for real-time stock.
