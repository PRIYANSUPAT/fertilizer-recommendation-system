
import streamlit as st
import pandas as pd
import joblib
import numpy as np


st.set_page_config(
    page_title="Fertilizer Recommendation System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


model = joblib.load("fertilizer_model.joblib")
le = joblib.load("fertilizer_label_encoder.joblib")
scaler = joblib.load("fertilizer_scaler.joblib")
feature_cols = joblib.load("fertilizer_feature_columns.joblib")

numeric_cols = ["Temperature", "Moisture", "Rainfall", "PH",
                "Nitrogen", "Phosphorous", "Potassium", "Carbon"]
cat_cols = ["Soil", "Crop"]


st.sidebar.title("ℹ️ About This App")
st.sidebar.markdown(
    """
    This app uses a **RandomForest + SMOTE** trained model  
    to recommend suitable **fertilizers** based on:
    
    - 🌡️ Temperature  
    - 💧 Moisture & Rainfall  
    - 🧪 N, P, K, pH, Carbon  
    - 🌍 Soil Type  
    - 🌱 Crop  

    You also get:
    - ⭐ Top 3 fertilizer suggestions  
    - 🧪 NPK status (Low / Normal / High)  
    - 📊 Model feature importance  
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Developer Notes:**")
st.sidebar.markdown(
    """
    - Model: RandomForestClassifier  
    - Handling Imbalance: SMOTE  
    - UI: Streamlit  
    """
)


st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center; color: #2E7D32;'>
        🌾 Fertilizer Recommendation System
    </h1>
    <p style='text-align: center; font-size:18px;'>
        Smart decision support for farmers – powered by Machine Learning
    </p>
    <hr>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Environmental Conditions")
    temp = st.number_input("Temperature (°C)", value=30.0)
    moist = st.number_input("Moisture (%)", value=40.0)
    rain = st.number_input("Rainfall (mm)", value=50.0)
    ph = st.number_input("Soil pH", value=6.5)

with col2:
    st.subheader("🧪 Soil Nutrients")
    n = st.number_input("Nitrogen (N)", value=50.0)
    p = st.number_input("Phosphorous (P)", value=30.0)
    k = st.number_input("Potassium (K)", value=20.0)
    c = st.number_input("Carbon Content", value=0.5)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='color:#1B5E20;'>🪴 Soil and Crop Selection</h3>",
    unsafe_allow_html=True,
)

soil_options = ["Red Soil", "Sandy Soil", "Clayey Soil", "Loamy Soil", "Black Soil"]
crop_options = ["Rice", "Sugarcane", "Chickpea", "Maize", "Tea", "Spinach", "Groundnut"]

soil = st.selectbox("🌍 Soil Type", soil_options)
crop = st.selectbox("🌱 Crop", crop_options)

st.markdown("<hr>", unsafe_allow_html=True)


def nutrient_status(value, low, high):
    if value < low:
        return "🔻 Low"
    elif value > high:
        return "🔺 High"
    return "✔ Normal"


def rule_based_hints(n, p, k, ph, moisture, soil):
    hints = []
    if n < 10:
        hints.append("Nitrogen is **very low** → Nitrogen-rich fertilizer like **Urea / NPK high N** can help.")
    if p < 10:
        hints.append("Phosphorous is **very low** → Consider **DAP or P-rich fertilizer**.")
    if k < 10:
        hints.append("Potassium is **very low** → **Muriate of Potash** or K-rich sources may be needed.")
    if ph < 5.5:
        hints.append("Soil is **acidic** → **Lime** is often used to increase pH.")
    if ph > 8.0:
        hints.append("Soil is **alkaline** → Gypsum or organic matter may help.")
    if moisture < 20 or soil == "Sandy Soil":
        hints.append("Soil seems **dry / low water retention** → **Water retaining fertilizer or organic matter** is useful.")
    if not hints:
        hints.append("NPK and pH are within a normal range. Balanced fertilizers might be suitable.")
    return hints


if st.button("🚀 Recommend Fertilizer", use_container_width=True):

    
    sample = {
        "Temperature": temp, "Moisture": moist, "Rainfall": rain, "PH": ph,
        "Nitrogen": n, "Phosphorous": p, "Potassium": k, "Carbon": c,
        "Soil": soil, "Crop": crop
    }
    row = pd.DataFrame([sample])

    
    row_num = pd.DataFrame(scaler.transform(row[numeric_cols]), columns=numeric_cols)

    
    row_cat = pd.get_dummies(row[cat_cols].astype(str), drop_first=False)

    
    row_final = pd.concat([row_num, row_cat], axis=1)

    
    for col in feature_cols:
        if col not in row_final.columns:
            row_final[col] = 0

    row_final = row_final[feature_cols]

    
    proba = model.predict_proba(row_final)[0]
    idx_sorted = np.argsort(proba)[::-1]

    top3_idx = idx_sorted[:3]
    top3_ferts = le.inverse_transform(top3_idx)
    top3_probs = proba[top3_idx]

    main_fert = top3_ferts[0]

    
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:12px; background-color:#E8F5E9; margin-bottom:15px;">
            <h2 style="color:#1B5E20; margin:0;">
                🌿 Recommended Fertilizer: <b>{main_fert}</b>
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    
    st.markdown("### ⭐ Top 3 Fertilizer Suggestions")
    for fert, prob in zip(top3_ferts, top3_probs):
        st.markdown(
            f"""
            <div style="padding:10px; border-left:5px solid #66BB6A; background-color:black; border-radius:6px; margin-bottom:8px;">
                <b>{fert}</b> — {prob*100:.2f}% confidence
            </div>
            """,
            unsafe_allow_html=True,
        )

    
    st.markdown("### 🧪 Nutrient Status Summary")
    colN, colP, colK = st.columns(3)
    colN.metric("Nitrogen (N)", n, nutrient_status(n, 10, 80))
    colP.metric("Phosphorous (P)", p, nutrient_status(p, 10, 60))
    colK.metric("Potassium (K)", k, nutrient_status(k, 10, 60))

    
    st.markdown("### 💡 Smart Hints Based on Your Input")
    for hint in rule_based_hints(n, p, k, ph, moist, soil):
        st.write("•", hint)

    
    with st.expander("📊 Model Insights (Feature Importance)", expanded=False):
        try:
            importances = model.feature_importances_
            fi_df = pd.DataFrame({
                "feature": feature_cols,
                "importance": importances
            }).sort_values("importance", ascending=False)

            st.write("Top 15 important features used by the model:")
            top_fi = fi_df.head(15).set_index("feature")
            st.bar_chart(top_fi)
        except Exception as e:
            st.write("Could not compute feature importances:", e)
