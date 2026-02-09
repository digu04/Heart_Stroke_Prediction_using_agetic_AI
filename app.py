# app.py

import joblib
import pandas as pd
from flask import Flask, request, render_template

# Initialize the Flask application
app = Flask(__name__)

# Load the saved model, scaler, and column names
model = joblib.load(r'E:\Heart_Stroke_Prediction\KNN_heart.pkl')
scaler = joblib.load(r'E:\Heart_Stroke_Prediction\scaler.pkl')
columns = joblib.load(r'E:\Heart_Stroke_Prediction\columns.pkl')

@app.route('/')
def home():
    """Renders the home page with the input form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the prediction request."""
    
    data = request.form

    # Create default dictionary with all model columns = 0
    user_input = {col: 0 for col in columns}

    # Numerical features
    user_input['Age'] = int(data['Age'])
    user_input['RestingBP'] = float(data['RestingBP'])
    user_input['Cholesterol'] = float(data['Cholesterol'])
    user_input['FastingBS'] = int(data['FastingBS'])
    user_input['MaxHR'] = int(data['MaxHR'])
    user_input['Oldpeak'] = float(data['Oldpeak'])

    # Sex
    user_input['Sex_M'] = 1 if data['Sex'] == 'M' else 0

    # Chest Pain Type (MODEL HAS ONLY ATA, NAP, TA)
    if data['ChestPainType'] in ['ATA', 'NAP', 'TA']:
        user_input[f"ChestPainType_{data['ChestPainType']}"] = 1

    # Resting ECG (MODEL HAS ONLY Normal, ST)
    if data['RestingECG'] in ['Normal', 'ST']:
        user_input[f"RestingECG_{data['RestingECG']}"] = 1

    # Exercise Angina
    user_input['ExerciseAngina_Y'] = 1 if data['ExerciseAngina'] == 'Y' else 0

    # ST Slope (MODEL HAS ONLY Flat, Up)
    if data['ST_Slope'] in ['Flat', 'Up']:
        user_input[f"ST_Slope_{data['ST_Slope']}"] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([user_input])

    # Scale
    input_scaled = scaler.transform(input_df)

    # Prediction (0 or 1)
    prediction = model.predict(input_scaled)[0]

    # Probability in percentage
    probability = model.predict_proba(input_scaled)[0][1] * 100
    probability = round(probability, 2)

    # Result text
    result = "High Risk of Heart Disease 🚨" if prediction == 1 else "Low Risk of Heart Disease 🌱"

    return render_template(
        'index.html',
        prediction_result=result,
        probability=probability
    )

if __name__ == '__main__':
    app.run(debug=True)
