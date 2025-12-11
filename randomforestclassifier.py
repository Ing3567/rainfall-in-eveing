import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# 1. โหลดข้อมูล
# ใช้ชื่อไฟล์ตามที่คุณอัปโหลด
filename = 'open-meteo-13.74N100.50E7m (1).xlsx - Sheet1.csv'
# skip 3 บรรทัดแรกที่เป็น metadata
df = pd.read_csv(filename, skiprows=3)

# เปลี่ยนชื่อคอลัมน์ให้เรียกง่ายขึ้น
df.columns = ['time', 'temp', 'app_temp', 'humidity', 'rain', 'wind_speed', 'surf_pressure', 'pressure_msl']
df['time'] = pd.to_datetime(df['time'])
df['hour'] = df['time'].dt.hour
df['date'] = df['time'].dt.date

# 2. สร้าง Target: ฝนตกหรือไม่ในช่วง 16:00-18:00
# กรองเอาเฉพาะช่วงเวลาเป้าหมาย
target_hours = df[df['hour'].isin([16, 17, 18])]
# รวมผลตามวัน: ถ้ามีฝนตกในช่วงนี้ให้เป็น 1, ไม่มีเป็น 0
y = target_hours.groupby('date')['rain'].sum().apply(lambda x: 1 if x > 0 else 0).reset_index(name='target_rain')

# 3. สร้าง Features: ใช้ข้อมูลช่วง 00:00-15:00 เพื่อทำนายอนาคต
feature_hours = df[df['hour'] < 16]

# กำหนดว่าจะหาค่าอะไรบ้างจากแต่ละตัวแปร
agg_funcs = {
    'temp': ['mean', 'max', 'min'],
    'humidity': ['mean', 'max', 'min'],
    'rain': ['sum'], # ปริมาณฝนที่ตกไปแล้วในช่วงเช้า
    'wind_speed': ['mean', 'max'],
    'surf_pressure': ['mean', 'min', 'max']
}

# รวบรวมข้อมูลเป็นรายวัน
X = feature_hours.groupby('date').agg(agg_funcs)
# ตั้งชื่อคอลัมน์ใหม่
X.columns = ['_'.join(col).strip() for col in X.columns.values]
X = X.reset_index()

# 4. รวมข้อมูลเข้าด้วยกัน
data = pd.merge(X, y, on='date')

# 5. แบ่งข้อมูล Train/Test (แบ่งตามลำดับเวลา)
# ใช้ 80% แรกเทรน, 20% หลังทดสอบ
split_idx = int(len(data) * 0.8)
X_data = data.drop(columns=['date', 'target_rain'])
y_data = data['target_rain']

X_train, X_test = X_data.iloc[:split_idx], X_data.iloc[split_idx:]
y_train, y_test = y_data.iloc[:split_idx], y_data.iloc[split_idx:]

# 6. สร้างและเทรนโมเดล
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. ทดสอบและแสดงผล
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# แสดงความสำคัญของแต่ละตัวแปร
importances = pd.Series(model.feature_importances_, index=X_train.columns)
print("\nTop 5 Important Factors:")
print(importances.sort_values(ascending=False).head())