import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.dates as mdates

sns.set_theme(style="whitegrid")

def plot_time_series(df):
    if 'hour' not in df.columns: return
    hourly_prob = df.groupby('hour')['is_raining'].mean() * 100
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=hourly_prob.index, y=hourly_prob.values, marker='o', color='b')
    plt.title("Chance of Rain by Hour")
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Probability (%)")
    plt.xticks(range(0, 24))
    plt.axvspan(16, 18, color='orange', alpha=0.2, label='Evening (16-18)')
    plt.legend()
    plt.show()

def plot_monthly_heatmap(df):
    pivot = df.pivot_table(index='month', columns='hour', values='is_raining', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap='Blues', annot=False)
    plt.title("Rainfall Probability Heatmap")
    plt.show()

def plot_boxplot(df, col_name, mode='monthly'):
    plt.figure(figsize=(12, 6))
    if mode == 'monthly':
        sns.boxplot(data=df, x='month', y=col_name, palette="Set3", hue='month', legend=False)
        plt.xlabel("Month")
    elif mode == 'hourly':
        sns.boxplot(data=df, x='hour', y=col_name, palette="coolwarm", hue='hour', legend=False)
        plt.xlabel("Hour")
    elif mode == 'yearly':
        sns.boxplot(data=df, x='year', y=col_name, palette="viridis", hue='year', legend=False)
        plt.xlabel("Year")
    plt.title(f"Distribution of {col_name} ({mode})")
    plt.show()

def plot_seasonality_comparison(data, col, title_suffix, ylabel):
    long_term_avg = data.groupby('month')[col].mean()
    yearly_patterns = data.groupby(['year', 'month'])[col].mean().unstack(level=0)

    plt.figure(figsize=(12, 6))
    for year in yearly_patterns.columns:
        plt.plot(yearly_patterns.index, yearly_patterns[year], label=f'{year}', alpha=0.5, linestyle='--')
    
    plt.plot(long_term_avg.index, long_term_avg.values, label='5-Year Avg', color='black', linewidth=3)
    plt.title(f'Seasonality: 5-Year Avg vs Single Years ({title_suffix})')
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.xticks(range(1, 13))
    plt.legend()
    plt.show()

def plot_rain_drivers_prob(df):
    features = ['surface_pressure (hPa)', 'wind_speed_10m (km/h)', 'temperature_2m (°C)']
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for i, feature in enumerate(features):
        df['bin'] = pd.qcut(df[feature], q=10, duplicates='drop')
        prob = df.groupby('bin', observed=False)['is_raining'].mean() * 100
        mid_points = [b.mid for b in prob.index]
        
        sns.lineplot(x=mid_points, y=prob.values, marker='o', ax=axes[i], color='red')
        axes[i].set_title(f"Rain Prob vs {feature}")
        axes[i].set_ylabel("Chance (%)")
    
    plt.tight_layout()
    plt.show()

def plot_humidity_kde(df):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='relative_humidity_2m (%)', hue='is_raining', fill=True, common_norm=False, palette={False: "orange", True: "blue"})
    plt.title('Humidity Distribution: Rain vs No Rain')
    plt.show()

def plot_evening_scatter(daily_data, x_col, year_label):
    plt.figure(figsize=(10, 6))
    
    # กำหนดสีอัตโนมัติ
    color_map = {
        'temperature_2m (°C)': ('red', 'orange'),
        'relative_humidity_2m (%)': ('darkred', 'green'),
        'wind_speed_10m (km/h)': ('darkred', 'purple'),
        'pressure_msl (hPa)': ('darkblue', 'cyan')
    }
    line_c, point_c = color_map.get(x_col, ('black', 'blue'))

    sns.regplot(
        data=daily_data, 
        x=x_col, 
        y='rain (mm)',
        scatter_kws={'alpha': 0.6, 'color': point_c, 'edgecolor': 'w'},
        line_kws={'color': line_c}
    )
    
    plt.title(f'{x_col} vs Rain (Evening 16:00-18:00) - Year: {year_label}', fontsize=14)
    plt.xlabel(f'Average {x_col}', fontsize=12)
    plt.ylabel('Total Rainfall (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_evening_rain_trend(daily_data, year_label):

    plt.figure(figsize=(15, 7))
    plt.plot(daily_data['date'], daily_data['rain (mm)'], marker='o', linestyle='-', color='skyblue', markersize=4)
    
    plt.title(f'Total Rainfall Daily (16:00-18:00) - Year: {year_label}', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Total Rainfall (mm)')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()