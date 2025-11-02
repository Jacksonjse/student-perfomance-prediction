# backend/model_utils.py
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import joblib

NUMERIC_FEATURES = [
    "weekly_self_study_hours",
    "attendance_percentage",
    "class_participation",
    "total_score",
]

def build_pipeline(model_type="random_forest", random_state=42):
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    preprocessor = ColumnTransformer(
        transformers=[("num", numeric_transformer, NUMERIC_FEATURES)],
        remainder="drop"
    )

    if model_type == "logistic":
        clf = LogisticRegression(max_iter=200, random_state=random_state)
    else:
        clf = RandomForestClassifier(n_estimators=100, random_state=random_state)

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("clf", clf)])
    return pipeline

def save_model(pipeline, path="model.joblib"):
    joblib.dump(pipeline, path)

def load_model(path="model.joblib"):
    return joblib.load(path)
