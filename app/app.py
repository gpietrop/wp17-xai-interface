from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "mock" / "mock_patients.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def get_mock_probability(patient: pd.Series) -> float:
    score = 0.0

    if patient["ldl_c"] > 190:
        score += 0.30
    if patient["has_pathogenic_variant"] == 1:
        score += 0.30
    if patient["previous_cvd_event"] == 1:
        score += 0.25
    if patient["lipoprotein_a"] > 50:
        score += 0.15
    if patient["family_history"] == 1:
        score += 0.10

    return min(score, 0.95)


def get_explanation(patient: pd.Series) -> list[str]:
    reasons = []

    if patient["ldl_c"] > 190:
        reasons.append("LDL-C is above 190 mg/dL.")
    if patient["has_pathogenic_variant"] == 1:
        reasons.append("A pathogenic variant is present.")
    if patient["previous_cvd_event"] == 1:
        reasons.append("The patient has a previous cardiovascular event.")
    if patient["lipoprotein_a"] > 50:
        reasons.append("Lipoprotein(a) is elevated.")
    if patient["family_history"] == 1:
        reasons.append("Family history is positive.")

    if not reasons:
        reasons.append("No major high-risk factor is detected in this mock explanation.")

    return reasons


def get_mock_rule(patient: pd.Series) -> str:
    if patient["ldl_c"] > 190 and patient["has_pathogenic_variant"] == 1:
        return "IF LDL-C > 190 AND pathogenic variant = yes THEN high risk"
    if patient["ldl_c"] > 160 and patient["family_history"] == 1:
        return "IF LDL-C > 160 AND family history = yes THEN medium risk"
    return "IF no major high-risk factor is present THEN low risk"


st.set_page_config(
    page_title="WP17 XAI Risk Prototype",
    layout="wide",
)

st.title("WP17 XAI Risk Profiling Prototype")
st.caption("Mock interface for testing the structure of the WP17 clinician-facing tool. Data and predictions are synthetic.")

df = load_data()

with st.sidebar:
    st.header("Patient selection")
    patient_id = st.selectbox("Select patient", df["patient_id"])

patient = df.loc[df["patient_id"] == patient_id].iloc[0]
probability = get_mock_probability(patient)

risk_class = patient["risk_label"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Predicted risk class", risk_class)

with col2:
    st.metric("Mock risk probability", f"{probability:.0%}")

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

    for reason in get_explanation(patient):
        st.write(f"- {reason}")

    st.subheader("Model rule")
    st.code(get_mock_rule(patient), language="text")

st.divider()

st.subheader("Clinical note")
st.info(
    "This prototype is only a structural mock-up. "
    "The current risk scores and explanations are rule-based placeholders. "
    "They will later be replaced by WP17 explainable models trained on WP16 features."
)