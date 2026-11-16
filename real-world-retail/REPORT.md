# Retail Sales Analytics — Completed Report

## Dataset and scope
Tableau Sample Superstore is a fictional retail company dataset. It includes order identifiers and dates, customer segments, geography, products, sales, quantity, discount, and profit. The analysis processed **9,994** transaction rows from **9,994** CSV rows.

## Executive KPIs
| Metric | Result |
|---|---:|
| Transaction rows | 9,994 |
| Unique orders | 5,009 |
| Unique customers | 793 |
| Unique products | 1,862 |
| Total sales | $2,297,200.86 |
| Total profit | $286,397.02 |
| Profit margin | 12.47% |
| Units sold | 37,873 |
| Average discount | 15.62% |

## Findings
- Highest-profit category: **Technology** ($145,454.95).
- Lowest-profit category: **Furniture** ($18,451.27).
- Highest-profit region: **West**.
- Highest-profit sub-category: **Copiers** ($55,617.82).
- Lowest-profit sub-category: **Tables** (-$17,725.48).
- Discount-profit Pearson correlation: **-0.219**.
- 48 monthly periods were analyzed.

## Interpretation and recommendations
Discount/profit correlation describes association, not causation. Product mix, region, and order size may influence the observed relationship. Investigate loss-making sub-categories, evaluate discount guardrails by category and region, and monitor profit margin alongside revenue. Test changes before rolling out pricing policies.

## Limitations
The dataset is fictional and intended for learning. Results are descriptive, not causal or predictive. Do not present these numbers as actual company performance.

## Reproducibility
Run `pip install -r requirements.txt` then `python analyze.py`. The script downloads the dataset and regenerates analysis outputs. The committed CSV tables and SVG charts in this folder were calculated from the source CSV above.
