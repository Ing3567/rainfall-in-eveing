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
Argument,Description,Example
--file,Path to the CSV data file (Default: data/weather_2021-2025.csv),--file data/my_weather.csv
--mode,"Text Analysis Mode: View summary stats or feature importance on the terminal.  Options: summary, rain_drivers, rain_comparison",--mode rain_drivers
--plot,"Visualization Mode: Generate specific plots.  Options: timeseries, heatmap, boxplot, seasonality, drivers, evening_scatter",--plot heatmap
--col,"Select a specific column for analysis (e.g., Temperature, Pressure).","--col ""pressure_msl (hPa)"""
--year,Filter analysis for a specific year (useful for evening trends).,--year 2024

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
