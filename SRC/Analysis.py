import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def summary_data(data, group_col, agg_type='mean'):
    summary = data.groupby(group_col).agg({
        'rain (mm)': agg_type,
        'temperature_2m (°C)': agg_type,
        'relative_humidity_2m (%)': agg_type,
        'wind_speed_10m (km/h)': agg_type,
        'pressure_msl (hPa)': agg_type
    }).reset_index()
    return summary

def analyze_rain_drivers(data):
    features = ['temperature_2m (°C)', 'relative_humidity_2m (%)', 
                'wind_speed_10m (km/h)', 'surface_pressure (hPa)']
    

    X = data[features].fillna(data[features].mean())
    y = data['is_raining'].astype(int)
    

    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    

    importances = pd.DataFrame({
        'Feature': features,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    return importances

def compare_rain_vs_norain(data):
    features = ['temperature_2m (°C)', 'relative_humidity_2m (%)', 
                'wind_speed_10m (km/h)', 'surface_pressure (hPa)']
    
    stats = data.groupby('is_raining')[features].mean()
    counts = data['is_raining'].value_counts()
    
    return stats, counts

def prepare_evening_data(data, year=None):
    df_evening = data[(data['hour'] >= 16) & (data['hour'] <= 18)].copy()

    if year is not None:
        df_evening = df_evening[df_evening['year'] == int(year)]
    
    if df_evening.empty:
        return pd.DataFrame()

    daily_summary = df_evening.groupby('date').agg({
        'rain (mm)': 'sum',
        'temperature_2m (°C)': 'mean',
        'relative_humidity_2m (%)': 'mean',
        'wind_speed_10m (km/h)': 'mean',
        'pressure_msl (hPa)': 'mean'
    }).reset_index()
    
    daily_summary['date'] = pd.to_datetime(daily_summary['date'])
    return daily_summary