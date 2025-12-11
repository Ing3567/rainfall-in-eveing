import pandas as pd

def load_data(file_path):
    try:
        return pd.read_csv(file_path, skiprows=3)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def Clean_data(data):
    if data is None: return None
    
   
    data['time'] = pd.to_datetime(data['time'])
    
   
    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    data['hour'] = data['time'].dt.hour
    data['month_name'] = data['time'].dt.month_name()
    data['date'] = data['time'].dt.date
    
    
    data['is_raining'] = data['rain (mm)'] > 0.0
    
    return data