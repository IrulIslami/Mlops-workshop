import argparse
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report
from joblib import load

# Script ini:
# - Membaca test.csv dan model.pkl
# - Menghasilkan metrics.json (accuracy, f1) di data test

def main(args):
    test_df = pd.read_csv(args.test)
    X_test = test_df["review"].astype(str).values
    y_test = test_df["sentiment"].values
    le = LabelEncoder()
    y_test_enc = le.fit_transform(y_test)

    model = load(args.model)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test_enc, y_pred)
    f1 = f1_score(y_test_enc, y_pred)

    with open(args.out, "w") as f:
        json.dump({"test_accuracy": acc, "test_f1": f1}, f, indent=2)

    print(f"[eval] test_accuracy={acc:.4f} test_f1={f1:.4f}")
    print("[eval] detailed report:")
    print(classification_report(y_test_enc, y_pred, target_names=["negative", "positive"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    main(args)
