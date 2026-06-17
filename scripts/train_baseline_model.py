from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS = PROJECT_ROOT / "models"

DATASET_PATH = PROCESSED / "ml_match_dataset.csv"
MODEL_PATH = MODELS / "baseline_random_forest.joblib"
PREDICTIONS_PATH = PROCESSED / "baseline_validation_predictions.csv"


DROP_FROM_FEATURES = {
    "target",
    "result",
    "goal_diff_home",
    "home_score",
    "away_score",
    "fotmob_home_score",
    "fotmob_away_score",
    "fotmob_status",
    "fotmob_match_status",
    "fotmob_utc_time",
    "match_score",
    "match_reversed",
}


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["date", "fotmob_match_id"]).reset_index(drop=True)


def make_feature_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    drop_cols = [c for c in DROP_FROM_FEATURES if c in df.columns]
    x = df.drop(columns=drop_cols)
    y = df["target"]

    # 날짜 자체는 누수는 아니지만 RandomForest에 직접 넣기보다 월/연도로 분해합니다.
    x["match_year"] = df["date"].dt.year
    x["match_month"] = df["date"].dt.month
    x = x.drop(columns=["date"], errors="ignore")

    return x, y


def build_pipeline(x: pd.DataFrame) -> Pipeline:
    numeric_cols = x.select_dtypes(include=[np.number, "bool"]).columns.tolist()
    categorical_cols = [c for c in x.columns if c not in numeric_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_cols),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=3)),
                    ]
                ),
                categorical_cols,
            ),
        ],
        remainder="drop",
    )

    model = RandomForestClassifier(
        n_estimators=500,
        min_samples_leaf=5,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline(steps=[("preprocess", preprocessor), ("model", model)])


def main() -> None:
    df = load_dataset()

    split_date = df["date"].quantile(0.8)
    train_df = df[df["date"].le(split_date)].copy()
    valid_df = df[df["date"].gt(split_date)].copy()

    x_train, y_train = make_feature_frame(train_df)
    x_valid, y_valid = make_feature_frame(valid_df)

    pipeline = build_pipeline(x_train)
    pipeline.fit(x_train, y_train)

    pred = pipeline.predict(x_valid)
    proba = pipeline.predict_proba(x_valid)

    print(f"train rows: {len(train_df)}")
    print(f"valid rows: {len(valid_df)}")
    print(f"split date: {pd.Timestamp(split_date).date()}")
    print(f"accuracy: {accuracy_score(y_valid, pred):.4f}")
    print(f"log_loss: {log_loss(y_valid, proba, labels=pipeline.classes_):.4f}")
    print()
    print(classification_report(y_valid, pred, digits=4))

    pred_df = valid_df[
        ["date", "home_team", "away_team", "home_score", "away_score", "target"]
    ].copy()
    pred_df["predicted"] = pred
    for idx, cls in enumerate(pipeline.classes_):
        pred_df[f"prob_{cls}"] = proba[:, idx]

    MODELS.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    pred_df.to_csv(PREDICTIONS_PATH, index=False, encoding="utf-8-sig")
    print(f"saved model: {MODEL_PATH}")
    print(f"saved predictions: {PREDICTIONS_PATH}")


if __name__ == "__main__":
    main()
