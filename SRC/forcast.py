import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve

filename = 'data/weather_2021-2025.csv'
print(f"Loading data from {filename}...")

try:
    df = pd.read_csv(filename, skiprows=3)
except:
    df = pd.read_csv(filename)

df['time'] = pd.to_datetime(df['time'])
df = df.sort_values('time').reset_index(drop=True)


df['hour'] = df['time'].dt.hour
df['month'] = df['time'].dt.month
df['rain_current'] = df['rain (mm)']
df['pressure'] = df['pressure_msl (hPa)']
df['temp'] = df['temperature_2m (°C)']
df['humidity'] = df['relative_humidity_2m (%)']
df['wind'] = df['wind_speed_10m (km/h)']

df['rain_next_hour'] = df['rain (mm)'].shift(-1)
df['target'] = (df['rain_next_hour'] > 0).astype(int)

df = df.dropna()

features = ['hour', 'month', 'rain_current', 'pressure', 'temp', 'humidity', 'wind']
split_idx = int(len(df) * 0.8)

X_train = df[features].iloc[:split_idx]
y_train = df['target'].iloc[:split_idx]

X_test = df[features].iloc[split_idx:]
y_test = df['target'].iloc[split_idx:]
time_test = df['time'].iloc[split_idx:]

print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n--- Accuracy Details ---")
print(classification_report(y_test, y_pred))


plt.figure(figsize=(10, 6))
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
sns.barplot(x=importances, y=importances.index, palette='viridis')
plt.title('Feature Importance')
plt.xlabel('Importance')
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 6))


y_test_np = y_test.values
time_test_np = time_test.values

rain_indices = np.where(y_test_np == 1)[0]

if len(rain_indices) > 0:
    start_idx = max(0, rain_indices[0] - 50)
    end_idx = min(len(y_test_np), start_idx + 200) 
    

    t_plot = time_test_np[start_idx:end_idx]
    actual_plot = y_test_np[start_idx:end_idx]
    prob_plot = y_prob[start_idx:end_idx]
    title_text = f'Forecast Comparison (Auto-detected Rain Event)'
else:
    t_plot = time_test_np[-200:]
    actual_plot = y_test_np[-200:]
    prob_plot = y_prob[-200:]
    title_text = 'Forecast Comparison (No Rain in Test Data)'


plt.fill_between(t_plot, 0, actual_plot, color='skyblue', alpha=0.4, label='Actual Rain')
plt.plot(t_plot, prob_plot, color='darkblue', linewidth=2, label='Forecast Probability')
plt.axhline(y=0.3, color='orange', linestyle='--', label='Threshold (30%)')

plt.title(title_text)
plt.ylabel('Probability / Rain Status')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


plt.figure(figsize=(18, 5))


plt.subplot(1, 3, 1)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.xticks([0.5, 1.5], ['No Rain', 'Rain'])
plt.yticks([0.5, 1.5], ['No Rain', 'Rain'])


fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
plt.subplot(1, 3, 2)
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], linestyle='--')
plt.title('ROC Curve')
plt.legend(loc="lower right")

precision, recall, _ = precision_recall_curve(y_test, y_prob)
plt.subplot(1, 3, 3)
plt.plot(recall, precision, color='green', lw=2)
plt.title('Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')

plt.tight_layout()
plt.show()