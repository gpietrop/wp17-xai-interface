import pandas as pd


def predict_probability(patient: pd.Series) -> float:
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


def assign_risk_class(probability: float) -> str:
    if probability >= 0.70:
        return "High"
    if probability >= 0.35:
        return "Medium"
    return "Low"


def explain_prediction(patient: pd.Series) -> list[str]:
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
        reasons.append("No major high-risk factor is detected in this explanation.")

    return reasons


def get_model_rule(patient: pd.Series) -> str:
    if patient["ldl_c"] > 190 and patient["has_pathogenic_variant"] == 1:
        return "IF LDL-C > 190 AND pathogenic variant = yes THEN high risk"
    if patient["ldl_c"] > 160 and patient["family_history"] == 1:
        return "IF LDL-C > 160 AND family history = yes THEN medium risk"
    return "IF no major high-risk factor is present THEN low risk"