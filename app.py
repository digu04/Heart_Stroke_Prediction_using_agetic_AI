# app.py

import joblib
import pandas as pd
from flask import Flask, request, render_template

# -----------------------------
# INITIALIZE APP
# -----------------------------
app = Flask(__name__)

# -----------------------------
# LOAD LOCKED MODEL
# -----------------------------
model = joblib.load("best_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")


# -----------------------------
# CLEANING FUNCTIONS
# -----------------------------
def clean_numeric(value, default=0):
    try:
        return float(value)
    except:
        return float(default)


def clean_fastingbs(value):
    try:
        return int(value)
    except:
        v = str(value).lower()
        if v in ["yes", "y", "true", "1", "high"]:
            return 1
        return 0


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():

    data = request.form

    # -----------------------------
    # CLEAN INPUT DATA
    # -----------------------------
    cleaned_data = {
        "Age": clean_numeric(data.get("Age")),
        "RestingBP": clean_numeric(data.get("RestingBP")),
        "Cholesterol": clean_numeric(data.get("Cholesterol")),
        "MaxHR": clean_numeric(data.get("MaxHR")),
        "Oldpeak": clean_numeric(data.get("Oldpeak")),
        "FastingBS": clean_fastingbs(data.get("FastingBS")),

        "Sex": data.get("Sex"),
        "ChestPainType": data.get("ChestPainType"),
        "RestingECG": data.get("RestingECG"),
        "ExerciseAngina": data.get("ExerciseAngina"),
        "ST_Slope": data.get("ST_Slope"),
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([cleaned_data])

    # Apply same encoding as training
    input_df = pd.get_dummies(input_df, drop_first=True)

    # Align with training feature structure
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    # -----------------------------
    # PREDICTION
    # -----------------------------
    prediction = int(model.predict(input_df)[0])
    probability = round(model.predict_proba(input_df)[0][1] * 100, 2)

    # -----------------------------
    # RISK CATEGORY
    # -----------------------------
    if probability < 30:
        risk_level = "Low Risk 🌱"
    elif probability < 60:
        risk_level = "Moderate Risk ⚠"
    else:
        risk_level = "High Risk 🚨"

    result = "Heart Disease Likely" if prediction == 1 else "Heart Disease Unlikely"

    return render_template(
        'index.html',
        prediction_result=result,
        probability=probability,
        risk_level=risk_level
    )


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)