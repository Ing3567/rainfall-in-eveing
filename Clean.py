import pandas as pd

def Clean_data(data):
    data['time'] = pd.to_datetime(data['time'])
    data['is_raining'] = data['rain (mm)'] > 0.01
    data['year'] = pd.to_datetime(data['time']).dt.year
    data['hour'] = pd.to_datetime(data['time']).dt.hour
    return data

def check_rain_in_evening(data):
    evening_data = data[(data['hour'] >= 16) & (data['hour'] <= 18)]
    rain_summary = evening_data.groupby('year')['is_raining'].sum().reset_index()
    rain_summary.rename(columns={'is_raining': 'rainy_evening_count'}, inplace=True)
    return rain_summary

