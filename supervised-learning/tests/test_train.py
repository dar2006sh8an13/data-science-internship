"""Tests for the public-dataset supervised-learning workflow."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("supervised_training", ROOT / "train.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_stratified_split_is_reproducible():
    first = module.get_data()
    second = module.get_data()
    assert len(first[0]) + len(first[1]) == 569
    assert first[0].index.tolist() == second[0].index.tolist()
    assert first[1].index.tolist() == second[1].index.tolist()
    assert set(first[2].unique()) == {0, 1}


def test_all_models_produce_valid_metrics():
    x_train, x_test, y_train, y_test = module.get_data()
    models = module.make_models()
    assert len(models) == 3
    for model in models.values():
        model.fit(x_train, y_train)
        metrics, predictions, probabilities = module.evaluate_model(
            model, x_test, y_test
        )
        assert len(predictions) == len(y_test)
        assert len(probabilities) == len(y_test)
        assert all(0 <= value <= 1 for value in metrics.values())


def test_run_creates_expected_reports(tmp_path):
    comparison = module.run(tmp_path)
    assert len(comparison) == 3
    assert (tmp_path / "model_comparison.csv").exists()
    assert (tmp_path / "roc_curves.png").exists()
    for name in ("logistic_regression", "decision_tree", "random_forest"):
        assert (tmp_path / f"{name}_confusion_matrix.png").exists()
        assert (tmp_path / f"{name}_classification_report.json").exists()
