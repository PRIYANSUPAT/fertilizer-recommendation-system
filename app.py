import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Fertilizer Recommendation",
    page_icon="🌱",
    layout="wide",
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #111111 0%, #222222 100%);
        color: white;
    }
    .big-title {
        text-align: center;
        color: #00E676;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #cccccc;
        font-size: 18px;
        margin-top: 5px;
        margin-bottom: 25px;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff15;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    .black-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #000000;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        margin-bottom: 15px;
        border: 1px solid #00E676;
    }
    .black-small-card {
        padding: 12px;
        border-radius: 10px;
        background-color: #000000;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        border-left: 4px solid #00E676;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- TITLE ----------
st.markdown("<h1 class='big-title'>🌾 Fertilizer Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Smart suggestions based on your soil and crop details</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- LOAD MODEL ----------
model = joblib.load("fertilizer_model.joblib")
le = joblib.load("fertilizer_label_encoder.joblib")
scaler = joblib.load("fertilizer_scaler.joblib")
feature_cols = joblib.load("fertilizer_feature_columns.joblib")

numeric_cols = ["Temperature", "Moisture", "Rainfall", "PH",
                "Nitrogen", "Phosphorous", "Potassium", "Carbon"]
cat_cols = ["Soil", "Crop"]

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🧮 Prediction", "📊 Model Info"])

# ---------- PREDICTION TAB ----------
with tab1:

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

    soil_options = ["Red Soil", "Sandy Soil", "Clayey Soil", "Loamy Soil", "Black Soil"]
    crop_options = ["Rice", "Sugarcane", "Chickpea", "Maize", "Tea", "Spinach", "Groundnut"]

    st.subheader("🪴 Soil & Crop Details")
    soil = st.selectbox("🌍 Select Soil Type", soil_options)
    crop = st.selectbox("🌱 Select Crop", crop_options)

    # ---- nutrient status helper ----
    def nutrient_status(value, low, high):
        if value < low:
            return "🔻 Low"
        elif value > high:
            return "🔺 High"
        return "✔ Normal"

    # ---- fertilizer info ----
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

    # ---------- BUTTON ----------
    if st.button("🚀 Recommend Fertilizer", use_container_width=True):

        sample = {
            "Temperature": temp, "Moisture": moist, "Rainfall": rain, "PH": ph,
            "Nitrogen": n, "Phosphorous": p, "Potassium": k, "Carbon": c,
            "Soil": soil, "Crop": crop
        }
        row = pd.DataFrame([sample])

        # transform
        row_num = pd.DataFrame(scaler.transform(row[numeric_cols]), columns=numeric_cols)
        row_cat = pd.get_dummies(row[cat_cols], drop_first=False)

        row_final = pd.concat([row_num, row_cat], axis=1)

        # fix missing cols
        for col in feature_cols:
            if col not in row_final.columns:
                row_final[col] = 0

        row_final = row_final[feature_cols]

        # prediction
        proba = model.predict_proba(row_final)[0]
        idx_sorted = np.argsort(proba)[::-1]
        top3_idx = idx_sorted[:3]
        top3_ferts = le.inverse_transform(top3_idx)
        top3_probs = proba[top3_idx]
        main_fert = top3_ferts[0]

        # ---------- BLACK MAIN CARD ----------
        st.markdown(
            f"""
            <div class="black-card">
                <h2>🌿 Recommended Fertilizer: <b>{main_fert}</b></h2>
                <p>{fertilizer_info(main_fert)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------- BLACK TOP-3 SUGGESTIONS ----------
        st.markdown("### ⭐ Top 3 Fertilizer Suggestions")
        for fert, prob in zip(top3_ferts, top3_probs):
            st.markdown(
                f"""
                <div class="black-small-card">
                    <b>{fert}</b> — {prob*100:.2f}% confidence
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---------- NUTRIENT STATUS ----------
        st.markdown("### 🧪 Nutrient Status")
        colN, colP, colK = st.columns(3)
        colN.metric("Nitrogen (N)", n, nutrient_status(n, 10, 80))
        colP.metric("Phosphorous (P)", p, nutrient_status(p, 10, 60))
        colK.metric("Potassium (K)", k, nutrient_status(k, 10, 60))

# ---------- MODEL INFO TAB ----------
with tab2:
    st.subheader("📊 Model Information")
    st.write("- Algorithm: RandomForestClassifier")
    st.write("- Handling Imbalance: SMOTE")
    st.write("- Output: Multi-class Fertilizer Recommendation")
    st.write("- Shows Top-3 Suggestions with confidence")

    # ---- Feature importance ----
    try:
        importances = model.feature_importances_
        fi_df = pd.DataFrame({
            "feature": feature_cols,
            "importance": importances
        }).sort_values("importance", ascending=False).head(15)
        fi_df = fi_df.set_index("feature")
        st.bar_chart(fi_df)
    except:
        st.write("Feature importance unavailable.")

