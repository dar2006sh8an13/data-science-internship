from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cleaning import quality_report, clean_data, outlier_bounds


def sample_frame():
    return pd.DataFrame({
        "Name": ["A", "B", "B", "D", None],
        "Age": [20, None, None, 40, 30],
        "Salary": [30000, 40000, 40000, 250000, None],
        "Department": ["IT", "HR", "HR", "Finance", "IT"],
    })


def test_quality_report_counts_missing_and_duplicates():
    report = quality_report(sample_frame())
    assert report["missing_by_column"]["Age"] == 2
    assert report["missing_by_column"]["Salary"] == 1
    assert report["exact_duplicate_rows"] == 1


def test_cleaning_removes_duplicates_and_imputes():
    cleaned, audit = clean_data(sample_frame())
    assert len(cleaned) == 4
    assert cleaned[["Age", "Salary", "Name", "Department"]].isna().sum().sum() == 0
    assert audit["duplicate_rows_removed"] == 1


def test_outliers_are_flaged_not_dropped():
    cleaned, _ = clean_data(sample_frame())
    assert len(cleaned) == 4
    assert cleaned["Salary_outlier"].sum() >= 1


def test_iqr_bounds_are_ordered():
    lower, upper = outlier_bounds(pd.series([1, 2, 3, 4, 5]))
    assert lower < upper
