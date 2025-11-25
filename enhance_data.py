import pandas as pd
import numpy as np
import re

def extract_weight(product_name):
    """Extract weight in grams from product name if available"""
    # Patterns for g, kg, ml, l
    g_pattern = r'(\d+)\s*g'
    kg_pattern = r'(\d+\.?\d*)\s*kg'
    ml_pattern = r'(\d+)\s*ml'
    l_pattern = r'(\d+\.?\d*)\s*l'
    
    # Check grams
    match = re.search(g_pattern, product_name.lower())
    if match:
        return float(match.group(1))
        
    # Check kg
    match = re.search(kg_pattern, product_name.lower())
    if match:
        return float(match.group(1)) * 1000
        
    # Check ml (assume 1ml = 1g for simplicity)
    match = re.search(ml_pattern, product_name.lower())
    if match:
        return float(match.group(1))
        
    # Check liters
    match = re.search(l_pattern, product_name.lower())
    if match:
        return float(match.group(1)) * 1000
        
    return None

def get_default_weight(category, sub_category):
    """Get default weight based on category"""
    # Defaults in grams
    defaults = {
        'Produce': 500,  # 500g bag/bunch
        'Meat & Seafood': 450, # 1lb pack
        'Dairy & Eggs': 500, # 500g tub/carton
        'Bakery': 450, # Loaf of bread
        'Pantry': 400, # Can/Box
        'Frozen': 600, # Bag of frozen stuff
        'Snacks': 250, # Bag of chips
        'Beverages': 1000, # 1L bottle
    }
    
    # Specific sub-category overrides
    sub_defaults = {
        'Cereal': 450,
        'Cookies': 300,
        'Bars': 180, # Box of bars
        'Cheese': 250, # Block of cheese
        'Yogurt': 650, # Tub
        'Milk': 2000, # 2L carton
        'Eggs': 600, # Dozen
        'Bread': 600,
        'Pasta': 500, # Standard box
        'Rice': 900, # 2lb bag
        'Canned': 398, # Standard can
        'Spices': 50,
    }
    
    if sub_category in sub_defaults:
        return sub_defaults[sub_category]
        
    if category in defaults:
        return defaults[category]
        
    return 300 # Fallback

def round_retail_price(price):
    """Round price to realistic retail points (.99, .49, .97)"""
    if price < 1.0:
        return round(price * 2) / 2 # Round to nearest 0.50
        
    base = int(price)
    decimal = price - base
    
    if decimal < 0.25:
        return base - 0.01 # .99 of previous dollar
    elif decimal < 0.75:
        return base + 0.49 # .49
    else:
        return base + 0.99 # .99

def enhance_data():
    print("🚀 Enhancing dataset with realistic prices...")
    
    # Load data
    try:
        df = pd.read_csv('api/data/foods_scored.csv')
        print(f"Loaded {len(df)} products")
    except FileNotFoundError:
        print("❌ Could not find api/data/foods_scored.csv")
        return

    # 1. Calculate Package Weights
    weights = []
    sources = []
    
    for _, row in df.iterrows():
        extracted = extract_weight(row['product_name'])
        if extracted:
            weights.append(extracted)
            sources.append('extracted')
        else:
            default = get_default_weight(row['category'], row['sub_category'])
            weights.append(default)
            sources.append('default')
            
    df['package_weight_g'] = weights
    df['weight_source'] = sources
    
    # 2. Calculate Item Price
    # price_per_100g is in dollars
    # item_price = (price_per_100g / 100) * weight
    df['price_per_item'] = (df['price_per_100g'] / 100) * df['package_weight_g']
    
    # 3. Apply Retail Rounding
    df['price_per_item'] = df['price_per_item'].apply(round_retail_price)
    
    # Ensure minimum price (nothing free)
    df.loc[df['price_per_item'] < 0.25, 'price_per_item'] = 0.49
    
    # 4. Recalculate price_per_100g to match the new retail price
    # This ensures consistency: item_price / weight * 100 = price_per_100g
    df['price_per_100g'] = (df['price_per_item'] / df['package_weight_g']) * 100
    
    # Save enhanced data
    output_path = 'api/data/foods_enhanced.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Saved enhanced data to {output_path}")
    
    # Show samples
    print("\n📊 Sample Realistic Prices:")
    print(df[['product_name', 'package_weight_g', 'price_per_100g', 'price_per_item']].head(10))
    
    # Stats
    print("\n📈 Statistics:")
    print(f"Average Item Price: ${df['price_per_item'].mean():.2f}")
    print(f"Min Item Price: ${df['price_per_item'].min():.2f}")
    print(f"Max Item Price: ${df['price_per_item'].max():.2f}")

if __name__ == "__main__":
    enhance_data()
