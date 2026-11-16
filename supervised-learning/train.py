"""Compare three supervised classifiers on a public, built-in example dataset.

Educational example only; not for medical use.
Run: python supervised-learning/train.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
OUTPUT_DIR = Path(__file__).resolve().parent / "results"


def get_data():
    """Load the bundled dataset and create one reproducible stratified split."""
    dataset = load_breast_cancer()
    x = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = pd.Series(dataset.target, name="target")
    return train_test_split(
        x, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
    )


def make_models():
    """Create independent pipelines; scaling is fit on training data only."""
    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
        ]),
        "Decision Tree": Pipeline([
            ("model", DecisionTreeClassifier(
                max_depth=5, min_samples_leaf=3, random_state=RANDOM_STATE
            )),
        ]),
        "Random Forest": Pipeline([
            ("model", RandomForestClassifier(
                n_estimators=200, min_samples_leaf=2, random_state=RANDOM_STATE,
                n_jobs=-1
            )),
        ]),
    }


def evaluate_model(model, x_test, y_test):
    """Return numeric classification metrics and data for diagnostic plots."""
    predicted = model.predict(x_test)
    positive_probability = model.predict_proba(x_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, predicted)),
        "precision": float(precision_score(y_test, predicted, zero_division=0)),
        "recall": float(recall_score(y_test, predicted, zero_division=0)),
        "f1": float(f1_score(y_test, predicted, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, positive_probability)),
    }
    return metrics, predicted, positive_probability


def run(output_dir=OUTPUT_DIR):
    """Train models, evaluate on untouched test data, and save plots/reports."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    x_train, x_test, y_train, y_test = get_data()

    results = []
    roc_fig, roc_ax = plt.subplots(figsize=(8, 6))

    for name, model in make_models().items():
        model.fit(x_train, y_train)
        metrics, predicted, probability = evaluate_model(model, x_test, y_test)
        results.append({"model": name, **metrics})
        slug = name.lower().replace(" ", "_")

        matrix = confusion_matrix(y_test, predicted, labels=[0, 1])
        fig, ax = plt.subplots(figsize=(6, 5))
        ConfusionMatrixDisplay(
            confusion_matrix=matrix, display_labels=["Malignant", "Benign"]
        ).plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
        ax.set_title(f"{name} — Confusion Matrix")
        fig.tight_layout()
        fig.savefig(output_dir / f"{slug}_confusion_matrix.png", dpi=150)
        plt.close(fig)

        report = classification_report(
            y_test, predicted, target_names=["Malignant", "Benign"],
            output_dict=True, zero_division=0
        )
        (output_dir / f"{slug}_classification_report.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )

        false_positive_rate, true_positive_rate, _ = roc_curve(
            y_test, probability, pos_label=1
        )
        roc_ax.plot(
            false_positive_rate, true_positive_rate,
            label=f"{name} (AUC={metrics['roc_auc']:.3f})"
        )

    roc_ax.plot([0, 1], [0, 1], "k--", label="Random baseline")
    roc_ax.set(
        xlabel="False Positive Rate", ylabel="True Positive Rate",
        title="ROC Curves — Held-Out Test Set", xlim=(0, 1), ylim=(0, 1.02)
    )
    roc_ax.legend(loc="lower right")
    roc_fig.tight_layout()
    roc_fig.savefig(output_dir / "roc_curves.png", dpi=150)
    plt.close(roc_fig)

    table = pd.DataFrame(results).sort_values("roc_auc", ascending=False)
    table.to_csv(output_dir / "model_comparison.csv", index=False)
    print(f"Training rows: {len(x_train)} | Test rows: {len(x_test)}")
    print(table.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print(f"Reports saved to: {output_dir}")
    return table


if __name__ == "__main__":
    run()
