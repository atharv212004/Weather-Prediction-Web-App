"""Utilities to query historical series from cleaned data.

Provides a function `nearest_series(lat, lon, days=365)` which returns recent
historical daily series nearest to the supplied coordinates.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree


def load_cleaned(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, parse_dates=['date'])
    return df


def nearest_series(cleaned_df, lat, lon, max_days=365, n_neighbors=500):
    # Build KDTree on lat/lon
    coords = np.vstack([cleaned_df['latitude'].values, cleaned_df['longitude'].values]).T
    tree = cKDTree(coords)
    dist, idx = tree.query([lat, lon], k=min(n_neighbors, len(coords)))
    # idx may be scalar if only one
    if np.isscalar(idx):
        idx = [idx]

    nearby = cleaned_df.iloc[idx].copy()
    # Sort by date descending and return last `max_days` unique daily averages
    nearby = nearby.sort_values('date', ascending=False)
    # group by date and average
    series = nearby.groupby(nearby['date'].dt.date).agg({'temperature_avg':'mean','humidity':'mean','wind_speed':'mean'}).reset_index()
    series = series.sort_values('date')
    # take most recent up to max_days
    series = series.tail(max_days)
    # return as lists for plotting
    return {
        'dates': series['date'].astype(str).tolist(),
        'temperature': series['temperature_avg'].round(2).tolist(),
        'humidity': series['humidity'].round(2).tolist(),
        'wind_speed': series['wind_speed'].round(2).tolist()
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('Usage: history.py cleaned.csv lat lon')
        sys.exit(1)
    df = load_cleaned(sys.argv[1])
    out = nearest_series(df, float(sys.argv[2]), float(sys.argv[3]))
    print(out)
