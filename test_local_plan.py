import sys
sys.path.append('/Users/yagna/Documents/NutriBudget/nutribudget/api')

from planner import load_dataset, planner

# Load the enhanced dataset
print("Loading enhanced dataset...")
df = load_dataset('/Users/yagna/Documents/NutriBudget/nutribudget/api/data/foods_enhanced.csv')
print(f"Loaded {len(df)} products")

# Test plan generation
print("\nGenerating plan...")
result = planner(
    budget=40,
    people=2,
    diet_type="veg",
    goal="balanced",
    df=df,
    use_ml=True
)

print(f"\n✅ Plan Generated Successfully!")
print(f"Items in basket: {len(result['items'])}")
print(f"Total spent: ${result['totals']['total_spent']}")
print(f"Protein: {result['totals']['protein']}g")
print(f"Calories: {result['totals']['calories']}")

if len(result['items']) > 0:
    print("\nFirst 3 items:")
    for i, item in enumerate(result['items'][:3]):
        print(f"  {i+1}. {item['product_name']} - ${item['estimated_cost']:.2f}")
else:
    print("\n❌ ERROR: No items in basket!")
