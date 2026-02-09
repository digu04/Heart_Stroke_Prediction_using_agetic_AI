from agents.prediction_agent import predict_heart_disease

# Sample input to test the prediction agent
sample_input = {
    "Age": 52,
    "Sex": "M",
    "ChestPainType": "TA",
    "RestingBP": 140,
    "Cholesterol": 260,
    "FastingBS": 1,
    "RestingECG": "ST",
    "MaxHR": 130,
    "ExerciseAngina": "Y",
    "Oldpeak": 2.3,
    "ST_Slope": "Flat"
}

# Run the prediction
result = predict_heart_disease(sample_input)

# Print output
print("Prediction result:")
print(result)
