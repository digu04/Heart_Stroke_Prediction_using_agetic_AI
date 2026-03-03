import joblib
import pandas as pd

# -----------------------------
# LOAD LOCKED MODEL + FEATURES
# -----------------------------
model = joblib.load("best_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")


# -----------------------------
# CLEANING FUNCTIONS
# -----------------------------
def clean_fastingbs(value):
    try:
        return int(value)
    except:
        v = str(value).lower()
        if v in ["y", "yes", "true", "1", "high"]:
            return 1
        return 0


def clean_numeric(value, default=0):
    try:
        return float(value)
    except:
        return float(default)


# -----------------------------
# MAIN PREDICTION FUNCTION
# -----------------------------
def predict_heart_disease(input_data: dict):

    # Clean numeric fields
    cleaned_data = {
        "Age": clean_numeric(input_data.get("Age")),
        "RestingBP": clean_numeric(input_data.get("RestingBP")),
        "Cholesterol": clean_numeric(input_data.get("Cholesterol")),
        "MaxHR": clean_numeric(input_data.get("MaxHR")),
        "Oldpeak": clean_numeric(input_data.get("Oldpeak")),
        "FastingBS": clean_fastingbs(input_data.get("FastingBS")),

        "Sex": input_data.get("Sex"),
        "ChestPainType": input_data.get("ChestPainType"),
        "RestingECG": input_data.get("RestingECG"),
        "ExerciseAngina": input_data.get("ExerciseAngina"),
        "ST_Slope": input_data.get("ST_Slope"),
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([cleaned_data])

    # Apply same encoding used during training
    input_df = pd.get_dummies(input_df, drop_first=True)

    # Align with training feature structure
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    # Predict
    prediction = int(model.predict(input_df)[0])
    probability = model.predict_proba(input_df)[0][1]

    risk_percentage = round(probability * 100, 2)

    return {
        "prediction": prediction,
        "risk_percentage": risk_percentage,
        "input_used": cleaned_data
    }