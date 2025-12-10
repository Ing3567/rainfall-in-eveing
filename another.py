import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('open-meteo-13.74N100.50E7m (1).csv', skiprows=3)
df['is_raining'] = df['rain (mm)'] > 0

# Create a figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Overlapping KDE (Density) Plot
sns.kdeplot(data=df, x='relative_humidity_2m (%)', hue='is_raining', fill=True, common_norm=False, palette={False: "orange", True: "blue"}, ax=axes[0])
axes[0].set_title('Humidity Distribution: Rain vs No Rain')
axes[0].set_xlabel('Humidity (%)')

# Plot 2: Probability of Rain by Humidity Interval
# Bin humidity into 10% buckets
df['humidity_bin'] = pd.cut(df['relative_humidity_2m (%)'], bins=range(0, 101, 10))
prob_rain = df.groupby('humidity_bin')['is_raining'].mean() * 100

prob_rain.plot(kind='bar', color='skyblue', ax=axes[1])
axes[1].set_title('Probability of Rain at Different Humidity Levels')
axes[1].set_xlabel('Humidity Range')
axes[1].set_ylabel('Chance of Rain (%)')
axes[1].set_ylim(0, 100)

plt.tight_layout()
plt.savefig('humidity_overlap_analysis.png')

# Print specific stats to include in the answer
high_humidity_data = df[df['relative_humidity_2m (%)'] >= 90]
rain_at_high_humid = high_humidity_data['is_raining'].mean()
print(f"Chance of rain when humidity is >= 90%: {rain_at_high_humid*100:.2f}%")


# Load data
df = pd.read_csv('weather_2021-2025.csv', skiprows=3)

# 1. Prepare Data
# Create binary target
df['is_raining'] = (df['rain (mm)'] > 0).astype(int)

# Select features
features = ['temperature_2m (°C)', 'relative_humidity_2m (%)', 
            'wind_speed_10m (km/h)', 'surface_pressure (hPa)']
X = df[features]
y = df['is_raining']

# Handle any missing values (though previous checks said none, good practice)
X = X.fillna(X.mean())

# 2. Feature Importance (Random Forest)
# This handles non-linear relationships well
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X, y)

importances = pd.DataFrame({
    'Feature': features,
    'Importance': rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("--- Feature Importance (Random Forest) ---")
print(importances)

# 3. Correlation with Binary Target (Linear relationship)
corr_with_rain = df[features + ['is_raining']].corr()['is_raining'].drop('is_raining')
print("\n--- Correlation with Rain Presence (Linear) ---")
print(corr_with_rain)

# 4. Probability Plots for other variables (Pressure & Wind)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Helper to plot probability
def plot_prob(feature, ax, bins=10):
    # Create bins
    df['bin'] = pd.qcut(df[feature], q=bins, duplicates='drop')
    # Calculate mean of is_raining in each bin
    prob = df.groupby('bin')['is_raining'].mean() * 100
    # Get the mid-point of bins for plotting x-axis
    mid_points = [i.mid for i in prob.index]
    
    sns.lineplot(x=mid_points, y=prob.values, marker='o', ax=ax, color='red')
    ax.set_title(f"Rain Probability vs {feature}")
    ax.set_ylabel("Probability of Rain (%)")
    ax.set_xlabel(feature)
    ax.grid(True)

# Plot for Pressure
plot_prob('surface_pressure (hPa)', axes[0])

# Plot for Wind Speed
plot_prob('wind_speed_10m (km/h)', axes[1])

# Plot for Temperature
plot_prob('temperature_2m (°C)', axes[2])

plt.tight_layout()
plt.savefig('rain_drivers_analysis.png')