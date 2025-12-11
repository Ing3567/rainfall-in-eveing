import argparse
from Clean import load_data, Clean_data
from Analysis import summary_data, analyze_rain_drivers, compare_rain_vs_norain, prepare_evening_data
import Visualize as vis

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Weather Data Analysis Tool")
    p.add_argument("--file", default="data/weather_2021-2025.csv", help="CSV file path")
    p.add_argument("--mode", default="summary", 
                   choices=["summary", "rain_drivers", "rain_comparison"],
                   help="Analysis mode: summary stats, ML drivers, or Rain/NoRain comp")
    p.add_argument("--plot", default="none", 
                   choices=["none", "timeseries", "heatmap", "boxplot", "seasonality", 
                            "drivers", "humidity_kde", "evening_scatter", "evening_trend"], 
                   help="Select plot type")
    p.add_argument("--col", default="temperature_2m (°C)", help="Column name for analysis")
    p.add_argument("--year", default=None, help="Specific year (e.g., 2024) for evening plots")
    args = p.parse_args()


    print("Loading data...")
    data = load_data(args.file)
    if data is None: exit()
    data = Clean_data(data)
    if args.plot == "none":
        print(f"\n--- Mode: {args.mode} ---")
        if args.mode == "summary":
            print(summary_data(data, 'year'))
        elif args.mode == "rain_drivers":
            print("Calculating Feature Importance (Random Forest)...")
            print(analyze_rain_drivers(data))
        elif args.mode == "rain_comparison":
            stats, counts = compare_rain_vs_norain(data)
            print("Average Values (Rain vs No Rain):")
            print(stats)
    else:
        print(f"\n--- Generating Plot: {args.plot} ---")
        if args.plot == "timeseries": vis.plot_time_series(data)
        elif args.plot == "heatmap": vis.plot_monthly_heatmap(data)
        elif args.plot == "boxplot": vis.plot_boxplot(data, args.col, mode='hourly')
        elif args.plot == "seasonality": vis.plot_seasonality_comparison(data, args.col, "Custom", args.col)
        elif args.plot == "drivers": vis.plot_rain_drivers_prob(data)
        elif args.plot == "humidity_kde": vis.plot_humidity_kde(data)
        elif args.plot in ["evening_scatter", "evening_trend"]:
            evening_data = prepare_evening_data(data, year=args.year)
            year_label = args.year if args.year else "All Years"
            if evening_data.empty:
                print(f"No data found for year {year_label}")
            else:
                if args.plot == "evening_scatter":
                    vis.plot_evening_scatter(evening_data, args.col, year_label)
                elif args.plot == "evening_trend":
                    vis.plot_evening_rain_trend(evening_data, year_label)