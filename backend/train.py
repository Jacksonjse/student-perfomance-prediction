# backend/train.py
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from model_utils import build_pipeline, save_model, NUMERIC_FEATURES

def prepare_label(df, pass_threshold=50):
    # If total_score numeric exists, use threshold; else fallback to grade mapping
    if "total_score" in df.columns:
        df["label"] = (df["total_score"].astype(float) >= pass_threshold).astype(int)
    else:
        # Example fallback mapping: adjust as needed.
        df["label"] = df["grade"].apply(lambda g: 0 if str(g).strip().lower() in ["f", "fail"] else 1)
    return df

def main(csv_path, model_type="random_forest", pass_threshold=50, out_path="model.joblib"):
    df = pd.read_csv(csv_path)
    df = prepare_label(df, pass_threshold)
    X = df[["weekly_self_study_hours", "attendance_percentage", "class_participation", "total_score"]]
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = build_pipeline(model_type=model_type)
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    save_model(pipeline, out_path)
    print("Saved model to", out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to StudentPerformance.csv")
    parser.add_argument("--model", default="random_forest", choices=["random_forest","logistic"])
    parser.add_argument("--threshold", type=float, default=50.0, help="pass threshold on total_score")
    parser.add_argument("--out", default="model.joblib")
    args = parser.parse_args()
    main(args.csv, model_type=args.model, pass_threshold=args.threshold, out_path=args.out)
