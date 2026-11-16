# Project 2 — Supervised Learning & Model Evaluation

Train and compare Logistic Regression, Decision Tree, and Random Forest classifiers using scikit-learn's built-in Wisconsin Breast Cancer dataset (569 samples, 30 numeric features). Educational demonstration only; not suitable for medical diagnosis.

## Run
From repository root:
```bash
pip install -r supervised-learning/requirements.txt
python supervised-learning/train.py
pytest -q supervised-learning/tests
``

The script generates confusion matrices, a combined ROC curve, per-model classification reports, and a comparison CSV under `supervised-learning/results/`.

## Evaluation (held-out test set)
Stratified 80/20 split, random_state=42 (455 train rows, 114 test rows). Class 1 is benign.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9825 | 0.9861 | 0.9861 | 0.9861 | 0.9954 |
| Random Forest | 0.9561 | 0.9589 | 0.9722 | 0.9655 | 0.9940 |
| Decision Tree | 0.9035 | 0.9420 | 0.9028 | 0.9220 | 0.9373 |

These are results from one fixed hold-out split, not cross-validation or clinical performance claims. Logistic Regression performed best on this particular split. The dataset and model are for learning only.

## Contents
- `train.py`: data split, model training, evaluation, plots and reports
- `tests/test_train.py`: automated tests
- `results/`: generated metrics and classification reports
