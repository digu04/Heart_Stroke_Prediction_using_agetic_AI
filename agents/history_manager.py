# =====================================================
# history_manager.py
# Handles saving, loading & clearing user prediction history
# =====================================================

import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

# -----------------------------------------------------
# Ensure file exists
# -----------------------------------------------------
def init_history():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)


# -----------------------------------------------------
# Save a new history entry
# -----------------------------------------------------
def save_history(context, pdf_path):
    """
    context contains:
        - prediction
        - risk
        - features
        - reasoning
        - lifestyle
    """

    init_history()

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),   # now includes seconds
        "prediction": context["prediction"],
        "risk": context["risk"],
        "features": context["features"],
        "reasoning": context["reasoning"],
        "lifestyle": context["lifestyle"],
        "pdf_path": pdf_path
    }

    # Load old history
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    # Append new entry
    data.append(new_entry)

    # Save updated list
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------------------
# Load entire history
# -----------------------------------------------------
def load_history():
    init_history()

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


# -----------------------------------------------------
# Clear all history
# -----------------------------------------------------
def clear_history():
    init_history()

    # Replace list with empty list
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
