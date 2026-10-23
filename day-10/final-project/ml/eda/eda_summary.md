# Smart Hygiene Risk Prediction System - EDA & Visual Analytics Report

## 1. Overview
- **Dataset Sample Size**: 3,500 verified inspection records
- **Features Tracked**: 14 operational and environmental hazard indicators
- **Target Variables**: 
  - `hygiene_risk_level`: 3-Tier Classification (Low Risk, Medium Risk, High Risk)
  - `hygiene_risk_score`: Continuous index from 0.0 to 100.0

## 2. Risk Distribution Summary
- **Low Risk (Grade A)**: 1,584 inspections (45.3%)
- **Medium Risk (Grade B)**: 1,416 inspections (40.5%)
- **High Risk (Grade C)**: 500 inspections (14.3%)

## 3. Key Findings & Hazard Correlation
1. **Critical Failure Multipliers**: Failures in temperature control and pest audit correlate highest with elevated hazard risk (correlation > 0.82).
2. **Environmental Pressure**: Facilities with ambient kitchen temperatures exceeding 32°C and relative humidity over 75% exhibit a 2.4x higher probability of critical microbial hazards.
3. **Repeat Non-Compliance**: Facilities with 3 or more historical violations demonstrate an exponential jump in risk score, necessitating automated regulatory intervention.

## 4. Visual Artifacts
- **Correlation Heatmap**: `eda_correlation_matrix.png`
- **Facility Risk Breakdown**: `eda_risk_distribution.png`
- **Feature Importance Ranking**: `eda_feature_importance.png`
- **Violation Progression**: `eda_violations_vs_risk.png`
- **Algorithm Benchmark**: `eda_model_benchmark_comparison.png`
- **Confusion Matrix**: `eda_confusion_matrix.png`
