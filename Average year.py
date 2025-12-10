import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from Clean import Clean_data
from main import load_data

def plot_comparison(data, col, title_suffix, ylabel, filename):  
    long_term_avg = data.groupby('month')[col].mean()
    yearly_patterns = data.groupby(['year', 'month'])[col].mean().unstack(level=0)

   
    plt.figure(figsize=(12, 6))
    
    
    for year in yearly_patterns.columns:
        plt.plot(yearly_patterns.index, yearly_patterns[year], label=f'Year {year}', alpha=0.5, linestyle='--')
    
    
    plt.plot(long_term_avg.index, long_term_avg.values, label='5-Year Average (Model)', color='black', linewidth=3)
    
    
    plt.title(f'Comparison: 5-Year Average vs. Single Year Data ({title_suffix})', fontsize=14)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.xticks(range(1, 13))
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close() 

    
    std_dev = yearly_patterns.std(axis=1).mean()
    print(f"Average Monthly Variability (Std Dev) for {title_suffix}: {std_dev:.2f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="weather_2021-2025.csv", help="Path to the CSV data file")
    args = p.parse_args()

    
    data = load_data(args.file)
    data = Clean_data(data)

    
    plot_configs = [
        ('temperature_2m (°C)', 'Temperature', 'Temperature (°C)', 'seasonality_comparison.png'),
        ('rain (mm)', 'Rainfall', 'Rain (mm/hour)', 'seasonality_comparison_rain.png'),
        ('relative_humidity_2m (%)', 'Relative Humidity', 'Relative Humidity (%)', 'seasonality_comparison_relative_humidity.png'),
        ('wind_speed_10m (km/h)', 'Wind Speed', 'Wind Speed (km/h)', 'seasonality_comparison_wind_speed.png'),
        ('pressure_msl (hPa)', 'Pressure MSL', 'Pressure (hPa)', 'seasonality_comparison_pressure.png')
    ]

    
    for col, title, ylabel, fname in plot_configs:
        plot_comparison(data, col, title, ylabel, fname)