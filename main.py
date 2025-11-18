import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path, skiprows=3)


def add_data_rain(df):
    df['is_raining'] = df['rain (mm)'] > 0.01
    return df['is_raining']

def spilt_data_year(df):
    data['year'] = pd.to_datetime(df['time']).dt.year
    data_by_year = {}
    for year in data['year'].unique():
        data_by_year[year] = data[data['year'] == year]
    return data_by_year

def split_data_houly(df): 
    df['hour'] = pd.to_datetime(df['time']).dt.hour
    data_by_hour = {}
    for hour in df['hour'].unique():
        data_by_hour[hour] = df[df['hour'] == hour]
    return data_by_hour

def analyze_data(df):
    summary = df.describe()
    return summary

if __name__ == "__main__":
    file_path = "open-meteo-13.74N100.50E7m (1).csv"
    data = load_data(file_path)
    data['is_raining'] = add_data_rain(data)
    data_by_year = spilt_data_year(data)
    data_by_hour = split_data_houly(data)
    # print(data_by_year[2023].head())
    print(data_by_hour[0].head())
    # for year, df_year in data_by_year.items():
    #     print(f"Year: {year}")
    #     print(analyze_data(df_year))
    print(data.isnull().sum())