import joblib
import pandas as pd
import os

# Load your model files (using your uploaded paths)
model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")


def clean_fastingbs(value):
    """
    Helper Agent sometimes outputs: "Fine", "Normal", "High", "Yes", etc.
    This function safely converts ANY such text into 0 or 1.
    """
    try:
        return int(value)  # if it's already 0 or 1
    except:
        v = str(value).lower()
        if v in ["y", "yes", "true", "1", "high"]:
            return 1
        return 0


def clean_exercise_angina(value):
    v = str(value).upper()
    return "Y" if v in ["Y", "YES", "1", "TRUE"] else "N"


def clean_numeric(value, default=0):
    """Prevent crash if helper agent outputs text like 'Fine'."""
    try:
        return float(value)
    except:
        return float(default)


def predict_heart_disease(input_data: dict):
    """
    Takes user input dict and returns:
    - prediction (0/1)
    - risk_percentage (float)
    """

    # Base all-zero input structure
    input_dict = {col: 0 for col in columns}

    # ----- NUMERIC VALUES (with cleaning) -----
    input_dict['Age'] = clean_numeric(input_data['Age'])
    input_dict['RestingBP'] = clean_numeric(input_data['RestingBP'])
    input_dict['Cholesterol'] = clean_numeric(input_data['Cholesterol'])
    input_dict['MaxHR'] = clean_numeric(input_data['MaxHR'])
    input_dict['Oldpeak'] = clean_numeric(input_data['Oldpeak'])
    input_dict['FastingBS'] = clean_fastingbs(input_data['FastingBS'])

    # ----- SEX -----
    input_dict['Sex_M'] = 1 if str(input_data['Sex']).upper() == 'M' else 0

    # ----- CHEST PAIN -----
    cp = str(input_data['ChestPainType']).upper()
    if cp in ['ATA', 'NAP', 'TA']:
        input_dict[f"ChestPainType_{cp}"] = 1

    # ----- RESTING ECG -----
    ecg = str(input_data['RestingECG'])
    if ecg in ['Normal', 'ST']:
        input_dict[f"RestingECG_{ecg}"] = 1

    # ----- EXERCISE ANGINA -----
    ang = clean_exercise_angina(input_data['ExerciseAngina'])
    input_dict['ExerciseAngina_Y'] = 1 if ang == "Y" else 0

    # ----- ST SLOPE -----
    slope = str(input_data['ST_Slope'])
    if slope in ['Flat', 'Up']:
        input_dict[f"ST_Slope_{slope}"] = 1

    # Convert to DataFrame
    df = pd.DataFrame([input_dict])

    # Scale
    df_scaled = scaler.transform(df)

    # Prediction
    prediction = int(model.predict(df_scaled)[0])

    # Risk percentage
    risk_percentage = round(model.predict_proba(df_scaled)[0][1] * 100, 2)

    return {
        "prediction": prediction,
        "risk_percentage": risk_percentage,
        "input_used": input_dict
    }
