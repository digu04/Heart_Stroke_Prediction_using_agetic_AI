# -----------------------------
# IMPORTS
# -----------------------------
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("heart.csv")

# -----------------------------
# TARGET
# -----------------------------
X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]

# -----------------------------
# ENCODING
# -----------------------------
X = pd.get_dummies(X, drop_first=True)

# Save feature structure
joblib.dump(X.columns.tolist(), "feature_columns.pkl")
print("Feature columns saved.")

# -----------------------------
# SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# FINAL LOCKED MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\nFinal Model Performance:")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))
print("ROC AUC  :", roc_auc_score(y_test, y_prob))

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "best_model.pkl")

print("\nProject Locked on Random Forest")