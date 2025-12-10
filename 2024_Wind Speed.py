import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_wind_rain_scatter_2024(file_path):
    """
    This function creates a scatter plot to show the relationship between 
    average wind speed and total rainfall for each day of 2024, 
    using data from 16:00 - 18:00.
    """
    try:
        # Read the CSV file, skipping the first 3 rows and using the 'python' engine.
        df = pd.read_csv(file_path, skiprows=3, engine='python')
        
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # --- 1. Data Preparation ---
    
    # Convert 'time' column to datetime objects
    df['time'] = pd.to_datetime(df['time'])
    
    # Filter data for the year 2024 only
    df_2024 = df[df['time'].dt.year == 2024].copy()
    if df_2024.empty:
        print("No data found for the year 2024 in the file.")
        return
        
    # Filter data for the time period 16:00 - 18:00
    df_filtered_time = df_2024[(df_2024['time'].dt.hour >= 16) & (df_2024['time'].dt.hour <= 18)].copy()
    if df_filtered_time.empty:
        print("No data found for the 16:00-18:00 time period in 2024.")
        return
        
    # --- 2. Daily Data Aggregation ---
    # Group by date and calculate the 'sum' of rain and the 'mean' of wind speed
    daily_summary = df_filtered_time.groupby(df_filtered_time['time'].dt.date).agg({
        'rain (mm)': 'sum',
        'wind_speed_10m (km/h)': 'mean' # <<< เปลี่ยนเป็นคอลัมน์ความเร็วลม
    }).reset_index()

    # --- 3. Create Scatter Plot ---
    
    plt.figure(figsize=(10, 6)) # Set the figure size
    
    # Use seaborn's regplot for a scatter plot with a regression line
    sns.regplot(
        data=daily_summary, 
        x='wind_speed_10m (km/h)',     # <<< แกน X คือ ความเร็วลม
        y='rain (mm)',                 # <<< แกน Y คือ ปริมาณฝน
        scatter_kws={'alpha': 0.6, 'color': 'purple'}, # Style for the points
        line_kws={'color': 'darkred'}                  # Style for the trendline
    )
    
    # --- 4. Plot Styling (with English labels) ---
    
    plt.title('Wind Speed vs. Rain (mm) (Daily Summary 4:00 PM - 6:00 PM) in 2024', fontsize=16)
    plt.xlabel('Average Wind Speed (km/h)', fontsize=12)
    plt.ylabel('Total Rainfall (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# Function Call
# -------------------------------------------------------------
file_name = 'weather_2021-2025.csv'
plot_wind_rain_scatter_2024(file_name)