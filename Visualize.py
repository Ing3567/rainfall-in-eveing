import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ตั้งค่าสไตล์ของกราฟให้สวยงาม
sns.set_theme(style="whitegrid", font="Tahoma") # เปลี่ยน font เป็น Tahoma เพื่อรองรับภาษาไทย

# ==============================================================================
# โค้ดเดิมที่ให้มา (ปรับปรุงเล็กน้อยเพื่อความสอดคล้องกัน)
# ==============================================================================

def plot_hourly_rain_prob(df):
    if 'hour' not in df.columns or 'is_raining' not in df.columns:
        print("Error: Missing 'hour' or 'is_raining' columns.")
        return
    hourly_prob = df.groupby('hour')['is_raining'].mean() * 100
    
    plt.figure(figsize=(12, 7))
    sns.lineplot(x=hourly_prob.index, y=hourly_prob.values, marker='o', color='b')
    
    plt.title("โอกาสฝนตกรายชั่วโมง (Chance of Rain by Hour)")
    plt.xlabel("ชั่วโมง (Hour of Day, 0-23)")
    plt.ylabel("ความน่าจะเป็นที่จะมีฝน (%)")
    plt.xticks(range(0, 24)) 
    plt.axvspan(16, 18, color='orange', alpha=0.2, label='ช่วงเย็น (16:00-18:00)') 
    plt.legend()
    plt.show()

def plot_monthly_heatmap(df):
    if 'time' not in df.columns:
        print("Error: 'time' column not found.")
        return
        
    df_copy = df.copy()
    df_copy['month'] = df_copy['time'].dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_copy['month'] = pd.Categorical(df_copy['month'], categories=month_order, ordered=True)
    pivot = df_copy.pivot_table(index='month', columns='hour', values='is_raining', aggfunc='mean')
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot, cmap='Blues', annot=False)
    plt.title("Heatmap โอกาสฝนตก (รายเดือน vs รายชั่วโมง)")
    plt.show()

def plot_yearly_total(df):
    yearly = df.groupby('year')['rain (mm)'].sum().reset_index()
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=yearly, x='year', y='rain (mm)', palette='viridis')
    plt.title("ปริมาณน้ำฝนรวมในแต่ละปี")
    plt.ylabel("ปริมาณน้ำฝนรวม (mm)")
    plt.xlabel("ปี")
    plt.show()

def plot_correlation(df):
    cols = ['rain (mm)', 'temperature_2m (°C)', 'relative_humidity_2m (%)', 
            'wind_speed_10m (km/h)', 'pressure_msl (hPa)']
    corr = df[cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix ของตัวแปรสภาพอากาศ")
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
    
    plt.title(f"ความสัมพันธ์ระหว่าง: {col_x} vs {col_y}")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_boxplot(df):
    print("\n--- Select Boxplot Mode ---")
    print("1: Monthly (ดูการกระจายตัวรายเดือน)")
    print("2: Hourly  (ดูการกระจายตัวรายชั่วโมง)")
    print("3: Yearly  (เปรียบเทียบข้อมูลระหว่างปี)") 
    mode = input("Enter mode (1, 2, or 3): ").strip()
    
    print("\nAvailable columns:", df.columns.tolist())
    input_col = input("Enter column name (e.g., temperature_2m (°C)): ").strip()
    
    if input_col not in df.columns:
        print(f"Error: Column '{input_col}' not found.")
        return
   
    df_selected = df.copy()
    title_suffix = "(All Years)"

    if mode in ['1', '2']:
        print("\n(Optional) Enter a specific year to filter, or press Enter to see all years.")
        input_year = input("Enter year (e.g., 2023): ").strip()
        
        if input_year.isdigit():
            target_year = int(input_year)
            df_selected = df[df['year'] == target_year].copy()
            title_suffix = f"in {target_year}"
            
            if df_selected.empty:
                print(f"No data found for year {target_year}")
                return
   
    plt.figure(figsize=(14, 7))
    
    if mode == '1': 
        df_selected['month_name'] = df_selected['time'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        sns.boxplot(data=df_selected, x='month_name', y=input_col, order=month_order, palette="Set3")
        plt.xlabel("Month")
        plt.title(f"Monthly Distribution of {input_col} {title_suffix}")
        plt.xticks(rotation=45)
        
    elif mode == '2':
        sns.boxplot(data=df_selected, x='hour', y=input_col, palette="coolwarm")
        plt.xlabel("Hour of Day (0-23)")
        plt.title(f"Hourly Distribution of {input_col} {title_suffix}")
        
    elif mode == '3': 
        sns.boxplot(data=df_selected, x='year', y=input_col, palette="viridis")
        plt.xlabel("Year")
        plt.title(f"Yearly Comparison of {input_col}")
        
    else:
        print("Invalid mode selected.")
        return

    plt.ylabel(input_col)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# ==============================================================================
# ฟังก์ชันใหม่ที่สร้างขึ้นตามโจทย์ที่ต้องการ
# ==============================================================================
def plot_daily_evening_rain_2024(df):
    """
    ฟังก์ชันนี้จะสร้างกราฟแสดงปริมาณฝนรวมในแต่ละวันของปี 2024 
    โดยพิจารณาข้อมูลเฉพาะช่วงเวลา 16:00 - 18:00 น.
    """
    print("\nกำลังสร้างกราฟปริมาณฝนรายวัน ปี 2024 (16:00-18:00)...")

    # 1. กรองข้อมูลให้เหลือเฉพาะปี 2024
    df_2024 = df[df['year'] == 2024].copy()

    if df_2024.empty:
        print("ไม่พบข้อมูลสำหรับปี 2024 ใน Dataset")
        return

    # 2. กรองข้อมูลให้เหลือเฉพาะช่วงเวลา 16:00, 17:00 และ 18:00
    evening_hours = [16, 17, 18]
    df_evening = df_2024[df_2024['hour'].isin(evening_hours)]

    if df_evening.empty:
        print("ไม่พบข้อมูลในช่วงเวลา 16:00-18:00 ของปี 2024")
        return

    # 3. รวมปริมาณน้ำฝนในแต่ละวัน (Group by วันที่ และ Sum ค่า rain)
    #    ใช้ .dt.date เพื่อไม่ให้เวลามาปน
    daily_rain_sum = df_evening.groupby(df_evening['time'].dt.date)['rain (mm)'].sum()
    
    # แปลง index (ที่เป็น date object) กลับเป็น datetime เพื่อให้ plot ง่าย
    daily_rain_sum.index = pd.to_datetime(daily_rain_sum.index)

    # 4. สร้างกราฟเส้น (Line Plot)
    plt.figure(figsize=(15, 7)) # กำหนดขนาดกราฟให้กว้างพอสำหรับข้อมูลทั้งปี
    sns.lineplot(x=daily_rain_sum.index, y=daily_rain_sum.values, color='dodgerblue')

    # 5. ปรับแต่งรายละเอียดกราฟ
    plt.title('ปริมาณฝนรวมรายวัน ปี 2024 (ช่วงเวลา 16:00 - 18:00 น.)')
    plt.xlabel('วันที่ (Date)')
    plt.ylabel('ปริมาณฝนรวม (mm)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45) # หมุนป้ายแกน X เพื่อให้อ่านง่ายขึ้น
    plt.tight_layout() #ปรับกราฟให้อัตโนมัติ
    plt.show()


# ==============================================================================
# Main Function - ส่วนหลักในการรันโปรแกรม
# ==============================================================================
def main():
    """
    ฟังก์ชันหลักสำหรับโหลดข้อมูลและเรียกใช้ฟังก์ชันสร้างกราฟต่างๆ ผ่านเมนู
    """
    file_path = 'weather_2021-2025.csv'
    
    try:
        # โหลดข้อมูลและประมวลผลเบื้องต้นแค่ครั้งเดียว
        print(f"กำลังโหลดข้อมูลจาก '{file_path}'...")
        df = pd.read_csv(file_path)
        
        # --- การประมวลผลข้อมูลล่วงหน้า (Preprocessing) ---
        # 1. แปลงคอลัมน์ 'time' ให้เป็น datetime object ซึ่งสำคัญมาก
        df['time'] = pd.to_datetime(df['time'])
        
        # 2. สร้างคอลัมน์ 'year', 'hour', 'is_raining' ไว้ล่วงหน้าเพื่อให้ฟังก์ชันอื่นเรียกใช้ง่าย
        df['year'] = df['time'].dt.year
        df['hour'] = df['time'].dt.hour
        df['is_raining'] = (df['rain (mm)'] > 0).astype(int)
        
        print("โหลดข้อมูลและประมวลผลเบื้องต้นสำเร็จ!")
        
    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ '{file_path}' กรุณาตรวจสอบว่าไฟล์อยู่ในตำแหน่งที่ถูกต้อง")
        return # ออกจากโปรแกรมถ้าไม่เจอไฟล์

    # สร้างเมนูให้ผู้ใช้เลือก
    while True:
        print("\n" + "="*30)
        print("  Weather Data Analysis Menu")
        print("="*30)
        print("เลือกกราฟที่ต้องการสร้าง:")
        print("1. โอกาสฝนตกรายชั่วโมง (Chance of Rain by Hour)")
        print("2. Heatmap โอกาสฝนตก (รายเดือน vs รายชั่วโมง)")
        print("3. ปริมาณน้ำฝนรวมรายปี (Total Rainfall per Year)")
        print("4. Correlation Matrix ของตัวแปรสภาพอากาศ")
        print("5. Box Plot (การกระจายตัวของข้อมูล)")
        print("6. Scatter Plot (ความสัมพันธ์ระหว่าง 2 ตัวแปร)")
        print("7. กราฟปริมาณฝนรายวัน ปี 2024 (16:00-18:00) <-- ตามโจทย์")
        print("0. ออกจากโปรแกรม (Exit)")
        
        choice = input("กรุณาเลือกตัวเลือก (0-7): ").strip()

        if choice == '1':
            plot_hourly_rain_prob(df)
        elif choice == '2':
            plot_monthly_heatmap(df)
        elif choice == '3':
            plot_yearly_total(df)
        elif choice == '4':
            plot_correlation(df)
        elif choice == '5':
            plot_boxplot(df)
        elif choice == '6':
            plot_scatter_custom(df)
        elif choice == '7':
            plot_daily_evening_rain_2024(df) # เรียกใช้ฟังก์ชันใหม่
        elif choice == '0':
            print("ออกจากโปรแกรม")
            break
        else:
            print("ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")


if __name__ == "__main__":
    main()