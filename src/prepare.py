import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from joblib import dump
import numpy as np

# Script ini:
# - Membaca data mentah dari data/raw/dataset.csv (kolom: review,sentiment)
# - Jika file belum ada, membuat dataset contoh kecil agar pipeline tetap bisa jalan
# - Split train/test
# - Fit CountVectorizer (disimpan ke data/processed/vectorizer.joblib)
# - Simpan train/test CSV (masih dalam bentuk teks agar mudah dieksplor)

SAMPLE_DATA = [
    ("i love this movie, it was fantastic", "positive"),
    ("this product is amazing and works well", "positive"),
    ("what a great experience, super recommended", "positive"),
    ("absolutely happy with the service", "positive"),
    ("the tutorial was clear and helpful", "positive"),
    ("i hate this, very disappointing", "negative"),
    ("worst experience ever, not recommended", "negative"),
    ("the product broke after one day", "negative"),
    ("support was unhelpful and rude", "negative"),
    ("waste of money and time", "negative"),
    ("meh, it’s okay but not great", "negative"),
    ("pretty good overall", "positive"),
]

def ensure_dataset(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        df = pd.DataFrame(SAMPLE_DATA, columns=["review", "sentiment"])
        df.to_csv(path, index=False)
        print(f"[prepare] Created sample dataset at {path}")
    else:
        print(f"[prepare] Found dataset at {path}")

def main(args):
    raw_path = args.in_path
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    ensure_dataset(raw_path)
    df = pd.read_csv(raw_path)

    # Basic cleaning
    df["review"] = df["review"].astype(str).str.strip()
    df["sentiment"] = df["sentiment"].astype(str).str.lower().str.strip()
    df = df[df["review"].str.len() > 0]
    df = df[df["sentiment"].isin(["positive", "negative"])]

    # Split
    train_df, test_df = train_test_split(
        df, test_size=args.test_size, random_state=args.seed, stratify=df["sentiment"]
    )

    # Fit vectorizer 
    vectorizer = CountVectorizer(
        max_features=args.max_features,
        ngram_range=tuple(args.ngram_range),
    )
    vectorizer.fit(train_df["review"].values)

    # Simpan output
    train_out = os.path.join(out_dir, "train.csv")
    test_out = os.path.join(out_dir, "test.csv")
    vec_out = os.path.join(out_dir, "vectorizer.joblib")

    train_df.to_csv(train_out, index=False)
    test_df.to_csv(test_out, index=False)
    dump(vectorizer, vec_out)

    print(f"[prepare] Saved: {train_out}, {test_out}")
    print(f"[prepare] Saved vectorizer: {vec_out}")
    print(f"[prepare] Train size: {len(train_df)}, Test size: {len(test_df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_path", required=True)
    parser.add_argument("--out_dir", dest="out_dir", required=True)
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_features", type=int, default=5000)
    parser.add_argument("--ngram_range", nargs=2, type=int, default=[1, 2])
    args = parser.parse_args()
    main(args)
