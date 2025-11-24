"""
NutriBudget ML Model Training Script

This script trains machine learning models on the grocery dataset to:
1. Classify product health quality (Random Forest)
2. Predict nutritional value scores (Linear Regression)
3. Predict fair prices to identify deals (Linear Regression)

Models are saved to the models/ directory for use in the planner.
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    r2_score, mean_squared_error, mean_absolute_error, classification_report
)
import joblib

# Configuration
DATA_PATH = "data/foods_scored.csv"
MODELS_DIR = "models"
RANDOM_STATE = 42

def create_health_categories(df):
    """
    Create health quality categories based on health_score.
    Categories: Low (0-40), Medium (40-70), High (70+)
    """
    conditions = [
        df['health_score'] < 40,
        (df['health_score'] >= 40) & (df['health_score'] < 70),
        df['health_score'] >= 70
    ]
    categories = ['Low', 'Medium', 'High']
    df['health_category'] = np.select(conditions, categories, default='Medium')
    return df

def prepare_features(df):
    """
    Prepare feature matrices for ML training.
    Returns scaled features for prediction.
    """
    # Select nutritional features
    feature_cols = [
        'calories', 'protein', 'carbs', 'fat', 'sugar', 'fiber', 'price_per_100g'
    ]
    
    # Ensure all features exist and handle missing values
    for col in feature_cols:
        if col not in df.columns:
            print(f"Warning: {col} not found in dataset")
            df[col] = 0
    
    # Fill missing values with column means
    df[feature_cols] = df[feature_cols].fillna(df[feature_cols].mean())
    
    X = df[feature_cols].copy()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols, index=X.index)
    
    return X_scaled, scaler

def train_quality_classifier(X, y):
    """
    Train Random Forest classifier to predict product health quality.
    """
    print("\n" + "="*60)
    print("Training Product Quality Classifier (Random Forest)")
    print("="*60)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\nResults on {len(X_test)} test samples:")
    print(f"  Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Most Important Features:")
    print(feature_importance.head().to_string(index=False))
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }
    
    return model, metrics

def train_value_predictor(X, y):
    """
    Train Random Forest regressor to predict nutritional value score.
    """
    print("\n" + "="*60)
    print("Training Nutritional Value Predictor (Random Forest Regression)")
    print("="*60)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\nResults on {len(X_test)} test samples:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  RMSE:     {rmse:.4f}")
    print(f"  MAE:      {mae:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Most Important Features:")
    print(feature_importance.head().to_string(index=False))
    
    metrics = {
        'r2_score': float(r2),
        'rmse': float(rmse),
        'mae': float(mae),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }
    
    return model, metrics

def train_price_predictor(X, y):
    """
    Train Linear Regression model to predict fair prices.
    """
    print("\n" + "="*60)
    print("Training Price Fairness Model (Linear Regression)")
    print("="*60)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    # Remove price from features (avoid data leakage)
    price_col = 'price_per_100g'
    if price_col in X_train.columns:
        X_train = X_train.drop(columns=[price_col])
        X_test = X_test.drop(columns=[price_col])
    
    # Train model
    model = LinearRegression()
    
    print(f"Training on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\nResults on {len(X_test)} test samples:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  RMSE:     ${rmse:.4f}")
    print(f"  MAE:      ${mae:.4f}")
    
    # Show coefficient insights
    coef_df = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': model.coef_
    }).sort_values('coefficient', ascending=False)
    
    print("\nTop Price Drivers (Positive Coefficients):")
    print(coef_df.head(3).to_string(index=False))
    
    metrics = {
        'r2_score': float(r2),
        'rmse': float(rmse),
        'mae': float(mae),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }
    
    return model, metrics

def main():
    """
    Main training pipeline.
    """
    print("\n" + "="*60)
    print("NutriBudget ML Model Training")
    print("="*60)
    
    # Create models directory
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Load data
    print(f"\nLoading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} products")
    
    # Create health categories
    df = create_health_categories(df)
    print(f"\nHealth Categories Distribution:")
    print(df['health_category'].value_counts())
    
    # Prepare features
    print("\nPreparing features...")
    X, scaler = prepare_features(df)
    
    # Save scaler
    scaler_path = os.path.join(MODELS_DIR, "feature_scaler.joblib")
    joblib.dump(scaler, scaler_path)
    print(f"Saved feature scaler to {scaler_path}")
    
    # Train Quality Classifier
    y_quality = df['health_category']
    quality_model, quality_metrics = train_quality_classifier(X, y_quality)
    quality_path = os.path.join(MODELS_DIR, "quality_classifier.joblib")
    joblib.dump(quality_model, quality_path)
    print(f"\nSaved quality classifier to {quality_path}")
    
    # Train Value Predictor
    y_value = df['nutri_score_app']
    value_model, value_metrics = train_value_predictor(X, y_value)
    value_path = os.path.join(MODELS_DIR, "value_predictor.joblib")
    joblib.dump(value_model, value_path)
    print(f"\nSaved value predictor to {value_path}")
    
    # Train Price Predictor
    y_price = df['price_per_100g']
    price_model, price_metrics = train_price_predictor(X, y_price)
    price_path = os.path.join(MODELS_DIR, "price_predictor.joblib")
    joblib.dump(price_model, price_path)
    print(f"\nSaved price predictor to {price_path}")
    
    # Save all metrics
    all_metrics = {
        'quality_classifier': quality_metrics,
        'value_predictor': value_metrics,
        'price_predictor': price_metrics,
        'dataset_size': len(df),
        'features': list(X.columns)
    }
    
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    print(f"\nSaved model metrics to {metrics_path}")
    
    # Summary
    print("\n" + "="*60)
    print("Training Complete! 🎉")
    print("="*60)
    print("\nTrained Models:")
    print(f"  ✅ Quality Classifier - Accuracy: {quality_metrics['accuracy']*100:.2f}%")
    print(f"  ✅ Value Predictor - R²: {value_metrics['r2_score']:.3f}")
    print(f"  ✅ Price Predictor - R²: {price_metrics['r2_score']:.3f}")
    print(f"\nAll models saved to {MODELS_DIR}/")

if __name__ == "__main__":
    main()
