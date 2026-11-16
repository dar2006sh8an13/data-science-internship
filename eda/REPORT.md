# Exploratory Data Analysis Report

## 1. Objective
Explore the diabetes dataset using descriptive statistics, visualizations, correlation analysis, and interpretation of potentially influential features.

## 2. Dataset overview
- Source: scikit-learn built-in `load_diabetes` dataset.
- Observations: **442**.
- Input features: **10** numeric features.
- Target: a quantitative disease-progression measure.
- Missing values: **0**.
- Feature values are standardized/centered in the source dataset; coefficients should not be read as raw clinical units.

## 3. Statistical summaries
The full descriptive statistics (count, mean, standard deviation, quartiles, minimum and maximum) are in `results/statistical_summary.csv`. Feature distributions are visualized in `results/feature_distributions.png`.

## 4. Correlation findings
Pearson correlation measures linear association, not causation. The feature with the largest absolute linear correlation with the target is **bmi** (r = **0.586**). The strongest off-diagonal feature-to-feature relationship is **s1** and **s2** (r = **0.897**).

See `results/target_correlations.csv`, `results/correlation_matrix.csv`, and `results/correlation_heatmap.png`. Scatterplots with fitted linear trends for the four most target-correlated features are in `results/top_feature_relationships.png`.

## 5. Key influencing factors (interpretation)
The ranking in `results/target_correlations.csv` identifies features most strongly associated with the target in a one-variable linear sense. These are exploratory signals, not proof that a feature causes progression or is the best predictor in a multivariable model. Correlated predictors can share information.

## 6. Conclusions
1. The dataset contains 442 complete observations and 10 numeric predictors.
2. Correlation analysis highlights bmi as the strongest individual linear correlate of the target in this dataset.
3. The heatmap helps identify relationships among predictors and potential multicollinearity.
4. Histograms and scatterplots reveal distribution shape and linear trends, while also showing why further modelling and validation may be needed.

## 7. Limitations
- This is a small, preprocessed teaching dataset, not a representative current population sample.
- Pearson correlation captures linear association and can miss nonlinear relationships.
- Correlation does not establish causation.
- No causal inference or clinical recommendation is made.

## 8. Reproducibility
Run `python analyze.py` after installing dependencies in `requirements.txt`. Outputs are regenerated in `results/`.
