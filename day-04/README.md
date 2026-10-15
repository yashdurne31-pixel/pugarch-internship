# Day 4 — Machine Learning: Facility Hygiene Risk Prediction

## Project Overview
A beginner machine-learning workflow that compares Logistic Regression and Random Forest for classifying facility hygiene risk.

## Problem Statement
Use facility cleanliness and operational indicators to predict whether a record is labelled Low or High hygiene risk.

## Features
- cleanliness_score
- odor_score
- waste_level (encoded: Low=0, Medium=1, High=2)
- complaints
- footfall
- hours_since_cleaning

Target: hygiene_risk (Low=0, High=1).

## Important Dataset Limitation
The dataset and its labels are synthetic and generated from an illustrative scoring rule for training purposes. They are not real facility inspection records or independently verified outcomes. Evaluation metrics demonstrate the ML workflow only and must not be presented as validated real-world performance.

## Technology Stack
Python, NumPy, pandas, scikit-learn, joblib.

## Workflow
1. Generate sample data.
2. Preprocess and encode categorical values.
3. Split data into 80% training and 20% testing.
4. Train Logistic Regression and Random Forest.
5. Evaluate accuracy, precision, recall, F1-score, and confusion matrices.
6. Save model files and predictions.

## Folder Structure
- `dataset/`: raw and preprocessed datasets
- `preprocessing/`: preprocessing script
- `models/`: trained model files and training script
- `evaluation/`: metrics and model comparison
- `predictions/`: test-set and sample predictions

## Installation
```bash
python -m pip install numpy pandas matplotlib scikit-learn joblib
```

## How to Run
From the project root:
```bash
python complete_day4.py
```

## Outputs
- `evaluation/model_metrics.json`
- `evaluation/model_comparison.csv`
- `evaluation/evaluation_report.txt`
- `predictions/test_set_predictions.csv`
- `predictions/sample_prediction.csv`
- trained `.joblib` models

## Challenges Faced
- The original Day 3 dataset did not include every requested feature or a validated hygiene-risk target.
- A synthetic dataset was used so the complete pipeline could be demonstrated reproducibly.

## Solutions
- Generated a seeded synthetic dataset and documented its limitations.
- Used the same train/test split to compare both algorithms.

## Future Improvements
- Replace synthetic data with real, quality-checked facility records and verified risk labels.
- Validate data with domain experts, assess class imbalance, and test on an independent dataset before operational use.
