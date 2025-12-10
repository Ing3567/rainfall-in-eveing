import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_humidity_rain_scatter_2023(file_path):
    """
    This function creates a scatter plot to show the relationship between 
    average relative humidity and total rainfall for each day of 2023, 
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
    
    # --- CHANGE 1: Filter data for the year 2023 only ---
    df_2023 = df[df['time'].dt.year == 2023].copy()
    
    if df_2023.empty:
        # --- CHANGE 2: Update print message ---
        print("No data found for the year 2023 in the file.")
        return
        
    # Filter data for the time period 16:00 - 18:00
    df_filtered_time = df_2023[(df_2023['time'].dt.hour >= 16) & (df_2023['time'].dt.hour <= 18)].copy()
    if df_filtered_time.empty:
        # --- CHANGE 3: Update print message ---
        print("No data found for the 16:00-18:00 time period in 2023.")
        return
        
    # --- 2. Daily Data Aggregation ---
    # Group by date and calculate the 'sum' of rain and the 'mean' of humidity
    daily_summary = df_filtered_time.groupby(df_filtered_time['time'].dt.date).agg({
        'rain (mm)': 'sum',
        'relative_humidity_2m (%)': 'mean' 
    }).reset_index()

    # --- 3. Create Scatter Plot ---
    
    plt.figure(figsize=(10, 6)) # Set the figure size
    
    # Use seaborn's regplot for a scatter plot with a regression line
    sns.regplot(
        data=daily_summary, 
        x='relative_humidity_2m (%)',  
        y='rain (mm)',                 
        scatter_kws={'alpha': 0.6, 'color': 'green'}, # Style for the points
        line_kws={'color': 'darkred'}                 # Style for the trendline
    )
    
    # --- 4. Plot Styling (with English labels) ---
    
    # --- CHANGE 4: Update plot title ---
    plt.title('Relative Humidity vs. Rain (mm) (Daily Summary 4:00 PM - 6:00 PM) in 2023', fontsize=16)
    plt.xlabel('Average Relative Humidity (%)', fontsize=12)
    plt.ylabel('Total Rainfall (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# Function Call
# -------------------------------------------------------------
file_name = 'weather_2021-2025.csv'
# --- CHANGE 5: Call the new function ---
plot_humidity_rain_scatter_2023(file_name)