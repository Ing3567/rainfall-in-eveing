## Capstone Project in CPE312
Time serire Analysis evening_rainfall



## SET UP


install libarary
run in powershell
python
```
pip install -r requirements.txt
```

## Main function
```
python ./main.py
```
คำสั่งเพิ่มเติม \n
--file ไฟล์ที่ใช้ \n
--mode ใช้ดูข้อมูลtextบนterminal \n
--plot เลือกที่ต้องแสดง \n
--col เลือกคอลัมที่สนใจ \n
--year เลือกปัที่สนใจ \n

ตัวอย่างคำสั่ง
```
python ./main.py --mode rain_drivers
```
```
python main.py --plot heatmap
```
```
python main.py --plot evening_trend --year 2024
```

## Classification
```
python ./forcast.py
```
แสดงผลเป็นกราฟ3ชุด
1.Feature Importance
2.Forecast vs Actual
3.Evaluation Metrics
