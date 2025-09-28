import argparse
import json
import pandas as pd
from joblib import load, dump
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import yaml

# Script ini:
# - Membaca train.csv dan vectorizer
# - Melatih Logistic Regression dalam Pipeline (Vectorizer -> LR)
# - Log parameter & metric awal ke MLflow
# - Simpan model ke models/model.pkl
# - Tulis metrics.json

def main(args):
    # Baca params.yaml
    with open(args.params, "r") as f:
        params = yaml.safe_load(f)
    seed = params.get("seed", 42)
    model_cfg = params.get("model", {})
    vec_path = "data/processed/vectorizer.joblib"

    # Siapkan data
    train_df = pd.read_csv(args.train)
    X_train = train_df["review"].astype(str).values
    y_train = train_df["sentiment"].values
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)  # negative=0, positive=1

    # Load vectorizer & buat pipeline (Vectorizer -> LR)
    vectorizer = load(vec_path)
    clf = LogisticRegression(
        C=model_cfg.get("C", 1.0),
        max_iter=model_cfg.get("max_iter", 100),
        penalty=model_cfg.get("penalty", "l2"),
        random_state=seed,
    )

    pipe = Pipeline([
        ("vec", vectorizer),
        ("clf", clf),
    ])

    # MLflow tracking (lokal)
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("sentiment-demo")
    with mlflow.start_run():
        mlflow.log_params({
            "C": clf.C,
            "max_iter": clf.max_iter,
            "penalty": clf.penalty,
            "seed": seed,
        })

        pipe.fit(X_train, y_train_enc)
        y_pred = pipe.predict(X_train)
        acc = accuracy_score(y_train_enc, y_pred)
        f1 = f1_score(y_train_enc, y_pred)

        mlflow.log_metrics({"train_accuracy": acc, "train_f1": f1})
        # Simpan model (pakai joblib agar ringan)
        dump(pipe, args.model)
        mlflow.log_artifact(args.model, artifact_path="artifacts")

        # Tulis metrics.json (akan di-collect DVC)
        with open("metrics.json", "w") as f:
            json.dump({"train_accuracy": acc, "train_f1": f1}, f, indent=2)

        print(f"[train] Saved model to {args.model}")
        print(f"[train] train_accuracy={acc:.4f} train_f1={f1:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--params", required=True)
    args = parser.parse_args()
    main(args)
