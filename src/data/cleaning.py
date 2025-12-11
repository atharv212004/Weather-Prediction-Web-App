"""Data cleaning utilities for the weather project.

This module provides a function `clean_raw_csv` which attempts to map common
column names to the required schema and writes a cleaned CSV to `data/cleaned.csv`.
"""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    'date', 'year', 'month', 'day', 'dayofweek',
    'latitude', 'longitude', 'elevation',
    'temperature_max', 'temperature_min', 'temperature_avg',
    'humidity', 'wind_speed', 'wind_direction', 'pressure',
    'rainfall_mm', 'weather_description', 'cloud_cover', 'visibility'
]


def _find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def clean_raw_csv(raw_csv_path, out_path=None):
    raw_csv_path = Path(raw_csv_path)
    if out_path is None:
        out_path = raw_csv_path.parent / 'cleaned.csv'

    df = pd.read_csv(raw_csv_path)

    # map common column names
    mapping = {}
    mapping['date'] = _find_col(df, ['date', 'Date', 'datetime', 'timestamp', 'time'])
    mapping['latitude'] = _find_col(df, ['lat', 'latitude', 'Latitude'])
    mapping['longitude'] = _find_col(df, ['lon', 'longitude', 'Longitude'])
    mapping['elevation'] = _find_col(df, ['elevation', 'altitude', 'elev'])
    mapping['temperature_max'] = _find_col(df, ['temp_max', 'tmax', 'temperature_max', 'Temperature_Max'])
    mapping['temperature_min'] = _find_col(df, ['temp_min', 'tmin', 'temperature_min', 'Temperature_Min'])
    mapping['temperature_avg'] = _find_col(df, ['temp', 'temperature', 'temp_avg', 'temperature_avg', 'Temperature'])
    mapping['humidity'] = _find_col(df, ['humidity', 'Humidity', 'hum'])
    mapping['wind_speed'] = _find_col(df, ['wind_speed', 'windspeed', 'wind'])
    mapping['wind_direction'] = _find_col(df, ['wind_dir', 'wind_direction', 'winddir'])
    mapping['pressure'] = _find_col(df, ['pressure', 'Pressure', 'atm_pressure'])
    mapping['rainfall_mm'] = _find_col(df, ['rain', 'rain_mm', 'precip', 'precipitation'])
    mapping['weather_description'] = _find_col(df, ['weather', 'weather_description', 'condition'])
    mapping['cloud_cover'] = _find_col(df, ['cloudcover', 'cloud_cover', 'clouds'])
    mapping['visibility'] = _find_col(df, ['visibility', 'vis'])

    # Build cleaned df with columns where possible
    cleaned = pd.DataFrame()
    # date first
    if mapping['date']:
        cleaned['date'] = pd.to_datetime(df[mapping['date']], errors='coerce')
    else:
        raise ValueError('Could not find a date column in raw CSV')

    # derived date fields
    cleaned['year'] = cleaned['date'].dt.year
    cleaned['month'] = cleaned['date'].dt.month
    cleaned['day'] = cleaned['date'].dt.day
    cleaned['dayofweek'] = cleaned['date'].dt.dayofweek

    # core columns
    def pull(colkey, default=None):
        src = mapping.get(colkey)
        if src and src in df.columns:
            return df[src]
        return pd.Series([default]*len(df))

    cleaned['latitude'] = pull('latitude')
    cleaned['longitude'] = pull('longitude')
    cleaned['elevation'] = pull('elevation')
    cleaned['temperature_max'] = pull('temperature_max')
    cleaned['temperature_min'] = pull('temperature_min')
    # compute average if missing
    temp_avg_src = mapping.get('temperature_avg')
    if temp_avg_src and temp_avg_src in df.columns:
        cleaned['temperature_avg'] = df[temp_avg_src]
    else:
        cleaned['temperature_avg'] = cleaned[['temperature_max', 'temperature_min']].mean(axis=1)

    cleaned['humidity'] = pull('humidity')
    cleaned['wind_speed'] = pull('wind_speed')
    cleaned['wind_direction'] = pull('wind_direction')
    cleaned['pressure'] = pull('pressure')
    cleaned['rainfall_mm'] = pull('rainfall_mm', 0)
    cleaned['weather_description'] = pull('weather_description', '')
    cleaned['cloud_cover'] = pull('cloud_cover')
    cleaned['visibility'] = pull('visibility')

    # drop rows missing essential fields
    cleaned = cleaned.dropna(subset=['date', 'latitude', 'longitude', 'temperature_avg'])

    # Clip ranges and types
    cleaned['latitude'] = pd.to_numeric(cleaned['latitude'], errors='coerce').clip(-90, 90)
    cleaned['longitude'] = pd.to_numeric(cleaned['longitude'], errors='coerce').clip(-180, 180)
    cleaned['temperature_avg'] = pd.to_numeric(cleaned['temperature_avg'], errors='coerce')
    cleaned['humidity'] = pd.to_numeric(cleaned['humidity'], errors='coerce').clip(0, 100)
    cleaned['wind_speed'] = pd.to_numeric(cleaned['wind_speed'], errors='coerce').clip(0)

    cleaned = cleaned.dropna(subset=['latitude', 'longitude', 'temperature_avg'])

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(out_path, index=False)
    return out_path


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python cleaning.py path/to/raw.csv')
        sys.exit(1)
    res = clean_raw_csv(sys.argv[1])
    print('Wrote cleaned CSV to', res)
