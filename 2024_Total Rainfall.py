import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_daily_rainfall_16_18(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=3, engine='python')
        
    except FileNotFoundError:
        print(f"ข้อผิดพลาด: ไม่พบไฟล์ที่ระบุที่ {file_path}")
        return
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV: {e}")
        return

    # แปลงคอลัมน์ 'time' ให้เป็น datetime object
    df['time'] = pd.to_datetime(df['time'])
    
    # กรองข้อมูลสำหรับปี 2024 เท่านั้น
    df_2024 = df[df['time'].dt.year == 2024].copy()
    if df_2024.empty:
        print("ไม่พบข้อมูลสำหรับปี 2024 ในไฟล์.")
        return
        
    # กรองข้อมูลสำหรับช่วงเวลา 16:00 - 18:00 น.
    df_filtered_time = df_2024[(df_2024['time'].dt.hour >= 16) & (df_2024['time'].dt.hour <= 18)].copy()
    if df_filtered_time.empty:
        print("ไม่พบข้อมูลในช่วงเวลา 16:00-18:00 น. สำหรับปี 2024.")
        return
        
    # รวมปริมาณฝนรายวัน
    daily_rainfall_16_18 = df_filtered_time.groupby(df_filtered_time['time'].dt.date)['rain (mm)'].sum().reset_index()
    daily_rainfall_16_18.columns = ['date', 'total_rain_16_18mm']
    
    daily_rainfall_16_18['date'] = pd.to_datetime(daily_rainfall_16_18['date'])
    
    # สร้างกราฟ
    plt.figure(figsize=(15, 7))
    plt.plot(daily_rainfall_16_18['date'], daily_rainfall_16_18['total_rain_16_18mm'], marker='o', linestyle='-', color='skyblue', markersize=4)
    
    # ปรับแต่งแกน X เพื่อแสดงวันที่ได้อย่างสวยงาม
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator()) 
    
    plt.gcf().autofmt_xdate() 
    
    plt.title('Daily Total Rainfall (4:00 PM - 6:00 PM) in 2024', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Rain (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# เรียกใช้ฟังก์ชัน
file_name = 'weather_2021-2025.csv'
plot_daily_rainfall_16_18(file_name)