"""
ML Utilities for NutriBudget

Helper functions for loading models and making predictions.
"""

import os
import joblib
import pandas as pd
import numpy as np

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

# Global cache for models
_models_cache = None

def load_models():
    """
    Load all trained ML models from disk.
    Returns dict with models and scaler, or None if models don't exist.
    """
    global _models_cache
    
    # Return cached models if already loaded
    if _models_cache is not None:
        return _models_cache
    
    try:
        models = {
            'quality_classifier': joblib.load(os.path.join(MODELS_DIR, "quality_classifier.joblib")),
            'value_predictor': joblib.load(os.path.join(MODELS_DIR, "value_predictor.joblib")),
            'price_predictor': joblib.load(os.path.join(MODELS_DIR, "price_predictor.joblib")),
            'scaler': joblib.load(os.path.join(MODELS_DIR, "feature_scaler.joblib"))
        }
        _models_cache = models
        print("✅ ML models loaded successfully")
        return models
    except FileNotFoundError as e:
        print(f"⚠️  ML models not found: {e}")
        print("   Run 'python train_models.py' to train models")
        return None
    except Exception as e:
        print(f"❌ Error loading ML models: {e}")
        return None

def prepare_features(df):
    """
    Prepare features from dataframe for ML prediction.
    
    Args:
        df: DataFrame with product data
    
    Returns:
        DataFrame with scaled features
    """
    models = load_models()
    if models is None:
        return None
    
    feature_cols = ['calories', 'protein', 'carbs', 'fat', 'sugar', 'fiber', 'price_per_100g']
    
    # Extract features
    X = df[feature_cols].copy()
    
    # Fill missing values
    X = X.fillna(X.mean())
    
    # Scale features
    X_scaled = models['scaler'].transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols, index=X.index)
    
    return X_scaled

def predict_quality(df):
    """
    Predict health quality category for products.
    
    Args:
        df: DataFrame with product data
    
    Returns:
        Series with predictions ('High', 'Medium', 'Low'), or None if models unavailable
    """
    models = load_models()
    if models is None:
        return None
    
    X = prepare_features(df)
    if X is None:
        return None
    
    predictions = models['quality_classifier'].predict(X)
    return pd.Series(predictions, index=df.index)

def predict_value(df):
    """
    Predict nutritional value score for products.
    
    Args:
        df: DataFrame with product data
    
    Returns:
        Series with predicted value scores, or None if models unavailable
    """
    models = load_models()
    if models is None:
        return None
    
    X = prepare_features(df)
    if X is None:
        return None
    
    predictions = models['value_predictor'].predict(X)
    return pd.Series(predictions, index=df.index)

def predict_fair_price(df):
    """
    Predict fair price for products based on nutritional content.
    
    Args:
        df: DataFrame with product data
    
    Returns:
        Series with predicted prices, or None if models unavailable
    """
    models = load_models()
    if models is None:
        return None
    
    X = prepare_features(df)
    if X is None:
        return None
    
    # Remove price column to avoid data leakage
    X_no_price = X.drop(columns=['price_per_100g'])
    
    predictions = models['price_predictor'].predict(X_no_price)
    return pd.Series(predictions, index=df.index)

def calculate_ml_score(df):
    """
    Calculate comprehensive ML-based score combining all predictions.
    
    Args:
        df: DataFrame with product data
    
    Returns:
        Series with ML scores, or None if models unavailable
    """
    # Get predictions
    quality_pred = predict_quality(df)
    value_pred = predict_value(df)
    fair_price_pred = predict_fair_price(df)
    
    if quality_pred is None or value_pred is None or fair_price_pred is None:
        return None
    
    # Quality score: High=3, Medium=2, Low=1
    quality_map = {'High': 3, 'Medium': 2, 'Low': 1}
    quality_score = quality_pred.map(quality_map)
    
    # Value score: normalized predicted value
    value_score = value_pred / 100.0  # Normalize to 0-1 range
    
    # Deal score: positive if underpriced (fair_price > actual_price)
    actual_price = df['price_per_100g']
    deal_score = np.maximum(0, fair_price_pred - actual_price) * 10  # Amplify deal bonus
    
    # Combined ML score
    ml_score = (
        quality_score * 0.3 +      # 30% weight on quality
        value_score * 0.4 +         # 40% weight on nutritional value
        deal_score * 0.3            # 30% weight on being a good deal
    )
    
    return ml_score

def models_available():
    """
    Check if ML models are available.
    
    Returns:
        bool: True if models are loaded, False otherwise
    """
    return load_models() is not None
