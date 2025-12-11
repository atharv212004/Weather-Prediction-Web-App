"""Train simple models for temperature_avg and humidity using RandomForest.
Uses only: latitude, longitude, month, year, day, dayofweek

Saves artifacts to `models/`:
- temp_model.pkl
- hum_model.pkl
- scaler.pkl
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


def train_models(cleaned_csv, out_dir='models'):
    print("=" * 60)
    print("TRAINING SIMPLE WEATHER MODELS")
    print("=" * 60)
    
    df = pd.read_csv(cleaned_csv, parse_dates=['date'])
    df = df.dropna(subset=['latitude', 'longitude', 'temperature_avg'])
    
    # Simple features: only latitude, longitude, and temporal
    all_features = ['latitude', 'longitude', 'year', 'month', 'day', 'dayofweek']
    
    print(f"✓ Using {len(all_features)} features: {all_features}")
    print(f"✓ Dataset size: {len(df)} records")
    
    X = df[all_features].copy()
    y_temp = df['temperature_avg'].copy()
    y_hum = df['humidity'].copy()
    
    # Standardize features
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, yt_train, yt_test = train_test_split(
        Xs, y_temp, test_size=0.15, random_state=42
    )
    _, _, yh_train, yh_test = train_test_split(
        Xs, y_hum, test_size=0.15, random_state=42
    )

    # Train simple RandomForest models
    print("\n" + "=" * 60)
    print("TRAINING TEMPERATURE MODEL")
    print("=" * 60)
    temp_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    temp_model.fit(X_train, yt_train)
    yt_pred = temp_model.predict(X_test)
    temp_mse = mean_squared_error(yt_test, yt_pred)
    temp_r2 = r2_score(yt_test, yt_pred)
    print(f"✓ Temperature MSE: {temp_mse:.4f}")
    print(f"✓ Temperature R² Score: {temp_r2:.4f}")

    print("\n" + "=" * 60)
    print("TRAINING HUMIDITY MODEL")
    print("=" * 60)
    hum_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    hum_model.fit(X_train, yh_train)
    yh_pred = hum_model.predict(X_test)
    hum_mse = mean_squared_error(yh_test, yh_pred)
    hum_r2 = r2_score(yh_test, yh_pred)
    print(f"✓ Humidity MSE: {hum_mse:.4f}")
    print(f"✓ Humidity R² Score: {hum_r2:.4f}")

    # Save models
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("SAVING MODELS")
    print("=" * 60)

    joblib.dump(temp_model, out / 'temp_model.pkl')
    print(f"✓ Saved: {out / 'temp_model.pkl'}")

    joblib.dump(hum_model, out / 'hum_model.pkl')
    print(f"✓ Saved: {out / 'hum_model.pkl'}")

    joblib.dump(scaler, out / 'scaler.pkl')
    print(f"✓ Saved: {out / 'scaler.pkl'}")

    print("=" * 60)
    print("✓ ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python train.py path/to/cleaned.csv')
        sys.exit(1)
    train_models(sys.argv[1])
