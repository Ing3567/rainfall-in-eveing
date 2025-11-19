import argparse
import pandas as pd
from Clean import Clean_data, check_rain_in_evening
from Visualize import plot_correlation, plot_hourly_rain_prob, plot_boxplot, plot_monthly_heatmap, plot_yearly_total , plot_scatter_custom

def load_data(file_path):
    return pd.read_csv(file_path, skiprows=3)


def summary_data(data,groupy,type):
    summary = data.groupby(groupy).agg({
        'rain (mm)': type,
        'temperature_2m (°C)': type,
        'relative_humidity_2m (%)': type,
        'wind_speed_10m (km/h)': type,
        'pressure_msl (hPa)': type
    }).reset_index()
    summary.rename(columns={
        'rain (mm)': 'total_rain_mm',
        'temperature_2m (°C)': 'avg_temp_C',
        'relative_humidity_2m (%)': 'avg_humidity_percent',
        'wind_speed_10m (km/h)': 'avg_wind_speed_kmh',
        'pressure_msl (hPa)': 'avg_pressure_hPa'
    }, inplace=True)
    return summary




if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="weather_2021-2025.csv", help="Path to the CSV data file")
    p.add_argument("--eveing", default=True, help="summary data" ,type=bool)
    p.add_argument("--group", default="year", help="group by column")
    p.add_argument("--type", default="mean", help="aggregation type: sum or mean")
    p.add_argument("--plot", default="none", 
                   choices=["none", "line", "heatmap", "bar", "corr", "box"], 
                   help="Select plot type: line, heatmap, bar, corr")
    args = p.parse_args()
    file_path = args.file
    data = load_data(file_path)
    data = Clean_data(data)
    print(data.info())
    print(data.describe())
    if args.eveing:
        rain_summary = check_rain_in_evening(data)
        print(rain_summary)
    else:
        summary = summary_data(data,args.group,args.type)
        print(summary)
    if args.plot != "none":
        print(f"\n--- Generating Plot: {args.plot} ---")
        if args.plot == "line":
            plot_hourly_rain_prob(data)
        elif args.plot == "heatmap":
            plot_monthly_heatmap(data)
        elif args.plot == "bar":
            plot_yearly_total(data)
        elif args.plot == "corr":
            plot_correlation(data)
        elif args.plot == "box": 
            plot_boxplot(data)
        elif args.plot == "scat":
            plot_scatter_custom(data)

    