<<<<<<< HEAD
🌾 Fertilizer Recommendation System

A Machine Learning–Powered Smart Farming Tool

This project predicts the most suitable fertilizer for a crop based on soil properties, nutrient levels, and environmental conditions.
It uses a RandomForest model enhanced with SMOTE to handle class imbalance and provides Top-3 fertilizer suggestions with confidence scores.

🚀 Features
✅ Machine Learning Model

Algorithm: RandomForestClassifier

Handles imbalanced classes using SMOTE

Supports multi-class classification

One-hot encoding for categorical features

Numerical feature scaling using StandardScaler

Probability-based predictions (predict_proba())

✅ Smart Recommendations

🎯 Best fertilizer suggestion

⭐ Top 3 fertilizers with confidence %

🧪 Nutrient status check (N, P, K)

💡 Rule-based expert hints

📊 Feature importance chart

✅ Modern Streamlit UI

Beautiful layout

Two-column input system

Clear result cards

Sidebar information

Professional look for college projects & GitHub

🧪 Input Parameters
Feature	Description
Temperature	Soil temperature (°C)
Moisture	Soil water percentage
Rainfall	Rainfall (mm)
pH	Soil acidity level
Nitrogen	N value
Phosphorous	P value
Potassium	K value
Carbon	Organic carbon
Soil Type	Loamy, Sandy, Red, Clayey, etc.
Crop	Rice, Wheat, Maize, Sugarcane, etc.
📈 Output

The system provides:

🌿 Recommended fertilizer

⭐ Top-3 fertilizer suggestions

🧪 Nutrient status: Low / Normal / High

💡 Expert advice based on soil conditions

📊 Feature importance visualization

📊 Dataset Details

Your dataset contains:

10 input columns

Multiple fertilizer classes (Balanced NPK, Urea, DAP, Lime, MOP, Organic Fertilizer, etc.)

Imbalanced classes → handled using SMOTE

The training pipeline includes cleaning, scaling, one-hot encoding, splitting, SMOTE oversampling, training, evaluating, and saving the final model.

🛠️ Model Training Pipeline

Load dataset

Drop unused/leakage columns

Label-encode fertilizer output

One-hot encode soil & crop

Scale numeric features

Train-test split (stratified)

Apply SMOTE

Train RandomForest

Evaluate model

Retrain on full balanced data

Save using joblib:

fertilizer_model.joblib

fertilizer_scaler.joblib

fertilizer_label_encoder.joblib

fertilizer_feature_columns.joblib

⚙️ Installation

Run these commands:

pip install -r requirements.txt


Typical requirements:

pandas
numpy
scikit-learn
imbalanced-learn
streamlit
joblib

▶️ Running the App
streamlit run app.py


This will open the fertilizer recommendation dashboard in your browser.

📁 Folder Structure
ml project/
│
├── app.py
├── dataset.ipynb
├── fertilizer_model.joblib
├── fertilizer_scaler.joblib
├── fertilizer_label_encoder.joblib
├── fertilizer_feature_columns.joblib
├── fertilizer_recommendation_dataset.csv
└── README.md  ← (this file)



=======
# fertilizer-recommendation-system
>>>>>>> f11c4bddbd3c95185da3ce3b0f29a0ceb00201f3
# fertilizer-recommendation-system
