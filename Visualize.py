import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_theme(style="whitegrid")

def plot_time_seri(df):
    if 'hour' not in df.columns or 'is_raining' not in df.columns:
        print("Error: Missing 'hour' or 'is_raining' columns.")
        return

    hourly_prob = df.groupby('hour')['is_raining'].mean() * 100
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=hourly_prob.index, y=hourly_prob.values, marker='o', color='b')
    
    plt.title("Chance of Rain by Hour (โอกาสฝนตกรายชั่วโมง)")
    plt.xlabel("Hour of Day (0-23)")
    plt.ylabel("Probability of Rain (%)")
    plt.xticks(range(0, 24)) 
    plt.axvspan(16, 18, color='orange', alpha=0.2, label='Evening (16-18 hrs)') 
    plt.legend()
    plt.show()

def plot_monthly_heatmap(df):
    if 'time' in df.columns:
        df['month'] = df['time'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    pivot = df.pivot_table(index='month', columns='hour', values='is_raining', aggfunc='mean')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap='Blues', annot=False)
    plt.title("Rainfall Probability Heatmap (Month vs Hour)")
    plt.show()

def plot_yearly_total(df):
    yearly = df.groupby('year')['rain (mm)'].sum().reset_index()
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=yearly, x='year', y='rain (mm)', palette='viridis')
    plt.title("Total Rainfall per Year")
    plt.ylabel("Total Rain (mm)")
    plt.show()

def plot_correlation(df):
    cols = ['rain (mm)', 'temperature_2m (°C)', 'relative_humidity_2m (%)', 
            'wind_speed_10m (km/h)', 'pressure_msl (hPa)']
    corr = df[cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Weather Variables Correlation")
    plt.show()

def plot_scatter_custom(df):
    print("\n--- Custom Scatter Plot ---")
    print("ฟังก์ชันนี้จะช่วยคุณดูความสัมพันธ์ (Correlation) ระหว่าง 2 ตัวแปร")
    

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    print("Available numeric columns:", numeric_cols)
    

    col_x = input("Enter Column for X-axis (e.g., temperature_2m (°C)): ").strip()
    if col_x not in df.columns:
        print(f"Error: Column '{col_x}' not found.")
        return


    col_y = input("Enter Column for Y-axis (e.g., rain (mm)): ").strip()
    if col_y not in df.columns:
        print(f"Error: Column '{col_y}' not found.")
        return


    plt.figure(figsize=(10, 6))
    

    sns.regplot(data=df, x=col_x, y=col_y, 
                scatter_kws={'alpha':0.5}, 
                line_kws={'color':'red'}) 
    
    plt.title(f"Correlation: {col_x} vs {col_y}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_boxplot(df):
    print("\n--- Select Boxplot Mode ---")
    print("1: Monthly (ดูการกระจายตัวรายเดือน - รวมทุกปี)")
    print("2: Hourly  (ดูการกระจายตัวรายชั่วโมง - รวมทุกปี)")
    print("3: Yearly  (เปรียบเทียบข้อมูลระหว่างปี)") 
    mode = input("Enter mode (1, 2, or 3): ").strip()
    
    print("\nAvailable columns:", df.columns.tolist())
    input_col = input("Enter column name (e.g., temperature_2m (°C)): ").strip()
    
    if input_col not in df.columns:
        print(f"Error: Column '{input_col}' not found.")
        return

    # แปลงข้อมูลเวลาให้พร้อมใช้
    if 'time' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['time']):
        df['time'] = pd.to_datetime(df['time'])
    
    # สร้างคอลัมน์ year หากยังไม่มี (สำหรับ mode 3)
    if 'year' not in df.columns:
        df['year'] = df['time'].dt.year
    
    # ใช้ข้อมูลทั้งหมด (ไม่ต้องกรองปีแล้ว)
    df_selected = df.copy()
    title_suffix = "(All Years)"

    plt.figure(figsize=(14, 6))
    
    if mode == '1': 
        # Mode 1: Monthly Distribution
        df_selected['month_name'] = df_selected['time'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        # ใช้ hue เป็น month_name เพื่อแก้ warning ของ seaborn ตัวใหม่ แต่ซ่อน legend
        sns.boxplot(data=df_selected, x='month_name', y=input_col, order=month_order, palette="Set3", hue='month_name', legend=False)
        plt.xlabel("Month")
        plt.title(f"Monthly Distribution of {input_col} {title_suffix}")
        plt.xticks(rotation=45)
        
    elif mode == '2':
        # Mode 2: Hourly Distribution
        df_selected['hour'] = df_selected['time'].dt.hour
        sns.boxplot(data=df_selected, x='hour', y=input_col, palette="coolwarm", hue='hour', legend=False)
        plt.xlabel("Hour of Day (0-23)")
        plt.title(f"Hourly Distribution of {input_col} {title_suffix}")
        
    elif mode == '3': 
        # Mode 3: Yearly Comparison
        sns.boxplot(data=df_selected, x='year', y=input_col, palette="viridis", hue='year', legend=False)
        plt.xlabel("Year")
        plt.title(f"Yearly Comparison of {input_col}")
        
    else:
        print("Invalid mode selected.")
        return

    plt.ylabel(input_col)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
