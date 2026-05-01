"""
Generate IEEE-style two-column research paper PDF
Matching the format of Heart_Disease_RP_Format_Final (144).pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    FrameBreak, PageBreak, KeepTogether
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib import colors

BASE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE, "paper_figures")
OUT = os.path.join(BASE, "research_paper_random_forest.pdf")

W, H = A4
MARGIN = 0.6 * inch
COL_GAP = 0.3 * inch
COL_W = (W - 2 * MARGIN - COL_GAP) / 2

# ── Styles ──────────────────────────────────────────────
styles = getSampleStyleSheet()

s_title = ParagraphStyle('PTitle', parent=styles['Title'],
    fontName='Times-Bold', fontSize=16, leading=20, alignment=TA_CENTER,
    spaceAfter=6)

s_author = ParagraphStyle('PAuthor', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=10, leading=13, alignment=TA_CENTER,
    spaceAfter=2)

s_affil = ParagraphStyle('PAffil', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=9, leading=11, alignment=TA_CENTER,
    spaceAfter=2)

s_email = ParagraphStyle('PEmail', parent=styles['Normal'],
    fontName='Courier', fontSize=8, leading=10, alignment=TA_CENTER,
    spaceAfter=4)

s_abstract_head = ParagraphStyle('PAbsHead', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=10, leading=12, alignment=TA_LEFT,
    spaceAfter=3, spaceBefore=6)

s_abstract = ParagraphStyle('PAbs', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=9, leading=11, alignment=TA_JUSTIFY,
    spaceAfter=4)

s_keywords = ParagraphStyle('PKw', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=9, leading=11, alignment=TA_JUSTIFY,
    spaceAfter=8)

s_section = ParagraphStyle('PSection', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_CENTER,
    spaceBefore=10, spaceAfter=4)

s_subsection = ParagraphStyle('PSubsec', parent=styles['Normal'],
    fontName='Times-Bold', fontSize=10, leading=12, alignment=TA_LEFT,
    spaceBefore=8, spaceAfter=3)

s_body = ParagraphStyle('PBody', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=9, leading=11.5, alignment=TA_JUSTIFY,
    spaceAfter=4)

s_caption = ParagraphStyle('PCaption', parent=styles['Normal'],
    fontName='Times-Italic', fontSize=8, leading=10, alignment=TA_CENTER,
    spaceAfter=6, spaceBefore=2)

s_ref = ParagraphStyle('PRef', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=8, leading=10, alignment=TA_JUSTIFY,
    spaceAfter=2, leftIndent=14, firstLineIndent=-14)

s_header = ParagraphStyle('PHdr', parent=styles['Normal'],
    fontName='Times-Roman', fontSize=7, leading=9, alignment=TA_CENTER)

# ── Header/Footer ──────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 7)
    hdr = "Heart Disease Risk Prediction Using Random Forest and Agentic AI"
    canvas.drawCentredString(W/2, H - 0.35*inch, hdr)
    canvas.drawCentredString(W/2, 0.35*inch, f"Page {doc.page}")
    canvas.restoreState()

# ── Document Setup ─────────────────────────────────────
class TwoColumnDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4,
            leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=0.7*inch, bottomMargin=0.6*inch, **kw)

        # Full-width frame for title page top
        full_frame = Frame(MARGIN, 0.6*inch, W-2*MARGIN, H-1.3*inch, id='full')

        # Two-column frames
        left = Frame(MARGIN, 0.6*inch, COL_W, H-1.3*inch, id='left')
        right = Frame(MARGIN+COL_W+COL_GAP, 0.6*inch, COL_W, H-1.3*inch, id='right')

        self.addPageTemplates([
            PageTemplate(id='FullPage', frames=[full_frame], onPage=header_footer),
            PageTemplate(id='TwoCol', frames=[left, right], onPage=header_footer),
        ])

# ── Table helper ───────────────────────────────────────
def make_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#E0E0E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#F5F5F5')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t

def img(name, w=None):
    p = os.path.join(FIG_DIR, name)
    if not os.path.exists(p):
        return Spacer(1, 12)
    if w is None:
        w = COL_W - 10
    return Image(p, width=w, height=w*0.65)

# ── Build content ──────────────────────────────────────
story = []

# TITLE
story.append(Paragraph("Heart Disease Risk Prediction Using Random Forest and Agentic AI", s_title))
story.append(Spacer(1, 6))

# AUTHORS
authors = [
    ("Digvijay Salunkhe", "digvijay.salunkhe@gcek.edu.in"),
    ("Maaz Parvez Ansari", "maaz.ansari@gcek.edu.in"),
    ("Vishwajit Gholave", "vishwajit.gholave@gcek.edu.in"),
    ("Shubham Vasant Kambale", "shubham.kambale@gcek.edu.in"),
]
for name, email in authors:
    story.append(Paragraph(f"<b>{name}</b>", s_author))
    story.append(Paragraph("Department of Information Technology, Government College of Engineering, Karad, India", s_affil))
    story.append(Paragraph(email, s_email))

story.append(Spacer(1, 4))
story.append(Paragraph("<b>Dr. S. A. Thorat</b> (Guide)", s_author))
story.append(Paragraph("Department of Information Technology, Government College of Engineering, Karad, India", s_affil))
story.append(Spacer(1, 10))

# ABSTRACT
story.append(Paragraph("ABSTRACT", s_abstract_head))
abstract_text = (
    "Cardiovascular disease remains one of the most serious public health problems worldwide, "
    "and early risk identification can support timely awareness and preventive action. This research "
    "presents a machine-learning-based heart disease risk prediction system enhanced with an agentic AI "
    "workflow. The proposed system uses clinical patient attributes such as age, sex, chest pain type, "
    "resting blood pressure, cholesterol, fasting blood sugar, ECG results, maximum heart rate, "
    "exercise-induced angina, old peak value, and ST slope to estimate the probability of heart disease. "
    "A Random Forest classifier was selected as the final prediction model because of its strong "
    "classification performance, robustness to nonlinear feature relationships, and ability to reduce "
    "overfitting through ensemble learning. The system also integrates multiple AI agents for input "
    "processing, medical reasoning, lifestyle recommendation, feedback handling, report generation, and "
    "history management. Experimental results show that the Random Forest model achieved an accuracy of "
    "89.67%, precision of 88.79%, recall of 93.14%, F1-score of 90.91%, and ROC AUC of 93.50%. The "
    "final application provides risk prediction, explainable reasoning, personalized lifestyle guidance, "
    "downloadable PDF reports, and a follow-up chat interface. This work demonstrates how machine learning "
    "and agentic AI can be combined to create an interactive health-risk support system."
)
story.append(Paragraph(abstract_text, s_abstract))

story.append(Paragraph(
    "<b>Keywords:</b> Heart disease prediction, Random Forest, machine learning, agentic AI, "
    "healthcare analytics, Streamlit, clinical decision support", s_keywords))

# Switch to two-column layout
story.append(PageBreak())

# ── 1. INTRODUCTION ────────────────────────────────────
story.append(Paragraph("1. INTRODUCTION", s_section))
story.append(Paragraph(
    "Heart disease is a major cause of illness and mortality across the world. Many patients remain "
    "unaware of their risk until symptoms become severe, which makes early screening and preventive "
    "guidance important. Traditional medical assessment depends on clinical examination, diagnostic "
    "tests, and physician expertise. Although these methods are essential, machine learning can support "
    "early-stage risk estimation by identifying patterns in patient data.", s_body))
story.append(Paragraph(
    "The purpose of this project is to build an intelligent heart disease risk prediction system that "
    "does more than output a simple class label. The system predicts whether a user has low or high "
    "heart disease risk, calculates a risk probability, explains the possible reasons behind the result, "
    "recommends lifestyle improvements, stores prediction history, and generates a structured PDF report. "
    "To achieve this, the project combines a Random Forest machine learning model with an agentic AI pipeline.", s_body))
story.append(Paragraph(
    "The earlier version of the research content was based on K-Nearest Neighbors (KNN). However, the "
    "implemented and final locked model in this project is Random Forest. Therefore, this paper focuses "
    "on the Random Forest classifier and its role in the final system.", s_body))

# ── 2. PROBLEM STATEMENT ──────────────────────────────
story.append(Paragraph("2. PROBLEM STATEMENT", s_section))
story.append(Paragraph(
    "The main problem addressed in this research is the need for an accessible and intelligent system "
    "that can estimate heart disease risk using basic clinical inputs and provide meaningful "
    "post-prediction support. A basic prediction model alone may not be enough for users, because they "
    "also need explanations, next-step suggestions, and a record of previous results.", s_body))
story.append(Paragraph("The objectives of this project are:", s_body))
objectives = [
    "To preprocess structured heart disease data for machine learning.",
    "To train and evaluate a Random Forest classifier for heart disease prediction.",
    "To generate a risk probability along with the predicted class.",
    "To provide AI-generated medical reasoning in simple language.",
    "To recommend lifestyle improvements based on patient features.",
    "To provide a chat-based feedback interface for follow-up questions.",
    "To generate a PDF report and maintain user prediction history.",
]
for i, obj in enumerate(objectives, 1):
    story.append(Paragraph(f"({i}) {obj}", s_body))

# ── 3. DATASET DESCRIPTION ────────────────────────────
story.append(Paragraph("3. DATASET DESCRIPTION", s_section))
story.append(Paragraph(
    "The project uses the Heart Failure Prediction dataset, which contains 918 patient records and 12 "
    "columns. Out of these, 11 columns are input features and one column is the target variable, "
    "HeartDisease. The target value is binary, where 1 indicates the presence of heart disease and 0 "
    "indicates a normal case.", s_body))

# Table I: Dataset Features
story.append(Paragraph("Table I: Clinical Features Used for Prediction", s_caption))
feat_data = [
    ['Feature', 'Description'],
    ['Age', 'Age of the patient in years'],
    ['Sex', 'Gender of the patient'],
    ['ChestPainType', 'Type of chest pain'],
    ['RestingBP', 'Resting blood pressure'],
    ['Cholesterol', 'Serum cholesterol'],
    ['FastingBS', 'Fasting blood sugar status'],
    ['RestingECG', 'Resting ECG result'],
    ['MaxHR', 'Maximum heart rate achieved'],
    ['ExerciseAngina', 'Exercise-induced angina'],
    ['Oldpeak', 'ST depression value'],
    ['ST_Slope', 'Slope of peak exercise ST segment'],
]
story.append(make_table(feat_data, col_widths=[COL_W*0.4, COL_W*0.55]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "The dataset contains 508 heart disease cases and 410 normal cases. Since the target classes are "
    "not perfectly balanced, the Random Forest model was trained with balanced class weights to reduce "
    "bias toward the majority class.", s_body))

# Figure: Heart Disease Distribution
story.append(KeepTogether([
    img("heart_disease_distribution.png", COL_W-20),
    Paragraph("Figure 1: Heart Disease Distribution (%)", s_caption),
]))

# Figure: Categorical distributions
story.append(FrameBreak())
story.append(KeepTogether([
    img("categorical_distributions.png", COL_W-10),
    Paragraph("Figure 2: Distribution of Categorical Features", s_caption),
]))

# Figure: Numerical distributions
story.append(KeepTogether([
    img("numerical_distributions.png", COL_W-10),
    Paragraph("Figure 3: Distribution of Numerical Features", s_caption),
]))

# Figure: Correlation Heatmap
story.append(KeepTogether([
    img("correlation_heatmap.png", COL_W-10),
    Paragraph("Figure 4: Correlation Heatmap of Numerical Features", s_caption),
]))

# ── 4. PROPOSED SYSTEM ────────────────────────────────
story.append(Paragraph("4. PROPOSED SYSTEM", s_section))
story.append(Paragraph(
    "The proposed system is an agentic AI-based heart disease risk prediction application. It consists "
    "of a frontend interface, a trained machine learning model, and several supporting AI agents. The "
    "frontend is built using Streamlit, allowing users to register, enter clinical values, view "
    "prediction results, ask follow-up questions, download reports, and check prediction history.", s_body))
story.append(Paragraph("The system workflow is as follows:", s_body))
workflow = [
    "The user enters patient information through a form or free-text input.",
    "The helper agent converts free-text input into structured feature values when needed.",
    "The prediction agent sends the processed features to the Random Forest model.",
    "The model predicts the class and calculates the risk probability.",
    "The reasoning agent explains the prediction in simple medical language.",
    "The lifestyle agent generates diet, exercise, stress, and sleep suggestions.",
    "The report agent creates a PDF report containing user details, health features, prediction, reasoning, and lifestyle advice.",
    "The history manager stores previous prediction records.",
    "The feedback agent handles follow-up chat questions using the prediction context.",
]
for i, w in enumerate(workflow, 1):
    story.append(Paragraph(f"({i}) {w}", s_body))

# ── 5. METHODOLOGY ────────────────────────────────────
story.append(Paragraph("5. METHODOLOGY", s_section))

story.append(Paragraph("5.1 Data Preprocessing", s_subsection))
story.append(Paragraph(
    "The input dataset contains both numerical and categorical attributes. Numerical fields such as "
    "age, resting blood pressure, cholesterol, maximum heart rate, fasting blood sugar, and old peak "
    "are cleaned and converted into numeric values. Categorical fields such as sex, chest pain type, "
    "resting ECG, exercise angina, and ST slope are converted into machine-readable form using one-hot "
    "encoding. The target column, HeartDisease, is separated from the input features. The feature "
    "structure created during training is saved using Joblib so that future user inputs can be aligned "
    "with the exact same columns before prediction.", s_body))

story.append(Paragraph("5.2 Train-Test Split", s_subsection))
story.append(Paragraph(
    "The dataset is divided into training and testing sets using an 80:20 split. Stratified sampling "
    "is used so that both classes remain proportionally represented in the training and testing data. "
    "A fixed random state is used to make the experiment reproducible.", s_body))

story.append(Paragraph("5.3 Random Forest Classifier", s_subsection))
story.append(Paragraph(
    "Random Forest is an ensemble learning algorithm that builds multiple decision trees and combines "
    "their outputs to make a final prediction. In classification tasks, the final class is usually "
    "selected through majority voting across trees. This makes Random Forest more stable than a single "
    "decision tree and helps reduce overfitting.", s_body))

# Table II: Model Parameters
story.append(Paragraph("Table II: Random Forest Model Parameters", s_caption))
param_data = [
    ['Parameter', 'Value'],
    ['Algorithm', 'Random Forest Classifier'],
    ['Number of trees', '300'],
    ['Random state', '42'],
    ['Class weight', 'Balanced'],
    ['Train-test split', '80:20'],
    ['Encoding method', 'One-hot encoding'],
    ['Model storage', 'Joblib pickle file'],
]
story.append(make_table(param_data, col_widths=[COL_W*0.45, COL_W*0.45]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "Random Forest was chosen because it handles nonlinear relationships well, works effectively with "
    "mixed feature types after encoding, and provides strong predictive performance for tabular "
    "healthcare data.", s_body))

# Feature importance figure
story.append(KeepTogether([
    img("feature_importance.png", COL_W-10),
    Paragraph("Figure 5: Random Forest Feature Importance", s_caption),
]))

# ── 6. IMPLEMENTATION DETAILS ─────────────────────────
story.append(Paragraph("6. IMPLEMENTATION DETAILS", s_section))
story.append(Paragraph(
    "The project is implemented in Python. The model training process is handled in train_models.py, "
    "where the dataset is loaded, preprocessed, split, trained, evaluated, and saved. The trained model "
    "is stored as best_model.pkl, and the feature column structure is stored as feature_columns.pkl. "
    "The main application interface is built in streamlit_app.py.", s_body))

# Table III: Technologies
story.append(Paragraph("Table III: Technologies Used", s_caption))
tech_data = [
    ['Component', 'Technology'],
    ['Programming language', 'Python'],
    ['User interface', 'Streamlit'],
    ['Web framework support', 'Flask'],
    ['Data processing', 'Pandas, NumPy'],
    ['Machine learning', 'Scikit-learn'],
    ['Model persistence', 'Joblib'],
    ['AI reasoning', 'Groq API, Llama, Ollama'],
    ['PDF generation', 'ReportLab'],
    ['Data storage', 'JSON'],
]
story.append(make_table(tech_data, col_widths=[COL_W*0.45, COL_W*0.45]))

# ── 7. AGENTIC AI ARCHITECTURE ────────────────────────
story.append(Paragraph("7. AGENTIC AI ARCHITECTURE", s_section))
story.append(Paragraph(
    "The project uses an agentic design, where different agents perform different responsibilities. "
    "This improves modularity and makes the system easier to maintain. The AI-generated content is "
    "designed as supportive guidance only.", s_body))

# Table IV: Agent Responsibilities
story.append(Paragraph("Table IV: Agent Responsibilities", s_caption))
agent_data = [
    ['Agent', 'Responsibility'],
    ['Helper Agent', 'Converts free-text input into structured JSON'],
    ['Prediction Agent', 'Loads Random Forest model and predicts risk'],
    ['Reasoning Agent', 'Generates medical interpretation of result'],
    ['Lifestyle Agent', 'Provides diet, exercise, stress, sleep recommendations'],
    ['Feedback Agent', 'Answers follow-up questions via chat'],
    ['Report Agent', 'Generates a downloadable PDF report'],
    ['History Manager', 'Saves and loads previous prediction records'],
    ['User Manager', 'Handles user registration and details'],
]
story.append(make_table(agent_data, col_widths=[COL_W*0.35, COL_W*0.60]))

# ── 8. RESULTS AND EVALUATION ─────────────────────────
story.append(Paragraph("8. RESULTS AND EVALUATION", s_section))
story.append(Paragraph(
    "The trained Random Forest model was evaluated using accuracy, precision, recall, F1-score, and "
    "ROC AUC. The results are shown below:", s_body))

# Table V: Results
story.append(Paragraph("Table V: Random Forest Model Performance Metrics", s_caption))
result_data = [
    ['Metric', 'Random Forest Result'],
    ['Cross-validation F1-score', '87.92%'],
    ['Accuracy', '89.67%'],
    ['Precision', '88.79%'],
    ['Recall', '93.14%'],
    ['F1-score', '90.91%'],
    ['ROC AUC', '93.50%'],
]
story.append(make_table(result_data, col_widths=[COL_W*0.50, COL_W*0.40]))
story.append(Spacer(1, 6))

# Table VI: Model Comparison
story.append(Paragraph("Table VI: Model Comparison Results", s_caption))
comp_data = [
    ['Model', 'CV F1', 'Accuracy', 'Precision', 'Recall', 'F1', 'AUC'],
    ['Logistic Reg.', '86.82%', '88.59%', '87.16%', '93.14%', '90.05%', '93.09%'],
    ['KNN', '73.27%', '69.57%', '72.55%', '72.55%', '72.55%', '74.86%'],
    ['Random Forest', '87.92%', '89.67%', '88.79%', '93.14%', '90.91%', '93.50%'],
    ['Extra Trees', '87.35%', '89.13%', '87.96%', '93.14%', '90.48%', '94.48%'],
    ['Gradient Boost', '87.15%', '87.50%', '89.11%', '88.24%', '88.67%', '93.19%'],
    ['XGBoost', '86.35%', '85.87%', '87.25%', '87.25%', '87.25%', '92.19%'],
    ['LightGBM', '87.06%', '85.87%', '86.54%', '88.24%', '87.38%', '92.34%'],
]
story.append(make_table(comp_data, col_widths=[COL_W*0.22, COL_W*0.13, COL_W*0.13, COL_W*0.13, COL_W*0.13, COL_W*0.10, COL_W*0.10]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "The Random Forest model performed better than the KNN model in the project comparison. KNN "
    "achieved 69.57% accuracy and 72.55% F1-score, while Random Forest achieved 89.67% accuracy and "
    "90.91% F1-score. This improvement shows that Random Forest is more suitable for this project's "
    "tabular clinical dataset.", s_body))

story.append(Paragraph(
    "The high recall value of 93.14% is especially useful in a healthcare risk-screening context "
    "because it indicates that the model is effective at identifying positive heart disease cases. "
    "However, the system should still be treated as a decision-support tool and not as a final medical "
    "diagnostic system.", s_body))

# Figures: Model Comparison & Confusion Matrix
story.append(KeepTogether([
    img("model_comparison.png", COL_W-10),
    Paragraph("Figure 6: Model Performance Comparison", s_caption),
]))

story.append(KeepTogether([
    img("confusion_matrix.png", COL_W-20),
    Paragraph("Figure 7: Confusion Matrix — Random Forest Model", s_caption),
]))

# ── 9. DISCUSSION ─────────────────────────────────────
story.append(Paragraph("9. DISCUSSION", s_section))
story.append(Paragraph(
    "The results show that Random Forest is a strong model for heart disease risk prediction using "
    "structured patient features. The ensemble nature of the model helps it capture complex "
    "relationships between clinical attributes. Compared with KNN, Random Forest provides better "
    "performance because it is less sensitive to feature scale and can model nonlinear interactions "
    "more effectively.", s_body))
story.append(Paragraph(
    "The agentic AI layer adds practical value to the prediction system. Instead of showing only "
    "'high risk' or 'low risk,' the application explains the result, gives lifestyle guidance, "
    "supports follow-up chat, and creates a PDF report. This makes the project more user-friendly "
    "and more suitable for presentation as a complete healthcare support application.", s_body))
story.append(Paragraph(
    "At the same time, the project has limitations. The dataset size is moderate, and the system has "
    "not been clinically validated on real hospital deployment data. AI-generated reasoning may be "
    "helpful for explanation, but it must remain safe, non-diagnostic, and clearly advisory. Future "
    "versions should include stronger validation, feature importance visualization, model "
    "explainability using SHAP or similar tools, and improved privacy controls.", s_body))

# ── 10. CONCLUSION ────────────────────────────────────
story.append(Paragraph("10. CONCLUSION", s_section))
story.append(Paragraph(
    "This research presents a heart disease risk prediction system using Random Forest and agentic AI. "
    "The Random Forest classifier achieved strong performance with 89.67% accuracy, 90.91% F1-score, "
    "and 93.50% ROC AUC. The application goes beyond basic prediction by integrating agents for "
    "structured input processing, medical reasoning, lifestyle recommendations, feedback chat, PDF "
    "reporting, and history management.", s_body))
story.append(Paragraph(
    "The final system demonstrates how machine learning can be combined with interactive AI agents to "
    "create a more useful healthcare support tool. While the system cannot replace doctors or clinical "
    "diagnosis, it can support awareness, early risk estimation, and personalized preventive guidance.", s_body))

# ── 11. FUTURE SCOPE ──────────────────────────────────
story.append(Paragraph("11. FUTURE SCOPE", s_section))
future = [
    "Adding explainable AI methods such as SHAP for feature-level interpretation.",
    "Deploying the application on a secure cloud platform.",
    "Adding database storage instead of JSON files for better scalability.",
    "Improving authentication and user privacy.",
    "Adding doctor/admin dashboards.",
    "Validating the model on larger and more diverse clinical datasets.",
    "Adding multilingual support for better accessibility.",
    "Improving the chat interface with conversational memory and safer medical guardrails.",
]
for i, f in enumerate(future, 1):
    story.append(Paragraph(f"({i}) {f}", s_body))

# ── REFERENCES ─────────────────────────────────────────
story.append(Paragraph("REFERENCES", s_section))
refs = [
    '[1] Breiman, L. (2001). Random Forests. <i>Machine Learning</i>, 45, 5-32.',
    '[2] Scikit-learn Developers. RandomForestClassifier documentation. https://sklearn.org',
    '[3] Fedesoriano. Heart Failure Prediction Dataset. Kaggle. https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction/data',
    '[4] UCI Machine Learning Repository. Heart Disease datasets. https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/',
]
for r in refs:
    story.append(Paragraph(r, s_ref))

# ── BUILD PDF ──────────────────────────────────────────
doc = TwoColumnDoc(OUT)
doc.build(story)
print(f"\nPDF generated successfully: {OUT}")
