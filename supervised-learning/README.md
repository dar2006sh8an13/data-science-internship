# Project 2 — Supervised Learning & Model Evaluation

Train and compare three supervised **classification** models using scikit-learn's built-in Wisconsin Breast Cancer dataset (569 samples, 30 numeric features). No external data download or private data is needed.

> Educational demonstration only. The models are not suitable for medical diagnosis or clinical decision-making.

## Models
- Logistic Regression (linear classification baseline)
- Decision Tree Classifier
- Random Forest Classifier

**Why not Linear Regression?** Linear Regression predicts continuous values. This project predicts two discrete classes, so Logistic Regression is the relevant linear classification baseline.

## Workflow
1. Load the built-in dataset.
2. Make a stratified 80/20 train/test split (`random_state=42`).
3. Fit preprocessing on training data only with a scikit-learn `Pipeline`.
4. Train each classifier and predict on the held-out test set.
5. Evaluate accuracy, precision, recall, F1, confusion matrix, ROC-AUC.
6. Save comparison CSV, classification reports, confusion-matrix charts, and a combined ROC plot.

## Setup
From the repository root:

```bash
pip install -r supervised-learning/requirements.txt
python supervised-learning/train.py
```

Outputs are written to `supervised-learning/results/`. Results are **not** precomputed in the repository; run the script to reproduce them.

## Tests
```bash
pytest -q supervised-learning/tests
```

## Files
- `train.py`: model training, evaluation and plots
- `requirements.txt`: dependencies
- `tests/test_train.py`: reproducibility and evaluation checks

## Notes
ROC-AUC uses probability estimates for the positive class (class 1, benign). The train/test split is stratified and shared by all three models. Reported test metrics are descriptive comparisons on one held-out split, not estimates of clinical utility.
