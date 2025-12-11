"""Train a MultiOutput RandomForest model for temperature, humidity, wind.

Usage:
  python train_model.py --csv "path/to/Global_Weather_5Years_2000Rows.csv"

This script attempts to auto-detect common column names. If your CSV uses
different names, update the mappings in the script.
"""
import argparse
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import joblib


def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def prepare(df):
    # Detect required columns
    lat_col = find_column(df, ['lat', 'latitude', 'Lat', 'Latitude'])
    lon_col = find_column(df, ['lon', 'longitude', 'Lon', 'Longitude'])
    date_col = find_column(df, ['date', 'Date', 'datetime', 'time'])

    temp_col = find_column(df, ['temp', 'temperature', 'Temperature', 'Temp'])
    hum_col = find_column(df, ['humidity', 'Humidity', 'hum'])
    wind_col = find_column(df, ['wind_speed', 'windspeed', 'WindSpeed', 'wind'])

    if not (lat_col and lon_col and date_col and temp_col and hum_col and wind_col):
        raise ValueError('Could not find required columns automatically. Found: {}, {}, {}, {}, {}, {}'.format(lat_col, lon_col, date_col, temp_col, hum_col, wind_col))

    # Optional extra features to include if available
    extra_candidates = ['pressure', 'Pressure', 'precipitation', 'precip', 'cloudcover', 'clouds']
    extra_cols = [c for c in extra_candidates if c in df.columns]

    needed = [lat_col, lon_col, date_col, temp_col, hum_col, wind_col] + extra_cols
    df = df[needed].copy()

    # Rename core columns
    rename_map = {lat_col: 'lat', lon_col: 'lon', date_col: 'date', temp_col: 'temp', hum_col: 'humidity', wind_col: 'wind'}
    for ec in extra_cols:
        rename_map[ec] = ec.lower()
    df = df.rename(columns=rename_map)

    # Parse dates and drop invalid
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'temp', 'humidity', 'wind'])

    # Feature engineering
    df['dayofyear'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Cleaning: clip realistic ranges
    df['humidity'] = df['humidity'].clip(0, 100)
    df['temp'] = df['temp'].clip(-90, 60)
    df['wind'] = df['wind'].clip(0, None)

    feature_cols = ['lat', 'lon', 'dayofyear', 'month', 'year'] + [c.lower() for c in extra_cols]
    X = df[feature_cols]
    y = df[['temp', 'humidity', 'wind']]

    # Impute missing feature values with median
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols)

    # Compute simple stats for UI hints
    stats = {c: {'min': float(X_imputed[c].min()), 'max': float(X_imputed[c].max()), 'median': float(X_imputed[c].median())} for c in feature_cols}

    return X_imputed, y, feature_cols, imputer, stats


def main(csv_path):
    df = pd.read_csv(csv_path)
    X, y, feature_cols, imputer, stats = prepare(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    print('Training MultiOutput RandomForestRegressor...')
    base = RandomForestRegressor(n_estimators=300, n_jobs=-1, random_state=42)
    model = MultiOutputRegressor(base)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print('Test MSE:', mse)

    # Save model and metadata together
    meta = {
        'model': model,
        'features': feature_cols,
        'imputer': imputer,
        'feature_stats': stats,
        'target_names': ['temp', 'humidity', 'wind']
    }
    joblib.dump(meta, 'model.joblib')
    # also save a human-readable metadata file
    with open('model_meta.json', 'w') as f:
        json.dump({'features': feature_cols, 'feature_stats': stats, 'target_names': ['temp','humidity','wind']}, f, indent=2)

    print('Saved model and metadata to model.joblib and model_meta.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=False, default=r'C:\Users\91932\Downloads\Global_Weather_5Years_2000Rows.csv')
    args = parser.parse_args()
    main(args.csv)
