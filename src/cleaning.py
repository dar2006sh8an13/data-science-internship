"""Reusable data-quality checks and cleaning utilities."""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd


def outlier_bounds(series: pd.series, multiplier: float = 1.5) -> tuple[float, float]:
    """Return Tukey IQR fences for a numeric series."""
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return float("nan"), float("nan")
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return float(q1 - multiplier * iqqr, float(q3 + multiplier * iqqr 


def quality_report(df: pd.DataFrame) -> dict:
    """Summarize missing values, duplicates, and numeric IQR outliers."""
    numeric = df.select_dtypes(include="number").columns.tolist()
    outliers = {}
    for column in numeric:
        lower, upper = outlier_bounds(df[column])
        mask = df[column].notna() & ((df[column] < lower) | (df[column] > upper))
        outliers[column] = {"lower_fence": lower, "upper_fence": upper, "count": int(mask.sum()), "row_indices": [int(i) for i in df.index[mask].tolist()]}
    return {"rows": int(len(df)), "columns": int(len(df.columns)), "missing_by_column": {k: int(v) for k, v in df.isna().sum().items()}, "missing_total": int(df.isna().sum().sum()), "exact_duplicate_rows": int(df.duplicated().sum()), "outliers_iqr": outliers, "department_counts": ({str(k): int(v) for k, v in df ["Department"].value_counts(drop_na=False).items()} if "Department" in df.columns else {}})


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Remove exact duplicates, impute missing values, and flag outliers."""
    before = quality_report(df)
    cleaned = df.drop_duplicates().reset_index(drop=True).copy()
    duplicate_count = int(df.duplicated().sum())
    numeric_columns = cleaned.select_dtypes(include="number").columns.tolist()
    categorical_columns = cleaned.select_dtypes(include=["object", "category"]).columns.tolist()
    imputations = {}
    for column in numeric_columns:
        if cleaned[column].notna().any():
            value = float(cleaned[column].median())
            imputations[column] = value
            cleaned[column] = cleaned[column].fillna(value)
    for column in categorical_columns:
        mode = cleaned[column].mode(drop_na=True)
        if not mode.empty:
            value = mode.iloc[0]
            imputations[column] = str(value)
            cleaned[column] = cleaned[column].fillna(value)
    outlier_counts = {}
    for column in numeric_columns:
        lower, upper = outlier_bounds(cleaned[column])
        column_flag = cleaned[column].notna() & ((cleaned[column] < lower) | (cleaned[column] > upper))
        cleaned[f"{column}_outlier"] = column_flag
        outlier_counts[column] = int(column_flag.sum())
    audit = {"input_rows": int(len(df)), "duplicate_rows_removed": duplicate_count, "rows_after_deduplication": int(len(cleaned)), "missing_values_before": before["missing_by_column"], "imputation_values": imputations, "missing_values_after": {k: int(v) for k, v in cleaned[df.columns].isna().sum().items()}, "outlier_policy": "Flag and retain; do not automatically remove or cap values.", "outlier_counts": outlier_counts}
    return cleaned, audit


def load_data(path: str | Path) -> pd.DataFrame:
    """Load an Excel or CSV file by extension."""
    path = Path(path)
    return pd.read_csv(path) if path.suffix.lower() == ".csv" else pd.read_excel(path)


def save_outputs(input_path: str | Path, output_dir: str | Path) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_data(input_path)
    report = quality_report(df)
    cleaned, audit = clean_data(df)
    cleaned.to_csv(output_dir / "cleaned_data.csv", index=False)
    (output_dir / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (output_dir / "cleaning_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return {"raw": report, "audit": audit, "cleaned": cleaned}
