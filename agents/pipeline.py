# =====================================================
# pipeline.py — FINAL VERSION (User Info Included)
# =====================================================

from agents.helper_agent import helper_agent_process
from agents.prediction_agent import predict_heart_disease
from agents.reasoning_agent import generate_medical_reasoning
from agents.lifestyle_agent import lifestyle_recommendations
from agents.feedback_agent import feedback_agent_process
from agents.report_agent import generate_pdf_report
from agents.history_manager import save_history

REPORT_PATH = "generated_report.pdf"


def process_free_text_input(user_text: str):
    return helper_agent_process(user_text)


def process_form_input(form_data: dict):
    try:
        return {
            "Age": int(form_data["Age"]),
            "Sex": form_data["Sex"],
            "ChestPainType": form_data["ChestPainType"],
            "RestingBP": int(form_data["RestingBP"]),
            "Cholesterol": int(form_data["Cholesterol"]),
            "FastingBS": int(form_data["FastingBS"]),
            "RestingECG": form_data["RestingECG"],
            "MaxHR": int(form_data["MaxHR"]),
            "ExerciseAngina": form_data["ExerciseAngina"],
            "Oldpeak": float(form_data["Oldpeak"]),
            "ST_Slope": form_data["ST_Slope"],
        }
    except:
        return {"error": "Invalid form input"}


def run_full_pipeline(features: dict, user_info=None):
    """
    Full AI pipeline that now includes USER INFO (name, email, mobile)
    """

    # 1. ML model (KNN)
    result = predict_heart_disease(features)
    prediction = result["prediction"]
    risk = result["risk_percentage"]

    # 2. Medical reasoning
    reasoning = generate_medical_reasoning(prediction, risk, features)

    # 3. Lifestyle recommendations
    lifestyle = lifestyle_recommendations(features, risk)

    # 4. Build context
    context = {
        "prediction": prediction,
        "risk": risk,
        "features": features,
        "reasoning": reasoning,
        "lifestyle": lifestyle,
        "user_info": user_info,
    }

    # 5. Generate PDF report
    generate_pdf_report(
        output_path=REPORT_PATH,
        features=features,
        prediction=prediction,
        risk=risk,
        reasoning=reasoning,
        lifestyle=lifestyle,
        user=user_info,      # ⬅ FIX: pass user
    )

    # 6. Save history
    save_history(context, REPORT_PATH)

    return context, REPORT_PATH


def run_feedback_agent(user_question: str, context: dict):
    return feedback_agent_process(user_question, context)
