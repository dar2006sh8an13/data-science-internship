# Project 3 — Exploratory Data Analysis (EDA)

A reproducible data exploration project using scikit-learn's built-in diabetes dataset.

## Objectives
- Calculate descriptive statistical summaries.
- Visualize feature distributions and relationships.
- Identify Pearson correlations and potentially influential features.
- Present findings, limitations, and conclusions in a structured report.

## Dataset
The dataset contains 442 observations, 10 numeric input features, and a quantitative target. Features are preprocessed/standardized in the source dataset. It is bundled with scikit-learn, so no external download or private data is required.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python analyze.py
```

Generated outputs are saved under `results/`; the written analysis is `REPORT.md`.

## Interpretation
Pearson correlation describes linear association, not causation. A high absolute correlation does not prove that a feature causes the target or that it is the strongest feature in a multivariable predictive model. This educational dataset is not intended for clinical decision-making.
