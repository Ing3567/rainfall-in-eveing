import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from main import load_data
from Clean import Clean_data



if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="weather_2021-2025.csv", help="Path to the CSV data file")
    args = p.parse_args()
    data = load_data(args.file)
    data = Clean_data(data)
    data['is_raining'] = data['is_raining'].astype(str)


    features = ['temperature_2m (°C)', 'relative_humidity_2m (%)', 'wind_speed_10m (km/h)', 'surface_pressure (hPa)']
    feature_names_th = ['Temperature', 'Humidity', 'Wind Speed', 'Pressure']


    grouped_stats = data.groupby('is_raining')[features].mean()
    count_stats = data['is_raining'].value_counts()

    print("--- Average Values: Raining vs Not Raining ---")
    print(grouped_stats)
    print("\n--- Count of Hours ---")
    print(count_stats)


    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    sns.set(style="whitegrid")

    for i, col in enumerate(features):
        sns.boxplot(x='is_raining', y=col, data=data,hue='is_raining',legend=False, ax=axes[i], palette={"False": "orange", "True": "blue"})
        axes[i].set_title(f'{feature_names_th[i]} vs Rain Status')
        axes[i].set_xlabel('Is it Raining?')
        axes[i].set_xticklabels(['No Rain', 'Rain'])

    plt.tight_layout()
    plt.savefig('rain_vs_norain_comparison.png')