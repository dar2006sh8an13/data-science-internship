# Project 4: Retail Sales Analytics
Domain: Retail / Business Analytics
Dataset: Tableau Sample Superstore (fictional retailer, transaction-style dataset)
Tools: Python, Pandas, NumPy, Matplotlib, Seaborn

## Business questions
- What are total sales, profit, orders, units, and profit margin?
- Which categories, sub-categories, segments, and regions perform best?
- Which areas generate losses?
- How do sales and profit change over time?
- Is discount associated with profit?

## Dataset and source
The script downloads the Sample Superstore CSV at runtime. It includes order dates, geography, customer segments, products, sales, quantity, discount, and profit. It represents a fictional retailer, not actual company accounts.
Official Tableau sample-data page: https://public.tableau.com/app/resources/sample-data
CSV mirror: https://github.com/vaibhavisnayak/data-analysis/blob/main/Sample%20-%20Superstore.csv

## Run
python -m venv .venv
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python analyze.py

The script downloads data into data/, cleans it, calculates KPIs, exports CSV tables and PNG charts into results/, and generates REPORT.md.

## Limitations
Correlation is not causation. Discount/profit relationships may be affected by product mix, region, and order size. This sample is fictional and is for educational analysis, not actual company reporting or forecasting.
