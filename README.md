# WP17 XAI Interface Prototype

This repository contains an early prototype for the WP17 explainable risk profiling interface of the FH-EARLY project
For now, the interface uses mock patient data and placeholder prediction rules.

## Questions

WP17 will develop an explainable model and a clinician-facing tool for patient-level risk profiling. This prototype can helps us clarify:

- what patient information should be shown
- what input format WP17 expects
- how predictions and explanations should be presented
- which parts belong to the model and which belong to the interface

## Streamlit

Streamlit is used because it allows fast development of interactive Python dashboards without requiring frontend development. 
Streamlit is only used as the prototype interface. The prediction and explanation logic should remain separate, so it can later be reused in another deployment platform if needed.

## Current status

The current version (will) includes:

- mock patient data
- patient selection
- patient-level variable display
- placeholder risk prediction
- simple rule-based explanation
