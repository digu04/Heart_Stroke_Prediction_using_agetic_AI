# Heart Disease Risk Prediction Using Random Forest and Agentic AI

## Abstract

Cardiovascular disease remains one of the most serious public health problems worldwide, and early risk identification can support timely awareness and preventive action. This research presents a machine-learning-based heart disease risk prediction system enhanced with an agentic AI workflow. The proposed system uses clinical patient attributes such as age, sex, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, ECG results, maximum heart rate, exercise-induced angina, old peak value, and ST slope to estimate the probability of heart disease. A Random Forest classifier was selected as the final prediction model because of its strong classification performance, robustness to nonlinear feature relationships, and ability to reduce overfitting through ensemble learning. The system also integrates multiple AI agents for input processing, medical reasoning, lifestyle recommendation, feedback handling, report generation, and history management. Experimental results show that the Random Forest model achieved an accuracy of 89.67%, precision of 88.79%, recall of 93.14%, F1-score of 90.91%, and ROC AUC of 93.50%. The final application provides risk prediction, explainable reasoning, personalized lifestyle guidance, downloadable PDF reports, and a follow-up chat interface. This work demonstrates how machine learning and agentic AI can be combined to create an interactive health-risk support system.

**Keywords:** Heart disease prediction, Random Forest, machine learning, agentic AI, healthcare analytics, Streamlit, clinical decision support

## 1. Introduction

Heart disease is a major cause of illness and mortality across the world. Many patients remain unaware of their risk until symptoms become severe, which makes early screening and preventive guidance important. Traditional medical assessment depends on clinical examination, diagnostic tests, and physician expertise. Although these methods are essential, machine learning can support early-stage risk estimation by identifying patterns in patient data.

The purpose of this project is to build an intelligent heart disease risk prediction system that does more than output a simple class label. The system predicts whether a user has low or high heart disease risk, calculates a risk probability, explains the possible reasons behind the result, recommends lifestyle improvements, stores prediction history, and generates a structured PDF report. To achieve this, the project combines a Random Forest machine learning model with an agentic AI pipeline.

The earlier version of the research content was based on K-Nearest Neighbors (KNN). However, the implemented and final locked model in this project is Random Forest. Therefore, this paper focuses on the Random Forest classifier and its role in the final system.

## 2. Problem Statement

The main problem addressed in this research is the need for an accessible and intelligent system that can estimate heart disease risk using basic clinical inputs and provide meaningful post-prediction support. A basic prediction model alone may not be enough for users, because they also need explanations, next-step suggestions, and a record of previous results.

The objectives of this project are:

1. To preprocess structured heart disease data for machine learning.
2. To train and evaluate a Random Forest classifier for heart disease prediction.
3. To generate a risk probability along with the predicted class.
4. To provide AI-generated medical reasoning in simple language.
5. To recommend lifestyle improvements based on patient features.
6. To provide a chat-based feedback interface for follow-up questions.
7. To generate a PDF report and maintain user prediction history.

## 3. Dataset Description

The project uses the Heart Failure Prediction dataset, which contains 918 patient records and 12 columns. Out of these, 11 columns are input features and one column is the target variable, `HeartDisease`. The target value is binary, where `1` indicates the presence of heart disease and `0` indicates a normal case.

The dataset contains the following input features:

| Feature | Description |
|---|---|
| Age | Age of the patient in years |
| Sex | Gender of the patient |
| ChestPainType | Type of chest pain |
| RestingBP | Resting blood pressure |
| Cholesterol | Serum cholesterol |
| FastingBS | Fasting blood sugar status |
| RestingECG | Resting electrocardiogram result |
| MaxHR | Maximum heart rate achieved |
| ExerciseAngina | Exercise-induced angina |
| Oldpeak | ST depression value |
| ST_Slope | Slope of peak exercise ST segment |

The dataset used in this project contains 508 heart disease cases and 410 normal cases. Since the target classes are not perfectly balanced, the Random Forest model was trained with balanced class weights to reduce bias toward the majority class.

## 4. Proposed System

The proposed system is an agentic AI-based heart disease risk prediction application. It consists of a frontend interface, a trained machine learning model, and several supporting AI agents. The frontend is built using Streamlit, allowing users to register, enter clinical values, view prediction results, ask follow-up questions, download reports, and check prediction history.

The system workflow is as follows:

1. The user enters patient information through a form or free-text input.
2. The helper agent converts free-text input into structured feature values when needed.
3. The prediction agent sends the processed features to the Random Forest model.
4. The model predicts the class and calculates the risk probability.
5. The reasoning agent explains the prediction in simple medical language.
6. The lifestyle agent generates diet, exercise, stress, and sleep suggestions.
7. The report agent creates a PDF report containing user details, health features, prediction, reasoning, and lifestyle advice.
8. The history manager stores previous prediction records.
9. The feedback agent handles follow-up chat questions using the prediction context.

## 5. Methodology

### 5.1 Data Preprocessing

The input dataset contains both numerical and categorical attributes. Numerical fields such as age, resting blood pressure, cholesterol, maximum heart rate, fasting blood sugar, and old peak are cleaned and converted into numeric values. Categorical fields such as sex, chest pain type, resting ECG, exercise angina, and ST slope are converted into machine-readable form using one-hot encoding.

The target column, `HeartDisease`, is separated from the input features. The feature structure created during training is saved using Joblib so that future user inputs can be aligned with the exact same columns before prediction.

### 5.2 Train-Test Split

The dataset is divided into training and testing sets using an 80:20 split. Stratified sampling is used so that both classes remain proportionally represented in the training and testing data. A fixed random state is used to make the experiment reproducible.

### 5.3 Random Forest Classifier

Random Forest is an ensemble learning algorithm that builds multiple decision trees and combines their outputs to make a final prediction. In classification tasks, the final class is usually selected through majority voting across trees. This makes Random Forest more stable than a single decision tree and helps reduce overfitting.

In this project, the final model uses:

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of trees | 300 |
| Random state | 42 |
| Class weight | Balanced |
| Train-test split | 80:20 |
| Encoding method | One-hot encoding |
| Model storage | Joblib pickle file |

Random Forest was chosen because it handles nonlinear relationships well, works effectively with mixed feature types after encoding, and provides strong predictive performance for tabular healthcare data.

## 6. Implementation Details

The project is implemented in Python. The model training process is handled in `train_models.py`, where the dataset is loaded, preprocessed, split, trained, evaluated, and saved. The trained model is stored as `best_model.pkl`, and the feature column structure is stored as `feature_columns.pkl`.

The main application interface is built in `streamlit_app.py`. It includes registration, input collection, prediction display, chat, report download, and history viewing. The backend logic is divided into agent modules inside the `agents` folder.

The major technologies used are:

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Web framework support | Flask |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn |
| Model persistence | Joblib |
| AI reasoning and recommendation | Groq API, Llama models, Ollama |
| PDF generation | ReportLab |
| PDF/text processing | PyPDF2, pdf2image, EasyOCR |
| Data storage | JSON |

## 7. Agentic AI Architecture

The project uses an agentic design, where different agents perform different responsibilities. This improves modularity and makes the system easier to maintain.

| Agent | Responsibility |
|---|---|
| Helper Agent | Converts free-text patient input into structured JSON |
| Prediction Agent | Loads the Random Forest model and predicts risk |
| Reasoning Agent | Generates simple medical interpretation of the result |
| Lifestyle Agent | Provides diet, exercise, stress, and sleep recommendations |
| Feedback Agent | Answers follow-up questions through the chat interface |
| Report Agent | Generates a downloadable PDF report |
| History Manager | Saves and loads previous prediction records |
| User Manager | Handles user registration and user details |

The AI-generated content is designed as supportive guidance only. The system does not provide a medical diagnosis and should not replace professional medical consultation.

## 8. Results and Evaluation

The trained Random Forest model was evaluated using accuracy, precision, recall, F1-score, and ROC AUC. The results are shown below:

| Metric | Random Forest Result |
|---|---:|
| Cross-validation F1-score | 87.92% |
| Accuracy | 89.67% |
| Precision | 88.79% |
| Recall | 93.14% |
| F1-score | 90.91% |
| ROC AUC | 93.50% |

The Random Forest model performed better than the KNN model in the project comparison. KNN achieved 69.57% accuracy and 72.55% F1-score, while Random Forest achieved 89.67% accuracy and 90.91% F1-score. This improvement shows that Random Forest is more suitable for this project’s tabular clinical dataset.

The high recall value of 93.14% is especially useful in a healthcare risk-screening context because it indicates that the model is effective at identifying positive heart disease cases. However, the system should still be treated as a decision-support tool and not as a final medical diagnostic system.

## 9. Discussion

The results show that Random Forest is a strong model for heart disease risk prediction using structured patient features. The ensemble nature of the model helps it capture complex relationships between clinical attributes. Compared with KNN, Random Forest provides better performance because it is less sensitive to feature scale and can model nonlinear interactions more effectively.

The agentic AI layer adds practical value to the prediction system. Instead of showing only “high risk” or “low risk,” the application explains the result, gives lifestyle guidance, supports follow-up chat, and creates a PDF report. This makes the project more user-friendly and more suitable for presentation as a complete healthcare support application.

At the same time, the project has limitations. The dataset size is moderate, and the system has not been clinically validated on real hospital deployment data. AI-generated reasoning may be helpful for explanation, but it must remain safe, non-diagnostic, and clearly advisory. Future versions should include stronger validation, feature importance visualization, model explainability using SHAP or similar tools, and improved privacy controls.

## 10. Conclusion

This research presents a heart disease risk prediction system using Random Forest and agentic AI. The Random Forest classifier achieved strong performance with 89.67% accuracy, 90.91% F1-score, and 93.50% ROC AUC. The application goes beyond basic prediction by integrating agents for structured input processing, medical reasoning, lifestyle recommendations, feedback chat, PDF reporting, and history management.

The final system demonstrates how machine learning can be combined with interactive AI agents to create a more useful healthcare support tool. While the system cannot replace doctors or clinical diagnosis, it can support awareness, early risk estimation, and personalized preventive guidance.

## 11. Future Scope

Future improvements may include:

1. Adding explainable AI methods such as SHAP for feature-level interpretation.
2. Deploying the application on a secure cloud platform.
3. Adding database storage instead of JSON files for better scalability.
4. Improving authentication and user privacy.
5. Adding doctor/admin dashboards.
6. Validating the model on larger and more diverse clinical datasets.
7. Adding multilingual support for better accessibility.
8. Improving the chat interface with conversational memory and safer medical guardrails.

## References

1. Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5-32. https://doi.org/10.1023/A:1010933404324
2. Scikit-learn Developers. RandomForestClassifier documentation. https://sklearn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
3. Fedesoriano. Heart Failure Prediction Dataset. Kaggle. https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction/data
4. UCI Machine Learning Repository. Heart Disease datasets index. https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/

