"""
Generate charts for the research paper from the Heart.ipynb data
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

output_dir = os.path.join(os.path.dirname(__file__), "paper_figures")
os.makedirs(output_dir, exist_ok=True)

# Load dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "heart.csv"))

# 1. Correlation Heatmap (numerical features only)
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f',
            linewidths=0.5, square=True)
plt.title('Correlation Heatmap of Numerical Features', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: correlation_heatmap.png")

# 2. Heart Disease Distribution
plt.figure(figsize=(6, 4))
(df['HeartDisease'].value_counts(normalize=True) * 100).plot(
    kind="bar", color=["#66b3ff", "#ff9999"], edgecolor="black"
)
plt.title("Heart Disease Distribution (%)", fontsize=12, fontweight='bold')
plt.ylabel("Percentage (%)")
plt.xlabel("Heart Disease")
plt.xticks([0, 1], ['No (0)', 'Yes (1)'], rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "heart_disease_distribution.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: heart_disease_distribution.png")

# 3. Categorical feature distributions
categorical_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for i, col in enumerate(categorical_cols):
    sns.countplot(x=col, data=df, palette='Set2', ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=10, fontweight='bold')
    axes[i].set_xlabel('')
plt.suptitle('Distribution of Categorical Features', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "categorical_distributions.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: categorical_distributions.png")

# 4. Model Comparison Bar Chart
model_comp = pd.read_csv(os.path.join(os.path.dirname(__file__), "model_comparison.csv"), index_col=0)
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC']
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(model_comp.index))
width = 0.15
colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0']
for i, metric in enumerate(metrics):
    bars = ax.bar(x + i * width, model_comp[metric] * 100, width, label=metric, color=colors[i])
ax.set_xlabel('Model', fontsize=12)
ax.set_ylabel('Score (%)', fontsize=12)
ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 2)
ax.set_xticklabels(model_comp.index, rotation=30, ha='right', fontsize=9)
ax.legend(fontsize=9)
ax.set_ylim(60, 100)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "model_comparison.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: model_comparison.png")

# 5. Numerical feature distributions (histograms)
num_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for i, col in enumerate(num_cols):
    df[col].hist(bins=20, ax=axes[i], color='#42A5F5', edgecolor='black', alpha=0.7)
    axes[i].set_title(f'{col}', fontsize=10, fontweight='bold')
    axes[i].set_xlabel('')
plt.suptitle('Distribution of Numerical Features', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "numerical_distributions.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: numerical_distributions.png")

# 6. Feature Importance (Random Forest)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]
X_encoded = pd.get_dummies(X, drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42, stratify=y)

rf = RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced")
rf.fit(X_train, y_train)

importances = pd.Series(rf.feature_importances_, index=X_encoded.columns)
importances = importances.sort_values(ascending=True)

plt.figure(figsize=(8, 6))
importances.plot(kind='barh', color='#42A5F5', edgecolor='black')
plt.title('Random Forest Feature Importance', fontsize=14, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "feature_importance.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: feature_importance.png")

# 7. Confusion Matrix for Random Forest
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_pred = rf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Low Risk', 'High Risk'])
disp.plot(ax=ax, cmap='Blues', values_format='d')
plt.title('Confusion Matrix — Random Forest Model', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "confusion_matrix.png"), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: confusion_matrix.png")

print("\nAll charts generated successfully!")
