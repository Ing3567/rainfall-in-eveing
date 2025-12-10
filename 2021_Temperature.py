import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # เพิ่ม seaborn เพื่อสร้างกราฟที่สวยงามและมีเส้นแนวโน้ม

def plot_temp_rain_scatter_2021(file_path):
    """
    This function creates a scatter plot to show the relationship between 
    average temperature and total rainfall for each day of 2021, 
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
    
    # --- CHANGE 1: Filter data for the year 2021 only ---
    df_2021 = df[df['time'].dt.year == 2021].copy()
    
    if df_2021.empty:
        # --- CHANGE 2: Update print message ---
        print("No data found for the year 2021 in the file.")
        return
        
    # Filter data for the time period 16:00 - 18:00
    df_filtered_time = df_2021[(df_2021['time'].dt.hour >= 16) & (df_2021['time'].dt.hour <= 18)].copy()
    if df_filtered_time.empty:
        # --- CHANGE 3: Update print message ---
        print("No data found for the 16:00-18:00 time period in 2021.")
        return
        
    # --- 2. Daily Data Aggregation ---
    # Group by date and calculate the 'sum' of rain and the 'mean' of temperature
    daily_summary = df_filtered_time.groupby(df_filtered_time['time'].dt.date).agg({
        'rain (mm)': 'sum',
        'temperature_2m (°C)': 'mean'
    }).reset_index()

    # --- 3. Create Scatter Plot ---
    
    plt.figure(figsize=(10, 6)) # Set the figure size
    
    # Use seaborn's regplot to create a scatter plot with a regression line (trendline)
    sns.regplot(
        data=daily_summary, 
        x='temperature_2m (°C)', 
        y='rain (mm)',
        scatter_kws={'alpha': 0.6, 'edgecolor': 'w'}, # Style for the points
        line_kws={'color': 'red'}                       # Style for the trendline
    )
    
    # --- 4. Plot Styling (with English labels) ---
    
    # --- CHANGE 4: Update plot title ---
    plt.title('Temperature vs. Rain (mm) (Daily Summary 4:00 PM - 6:00 PM) in 2021', fontsize=16)
    plt.xlabel('Average Temperature (°C)', fontsize=12)
    plt.ylabel('Total Rainfall (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# Function Call
# -------------------------------------------------------------
file_name = 'weather_2021-2025.csv'
# --- CHANGE 5: Call the new function ---
plot_temp_rain_scatter_2021(file_name)