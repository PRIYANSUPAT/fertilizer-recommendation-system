import streamlit as st
import pandas as pd
import joblib
import numpy as np

def show_fertilizer_recommendation():
    """Fertilizer recommendation tool for farmers"""
    
    st.markdown("### 🌾 Fertilizer Recommendation System")
    st.markdown("Get smart fertilizer suggestions based on your soil and crop details")
    st.markdown("---")
    
    # Load models
    try:
        model = joblib.load("fertilizer_model.joblib")
        le = joblib.load("fertilizer_label_encoder.joblib")
        scaler = joblib.load("fertilizer_scaler.joblib")
        feature_cols = joblib.load("fertilizer_feature_columns.joblib")
        
        numeric_cols = ["Temperature", "Moisture", "Rainfall", "PH",
                        "Nitrogen", "Phosphorous", "Potassium", "Carbon"]
        cat_cols = ["Soil", "Crop"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌡️ Environmental Conditions")
            temp = st.number_input("Temperature (°C)", value=30.0, key="fert_temp")
            moist = st.number_input("Moisture (%)", value=40.0, key="fert_moist")
            rain = st.number_input("Rainfall (mm)", value=50.0, key="fert_rain")
            ph = st.number_input("Soil pH", value=6.5, key="fert_ph")
        
        with col2:
            st.subheader("🧪 Soil Nutrients")
            n = st.number_input("Nitrogen (N)", value=50.0, key="fert_n")
            p = st.number_input("Phosphorous (P)", value=30.0, key="fert_p")
            k = st.number_input("Potassium (K)", value=20.0, key="fert_k")
            c = st.number_input("Carbon Content", value=0.5, key="fert_c")
        
        soil_options = ["Red Soil", "Sandy Soil", "Clayey Soil", "Loamy Soil", "Black Soil"]
        crop_options = ["Rice", "Sugarcane", "Chickpea", "Maize", "Tea", "Spinach", "Groundnut"]
        
        st.subheader("🪴 Soil & Crop Details")
        soil = st.selectbox("🌍 Select Soil Type", soil_options, key="fert_soil")
        crop = st.selectbox("🌱 Select Crop", crop_options, key="fert_crop")
        
        def nutrient_status(value, low, high):
            if value < low:
                return "🔻 Low"
            elif value > high:
                return "🔺 High"
            return "✔ Normal"
        
        def fertilizer_info(name):
            desc = {
                "Urea": "High-Nitrogen fertilizer used when N is low.",
                "DAP": "Phosphorous-rich fertilizer used when P is low.",
                "Muriate of Potash": "Potassium-rich fertilizer used when K is low.",
                "Lime": "Used to increase soil pH in acidic soils.",
                "Balanced NPK Fertilizer": "Provides a balanced mix of N, P, K.",
                "Organic Fertilizer": "Improves soil structure and carbon content.",
                "Water Retaining Fertilizer": "Useful in dry or sandy soils with low moisture."
            }
            return desc.get(name, "Helps improve soil nutrient balance.")
        
        if st.button("🚀 Get Recommendation", use_container_width=True, key="fert_btn"):
            sample = {
                "Temperature": temp, "Moisture": moist, "Rainfall": rain, "PH": ph,
                "Nitrogen": n, "Phosphorous": p, "Potassium": k, "Carbon": c,
                "Soil": soil, "Crop": crop
            }
            row = pd.DataFrame([sample])
            
            # Transform
            row_num = pd.DataFrame(scaler.transform(row[numeric_cols]), columns=numeric_cols)
            row_cat = pd.get_dummies(row[cat_cols], drop_first=False)
            row_final = pd.concat([row_num, row_cat], axis=1)
            
            # Fix missing cols
            for col in feature_cols:
                if col not in row_final.columns:
                    row_final[col] = 0
            
            row_final = row_final[feature_cols]
            
            # Prediction
            proba = model.predict_proba(row_final)[0]
            idx_sorted = np.argsort(proba)[::-1]
            top3_idx = idx_sorted[:3]
            top3_ferts = le.inverse_transform(top3_idx)
            top3_probs = proba[top3_idx]
            main_fert = top3_ferts[0]
            
            st.success(f"### 🌿 Recommended Fertilizer: **{main_fert}**")
            st.info(fertilizer_info(main_fert))
            
            st.markdown("#### ⭐ Top 3 Suggestions")
            for fert, prob in zip(top3_ferts, top3_probs):
                st.markdown(f"- **{fert}** — {prob*100:.2f}% confidence")
            
            st.markdown("#### 🧪 Nutrient Status")
            colN, colP, colK = st.columns(3)
            colN.metric("Nitrogen (N)", n, nutrient_status(n, 10, 80))
            colP.metric("Phosphorous (P)", p, nutrient_status(p, 10, 60))
            colK.metric("Potassium (K)", k, nutrient_status(k, 10, 60))
    
    except Exception as e:
        st.error(f"Error loading fertilizer recommendation model: {str(e)}")
        st.info("Please ensure all model files are present in the project directory.")
