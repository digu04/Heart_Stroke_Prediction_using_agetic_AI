from agents.report_agent import generate_pdf_report

# Dummy data (replace with real agent outputs later)
features = {
    "Age": 55,
    "Sex": "M",
    "RestingBP": 150,
    "Cholesterol": 250,
    "ExerciseAngina": "Y",
    "Oldpeak": 2.5
}

prediction = 1
risk = 82.7
reasoning = "Your elevated cholesterol and ST depression contribute..."
lifestyle = "1. Eat more fiber...\n2. Start walking..."

generate_pdf_report("heart_report.pdf", features, prediction, risk, reasoning, lifestyle)

print("PDF generated successfully!")
