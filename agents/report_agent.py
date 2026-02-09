# =====================================================
# report_agent.py — FINAL VERSION
# =====================================================

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from datetime import datetime


# OPTIONAL HEADER / BORDER FUNCTIONS
def draw_header(canvas, doc):
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(55, 805, "Heart Disease Risk Assessment Report")


def draw_double_border(canvas, doc):
    canvas.setLineWidth(2)
    canvas.rect(40, 40, 515, 790)


def generate_pdf_report(output_path, features, prediction, risk, reasoning, lifestyle, user):
    """
    user = { "name": "...", "email": "...", "mobile": "..." }
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=90,
        bottomMargin=40,
        leftMargin=55,
        rightMargin=55,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=10,
        alignment=TA_LEFT,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        fontName="Helvetica",
        fontSize=12,
        leading=18,
    )

    story = []

    # ----------------------------------------------------------
    # USER DETAILS AT TOP OF REPORT
    # ----------------------------------------------------------
    user_name = user.get("name", "N/A") if user else "N/A"
    user_email = user.get("email", "N/A") if user else "N/A"
    user_mobile = user.get("mobile", "N/A") if user else "N/A"

    user_info = f"""
        <b>Name:</b> {user_name}<br/>
        <b>Email:</b> {user_email}<br/>
        <b>Mobile:</b> {user_mobile}<br/>
    """

    story.append(Paragraph(user_info, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>__________________________________________________________</b>", body_style))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------------
    # PATIENT FEATURES TABLE
    # ----------------------------------------------------------
    story.append(Paragraph("📋 Patient Health Summary", title_style))
    story.append(Spacer(1, 10))

    table_data = [["Feature", "Value"]]
    for k, v in features.items():
        table_data.append([str(k), str(v)])

    table = Table(table_data, colWidths=[180, 260])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
    ]))

    story.append(table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>__________________________________________________________</b>", body_style))
    story.append(Spacer(1, 15))

    # ----------------------------------------------------------
    # PREDICTION
    # ----------------------------------------------------------
    story.append(Paragraph("❤️ Prediction & Risk Score", title_style))
    story.append(Spacer(1, 10))

    pred_text = f"""
        <b>Prediction:</b> {"High Risk ⚠️" if prediction == 1 else "Low Risk ✔️"}<br/>
        <b>Risk Probability:</b> {risk:.2f}%<br/>
    """
    story.append(Paragraph(pred_text, body_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>__________________________________________________________</b>", body_style))
    story.append(Spacer(1, 15))

    # ----------------------------------------------------------
    # MEDICAL REASONING
    # ----------------------------------------------------------
    story.append(Paragraph("🧠 Medical Interpretation", title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(reasoning.replace("\n", "<br/>"), body_style))
    story.append(Spacer(1, 15))

    # ----------------------------------------------------------
    # LIFESTYLE
    # ----------------------------------------------------------
    story.append(Paragraph("🥗 Lifestyle Recommendations", title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(lifestyle.replace("\n", "<br/>"), body_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>__________________________________________________________</b>", body_style))
    story.append(Spacer(1, 15))

    # ----------------------------------------------------------
    # DISCLAIMER
    # ----------------------------------------------------------
    disclaimer = """
        <b>Disclaimer:</b><br/>
        This AI-generated report is for educational purposes only.<br/>
        Always consult a licensed doctor for clinical decisions.
    """
    story.append(Paragraph(disclaimer, body_style))
    story.append(Spacer(1, 20))

    doc.build(
        story,
        onFirstPage=lambda canvas, doc: (draw_header(canvas, doc), draw_double_border(canvas, doc)),
        onLaterPages=lambda canvas, doc: (draw_header(canvas, doc), draw_double_border(canvas, doc)),
    )
