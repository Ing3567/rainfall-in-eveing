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
คำสั่งเพิ่มเติม <br>
--file ไฟล์ที่ใช้ <br>
--mode ใช้ดูข้อมูลtextบนterminal <br>
--plot เลือกที่ต้องแสดง <br>
--col เลือกคอลัมที่สนใจ <br>
--year เลือกปัที่สนใจ <br>
 <br>
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
