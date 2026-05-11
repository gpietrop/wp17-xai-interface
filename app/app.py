from pathlib import Path
import sys

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.risk_model import (
    assign_risk_class,
    explain_prediction,
    get_model_rule,
    predict_probability,
)


DATA_PATH = ROOT / "data" / "mock" / "mock_patients.csv"
LOGO_PATH = ROOT / "app" / "assets" / "fh-early-logo.png"


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


st.set_page_config(
    page_title="FH-EARLY WP17 Prototype",
    layout="wide",
)

header_left, header_right = st.columns([1, 5])

with header_left:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=140)

with header_right:
    st.title("FH-EARLY WP17: Explainable Risk Profiling Prototype")
    st.caption(
        "Early clinician-facing prototype for testing the patient-level prediction and explanation workflow. "
        "The current data and predictions are synthetic placeholders."
    )

df = load_data()

with st.sidebar:
    st.header("Input")
    input_mode = st.radio(
        "Choose input mode",
        ["Select mock patient", "Enter new patient"],
    )

if input_mode == "Select mock patient":
    with st.sidebar:
        patient_id = st.selectbox("Select patient", df["patient_id"])

    patient = df.loc[df["patient_id"] == patient_id].iloc[0]

else:
    st.sidebar.subheader("New patient data")

    patient = pd.Series(
        {
            "patient_id": "NEW_PATIENT",
            "age": st.sidebar.number_input("Age", min_value=0, max_value=120, value=50),
            "sex": st.sidebar.selectbox("Sex", ["F", "M"]),
            "ldl_c": st.sidebar.number_input("LDL-C", min_value=0, value=190),
            "hdl_c": st.sidebar.number_input("HDL-C", min_value=0, value=50),
            "triglycerides": st.sidebar.number_input(
                "Triglycerides",
                min_value=0,
                value=120,
            ),
            "lipoprotein_a": st.sidebar.number_input(
                "Lipoprotein(a)",
                min_value=0,
                value=30,
            ),
            "family_history": int(st.sidebar.checkbox("Family history")),
            "has_pathogenic_variant": int(
                st.sidebar.checkbox("Pathogenic variant present")
            ),
            "previous_cvd_event": int(st.sidebar.checkbox("Previous CVD event")),
            "risk_label": "Not available",
        }
    )

probability = predict_probability(patient)
risk_class = assign_risk_class(probability)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Predicted risk class", risk_class)

with col2:
    st.metric("Risk probability", f"{probability:.0%}")

with col3:
    st.metric("Patient age", int(patient["age"]))

st.divider()

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Patient profile")

    patient_table = patient.astype(str).to_frame(name="value")
    st.dataframe(patient_table, use_container_width=True)

with right:
    st.subheader("Explanation")

    for reason in explain_prediction(patient):
        st.write(f"- {reason}")

    st.subheader("Interpretable rule")
    st.code(get_model_rule(patient), language="text")

st.divider()

st.subheader("Prototype note")
st.info(
    "This prototype is used to test the expected WP17 workflow before real data and WP16 features are available. "
    "The current risk scores and explanations are placeholders and are not clinically meaningful."
)