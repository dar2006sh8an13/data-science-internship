"""Exploratory data analysis of scikit-learn's diabetes dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_diabetes

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def main():
    dataset = load_diabetes(as_frame=True)
    df = dataset.frame.copy()
    target = "target"
    features = [column for column in df.columns if column != target]

    df.describe().T.to_csv(OUT / "statistical_summary.csv")
    df.isna().sum().rename("missing_values").to_frame().to_csv(OUT / "missing_values.csv")

    correlation = df.corr(numeric_only=True)
    correlation.to_csv(OUT / "correlation_matrix.csv")
    target_corr = correlation[target].drop(target).sort_values(
        key=lambda values: values.abs(), ascending=False
    )
    target_corr.rename("pearson_correlation_with_target").to_csv(
        OUT / "target_correlations.csv"
    )

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(11, 8))
    sns.heatmap(correlation, cmap="coolwarm", center=0, annot=True, fmt=".2f", square=True)
    plt.title("Diabetes Dataset — Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(OUT / "correlation_heatmap.png", dpi=160)
    plt.close()

    df[features].hist(figsize=(14, 10), bins=20, edgecolor="black")
    plt.suptitle("Feature Distributions", y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / "feature_distributions.png", dpi=160, bbox_inches="tight")
    plt.close()

    top_features = target_corr.head(4).index.tolist()
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for axis, feature in zip(axes.flat, top_features):
        sns.regplot(
            data=df, x=feature, y=target,
            scatter_kws={"alpha": 0.55, "s": 22},
            line_kws={"color": "red"}, ax=axis
        )
        axis.set_title(f"{feature} vs target (r={correlation.loc[feature, target]:.3f})")
    plt.tight_layout()
    plt.savefig(OUT / "top_feature_relationships.png", dpi=160)
    plt.close()

    print(f"Rows: {len(df)} | Features: {len(features)}")
    print(f"Missing values: {int(df.isna().sum().sum())}")
    print("\nPearson correlation with target (absolute strength, descending):")
    print(target_corr.to_string())


if __name__ == "__main__":
    main()
