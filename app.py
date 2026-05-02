# =====================================================
# app.py — Flask REST API + Static SPA Server
# Heart Disease Prediction with Agentic AI
# =====================================================

import os
import re
import json
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory, send_file

from agents.pipeline import (
    process_free_text_input,
    run_full_pipeline,
    run_feedback_agent,
)
from agents.user_manager import register_user, load_users
from agents.history_manager import load_history, clear_history

# -----------------------------
# INITIALIZE APP
# -----------------------------
app = Flask(__name__, static_folder='static')

REPORT_PATH = "generated_report.pdf"

# -----------------------------
# SERVE SPA
# -----------------------------
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# =====================================================
# API: USER MANAGEMENT
# =====================================================

@app.route('/api/users', methods=['GET'])
def api_get_users():
    """Return list of registered users."""
    users = load_users()
    return jsonify({"users": users})


@app.route('/api/register', methods=['POST'])
def api_register():
    """Register a new user."""
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    mobile = data.get('mobile', '').strip()

    if not name or not email:
        return jsonify({"success": False, "error": "Name and email are required."})

    ok, result = register_user(name, email, mobile)

    if ok:
        return jsonify({"success": True, "user": result})
    else:
        return jsonify({"success": False, "error": result})


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login an existing user by email."""
    data = request.json
    email = data.get('email', '').strip().lower()

    users = load_users()
    for u in users:
        if u['email'].lower() == email:
            return jsonify({"success": True, "user": u})

    return jsonify({"success": False, "error": "User not found."})


# =====================================================
# API: PREDICTION
# =====================================================

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Run the full agentic AI prediction pipeline."""
    data = request.json
    features = data.get('features', {})
    user_info = data.get('user', None)

    try:
        ctx, pdf_path = run_full_pipeline(features, user_info=user_info)

        return jsonify({
            "success": True,
            "context": {
                "prediction": ctx["prediction"],
                "risk": ctx["risk"],
                "features": ctx["features"],
                "reasoning": ctx["reasoning"],
                "lifestyle": ctx["lifestyle"],
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/predict-text', methods=['POST'])
def api_predict_text():
    """Process free-text input through the helper agent, then run prediction."""
    data = request.json
    text = data.get('text', '')
    user_info = data.get('user', None)

    try:
        extracted = process_free_text_input(text)

        if "error" in extracted:
            return jsonify({"success": False, "error": extracted["error"]})

        ctx, pdf_path = run_full_pipeline(extracted, user_info=user_info)

        return jsonify({
            "success": True,
            "context": {
                "prediction": ctx["prediction"],
                "risk": ctx["risk"],
                "features": ctx["features"],
                "reasoning": ctx["reasoning"],
                "lifestyle": ctx["lifestyle"],
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# =====================================================
# API: PDF EXTRACTION
# =====================================================

def extract_medical_values_from_text(text):
    """Extract structured medical values from raw text."""
    def find(pattern, default=None):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else default

    return {
        "Age": int(find(r"Age[:\s]+(\d+)", 50)),
        "Sex": "M" if "male" in text.lower() else "F",
        "ChestPainType": "ATA" if "chest pain" in text.lower() else "NAP",
        "RestingBP": int(find(r"(?:BP|Blood Pressure)[:\s]+(\d+)", 120)),
        "Cholesterol": int(find(r"Cholesterol[:\s]+(\d+)", 200)),
        "FastingBS": "1" if "high sugar" in text.lower() else "0",
        "RestingECG": "Normal",
        "MaxHR": int(find(r"MaxHR[:\s]+(\d+)", 150)),
        "ExerciseAngina": "Y" if "angina" in text.lower() else "N",
        "Oldpeak": float(find(r"Oldpeak[:\s]+([\d.]+)", 0)),
        "ST_Slope": "Flat"
    }


@app.route('/api/extract-pdf', methods=['POST'])
def api_extract_pdf():
    """Extract medical data from an uploaded PDF."""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."})

    file = request.files['file']
    text = ""

    # Try text extraction with PyPDF2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    except Exception:
        pass

    # OCR fallback if text extraction fails
    if not text.strip():
        try:
            file.seek(0)
            from pdf2image import convert_from_bytes
            import easyocr

            images = convert_from_bytes(file.read(), dpi=300)
            reader_ocr = easyocr.Reader(['en'], gpu=False)

            for img in images:
                img_array = np.array(img)
                result = reader_ocr.readtext(img_array, detail=0)
                text += " ".join(result)
        except Exception as e:
            return jsonify({"success": False, "error": f"PDF extraction failed: {str(e)}"})

    if not text.strip():
        return jsonify({"success": False, "error": "Could not extract any text from PDF."})

    extracted_data = extract_medical_values_from_text(text)
    return jsonify({"success": True, "extracted": extracted_data, "raw_text": text[:500]})


# =====================================================
# API: CHAT
# =====================================================

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Send a follow-up question to the feedback agent."""
    data = request.json
    message = data.get('message', '')
    context = data.get('context', {})

    try:
        reply = run_feedback_agent(message, context)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


# =====================================================
# API: HISTORY
# =====================================================

@app.route('/api/history', methods=['GET'])
def api_history():
    """Return all prediction history."""
    history = load_history()
    return jsonify({"history": history})


@app.route('/api/history/clear', methods=['POST'])
def api_clear_history():
    """Clear all prediction history."""
    clear_history()
    return jsonify({"success": True})


# =====================================================
# API: REPORT DOWNLOAD
# =====================================================

@app.route('/api/report/download', methods=['GET'])
def api_download_report():
    """Download the latest generated PDF report."""
    if os.path.exists(REPORT_PATH):
        return send_file(REPORT_PATH, as_attachment=True, download_name="Heart_Report.pdf")
    return jsonify({"error": "No report available."}), 404


# =====================================================
# RUN APP
# =====================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)