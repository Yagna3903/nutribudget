import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ml_utils

def verify_models():
    print("🔍 Verifying ML Models...")
    
    # 1. Load Models
    try:
        models = ml_utils.load_models()
        print("✅ Models loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load models: {e}")
        return

    # 2. Create Sample Data (Simulating real products)
    # We'll create 3 distinct products to see if models can tell the difference
    sample_products = [
        {
            "product_name": "Fresh Spinach (Healthy)",
            "calories": 23,
            "protein": 2.9,
            "carbs": 3.6,
            "fat": 0.4,
            "sugar": 0.4,
            "fiber": 2.2,
            "price_per_100g": 0.50
        },
        {
            "product_name": "Chocolate Bar (Unhealthy)",
            "calories": 530,
            "protein": 7.0,
            "carbs": 59.0,
            "fat": 30.0,
            "sugar": 54.0,
            "fiber": 3.0,
            "price_per_100g": 1.50
        },
        {
            "product_name": "Lentils (High Value)",
            "calories": 116,
            "protein": 9.0,
            "carbs": 20.0,
            "fat": 0.4,
            "sugar": 1.8,
            "fiber": 7.9,
            "price_per_100g": 0.30
        }
    ]
    
    df = pd.DataFrame(sample_products)
    
    print("\n📊 Testing Predictions on Sample Products:")
    print("-" * 60)
    
    # Get predictions
    qualities = ml_utils.predict_quality(df)
    values = ml_utils.predict_value(df)
    fair_prices = ml_utils.predict_fair_price(df)
    
    for i, product in df.iterrows():
        name = product['product_name']
        actual_price = product['price_per_100g']
        
        predicted_quality = qualities[i]
        predicted_value = values[i]
        predicted_fair_price = fair_prices[i]
        
        print(f"\nProduct: {name}")
        print(f"  Actual Price: ${actual_price:.2f}/100g")
        print(f"  🤖 Predicted Quality: {predicted_quality}")
        print(f"  📈 Predicted Value Score: {predicted_value:.1f}/100")
        print(f"  💰 Predicted Fair Price: ${predicted_fair_price:.2f}/100g")
        
        # Analysis
        if predicted_fair_price > actual_price:
            print(f"  ✨ DEAL ALERT: Model thinks this is worth ${predicted_fair_price-actual_price:.2f} more!")
        else:
            print(f"  ⚠️ Overpriced: Model thinks this should cost ${actual_price-predicted_fair_price:.2f} less.")

if __name__ == "__main__":
    verify_models()
