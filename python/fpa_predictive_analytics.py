"""
Python export of notebooks/fpa_predictive_analytics.ipynb.

This is a cell-by-cell export; the original notebook is unchanged.
The notebook uses Kaggle dataset paths under /kaggle/input.
Update DATA_PATH before running outside Kaggle.
"""

def display(value):
    """Print notebook-style results when running this export as a script."""
    if hasattr(value, "to_string"):
        print(value.to_string())
    else:
        print(value)

# %% [notebook cell 1]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# The original KaggleHub example import was omitted because this notebook
# reads the dataset directly from DATA_PATH rather than downloading it.

# %% [notebook cell 2]
import os

for root, dirs, files in os.walk("/kaggle/input"):
    level = root.replace("/kaggle/input", "").count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}/")

    for file in files[:10]:
        print(f"{indent}  {file}")

# %% [notebook cell 3]
import pandas as pd
from pathlib import Path

# Location of our dataset
DATA_PATH = Path(
    "/kaggle/input/datasets/shrutimeshram29/financial-fpa-analytics-dataset"
)

# Find all CSV files
files = list(DATA_PATH.glob("*.csv"))

# Number of files
print("Number of CSV files:", len(files))

# File names
print("\nFiles:")

for file in files:
    print("-", file.name)

# %% [notebook cell 4]
import os

print("FILE SIZES")
print("=" * 60)

for file in files:
    size_mb = os.path.getsize(file) / (1024 * 1024)
    print(f"{file.name:40} {size_mb:8.2f} MB")

# %% [notebook cell 5]
import os

print("FILE SIZES")
print("=" * 60)

for file in files:
    size_mb = os.path.getsize(file) / (1024 * 1024)
    print(f"{file.name:40} {size_mb:8.2f} MB")

# %% [notebook cell 6]
gl_account = pd.read_csv(
    DATA_PATH / "dim_gl_account.csv"
)

# %% [notebook cell 7]
gl_account.head()

# %% [notebook cell 8]
gl_account.shape

# %% [notebook cell 9]
gl_account.columns

# %% [notebook cell 10]
gl_account.info()

# %% [notebook cell 11]
gl_account.isna().sum()

# %% [notebook cell 12]
gl_account.duplicated().sum()

# %% [notebook cell 13]
actuals_path = DATA_PATH / "acdoca_actuals.csv"

actuals = pd.read_csv(
    actuals_path,
    low_memory=False
)

print("Number of rows:", f"{actuals.shape[0]:,}")
print("Number of columns:", actuals.shape[1])

print("\nColumn names:")
print(actuals.columns.tolist())

print("\nFirst 5 rows:")
display(actuals.head())

# %% [notebook cell 14]
column_mapping = {
    "BUKRS": "company_code",
    "BELNR": "document_number",
    "GJAHR": "fiscal_year",
    "MONAT": "fiscal_month",
    "BUDAT": "posting_date",
    "BLDAT": "document_date",
    "BLART": "document_type",
    "WAERS": "currency",
    "VERSION": "accounting_version",
    "USNAM": "created_by",
    "STBLG": "reversal_document",
    "BUZEI": "line_item",
    "BSCHL": "posting_key",
    "SHKZG": "debit_credit",
    "HKONT": "gl_account",
    "KOSTL": "cost_center",
    "PRCTR": "profit_center",
    "DMBTR": "local_currency_amount",
    "WRBTR": "document_currency_amount"
}

# %% [notebook cell 15]
actuals_clean = actuals.rename(columns=column_mapping)

# %% [notebook cell 16]
print(actuals_clean.columns.tolist())

# %% [notebook cell 17]
print("Original columns:")
print(actuals.columns.tolist())

print("\nCleaned columns:")
print(actuals_clean.columns.tolist())

# %% [notebook cell 18]
display(actuals_clean.head())

# %% [notebook cell 19]
actuals_clean.dtypes

# %% [notebook cell 20]
actuals_clean["posting_date"] = pd.to_datetime(
    actuals_clean["posting_date"],
    errors="coerce"
)

actuals_clean["document_date"] = pd.to_datetime(
    actuals_clean["document_date"],
    errors="coerce"
)

# %% [notebook cell 21]
print(actuals_clean[["posting_date", "document_date"]].dtypes)

# %% [notebook cell 22]
missing_values = (
    actuals_clean.isna()
    .sum()
    .sort_values(ascending=False)
)

display(missing_values.to_frame("missing_count"))

# %% [notebook cell 23]
missing_summary = pd.DataFrame({
    "missing_count": actuals_clean.isna().sum(),
    "missing_percentage": (
        actuals_clean.isna().mean() * 100
    ).round(2)
})

missing_summary = missing_summary.sort_values(
    "missing_percentage",
    ascending=False
)

display(missing_summary)

# %% [notebook cell 24]
duplicate_count = actuals_clean.duplicated().sum()

print("Duplicate rows:", f"{duplicate_count:,}")

# %% [notebook cell 25]
print("Company codes:")
print(actuals_clean["company_code"].unique())

# %% [notebook cell 26]
print("Fiscal years:")
print(sorted(actuals_clean["fiscal_year"].unique()))

# %% [notebook cell 27]
print("Fiscal months:")
print(sorted(actuals_clean["fiscal_month"].unique()))

# %% [notebook cell 28]
print("Currencies:")
print(actuals_clean["currency"].value_counts())

# %% [notebook cell 29]
print("Debit/Credit distribution:")
print(actuals_clean["debit_credit"].value_counts())

# %% [notebook cell 30]
print("Number of unique G/L accounts:")
print(actuals_clean["gl_account"].nunique())

# %% [notebook cell 31]
print(
    actuals_clean["gl_account"].value_counts().head(20)
)

# %% [notebook cell 32]
actuals_clean["local_currency_amount"].describe()

# %% [notebook cell 33]
missing_summary[
    missing_summary["missing_count"] > 0
]

# %% [notebook cell 34]
duplicate_count = actuals_clean.duplicated().sum()

print("Duplicate rows:", f"{duplicate_count:,}")

# %% [notebook cell 35]
line_item_duplicates = actuals_clean.duplicated(
    subset=["document_number", "line_item"]
).sum()

print(
    "Duplicate document + line item combinations:",
    f"{line_item_duplicates:,}"
)

# %% [notebook cell 36]
print("Earliest posting date:")
print(actuals_clean["posting_date"].min())

print("\nLatest posting date:")
print(actuals_clean["posting_date"].max())

# %% [notebook cell 37]
currency_distribution = (
    actuals_clean["currency"]
    .value_counts()
)

display(currency_distribution)

# %% [notebook cell 38]
debit_credit_distribution = (
    actuals_clean["debit_credit"]
    .value_counts()
)

display(debit_credit_distribution)

# %% [notebook cell 39]
actuals_clean["local_currency_amount"].describe()

# %% [notebook cell 40]
duplicate_key_count = actuals_clean.duplicated(
    subset=[
        "company_code",
        "fiscal_year",
        "document_number",
        "line_item"
    ]
).sum()

print(
    "Duplicate company + year + document + line item:",
    f"{duplicate_key_count:,}"
)

# %% [notebook cell 41]
gl_account = pd.read_csv(
    DATA_PATH / "dim_gl_account.csv"
)

gl_account = gl_account.rename(
    columns={
        "HKONT": "gl_account",
        "TXT50": "gl_account_name",
        "CATEGORY": "financial_category"
    }
)

display(gl_account.head())

# %% [notebook cell 42]
actuals_analysis = actuals_clean.merge(
    gl_account[
        ["gl_account", "gl_account_name", "financial_category"]
    ],
    on="gl_account",
    how="left"
)

display(
    actuals_analysis[
        [
            "gl_account",
            "gl_account_name",
            "financial_category",
            "cost_center"
        ]
    ].head()
)

# %% [notebook cell 43]
cost_center_analysis = (
    actuals_analysis
    .groupby("financial_category")
    .agg(
        total_transactions=("gl_account", "size"),
        missing_cost_centers=(
            "cost_center",
            lambda x: x.isna().sum()
        )
    )
)

cost_center_analysis["missing_percentage"] = (
    cost_center_analysis["missing_cost_centers"]
    / cost_center_analysis["total_transactions"]
    * 100
).round(2)

display(cost_center_analysis)

# %% [notebook cell 44]
category_summary = (
    actuals_analysis
    .groupby("financial_category")
    .agg(
        transaction_count=("gl_account", "size"),
        total_amount=("local_currency_amount", "sum"),
        average_amount=("local_currency_amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
)

display(category_summary)

# %% [notebook cell 45]
company_currency_summary = (
    actuals_analysis
    .groupby(["company_code", "currency"])
    .agg(
        transaction_count=("gl_account", "size"),
        total_local_amount=("local_currency_amount", "sum"),
        total_document_amount=("document_currency_amount", "sum")
    )
    .reset_index()
)

display(company_currency_summary)

# %% [notebook cell 46]
debit_credit_amount = (
    actuals_analysis
    .groupby("debit_credit")
    .agg(
        transaction_count=("gl_account", "size"),
        total_amount=("local_currency_amount", "sum"),
        average_amount=("local_currency_amount", "mean"),
        minimum_amount=("local_currency_amount", "min"),
        maximum_amount=("local_currency_amount", "max")
    )
    .reset_index()
)

display(debit_credit_amount)

# %% [notebook cell 47]
category_debit_credit = (
    actuals_analysis
    .groupby(["financial_category", "debit_credit"])
    .agg(
        transaction_count=("gl_account", "size"),
        total_amount=("local_currency_amount", "sum")
    )
    .reset_index()
)

display(category_debit_credit)

# %% [notebook cell 48]
document_balance = (
    actuals_analysis
    .groupby(
        ["company_code", "fiscal_year", "document_number", "debit_credit"]
    )["local_currency_amount"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)

display(document_balance.head(20))

# %% [notebook cell 49]
document_balance["balance_difference"] = (
    document_balance["H"] -
    document_balance["S"]
)

print(
    "Total documents:",
    f"{len(document_balance):,}"
)

print(
    "Balanced documents:",
    (document_balance["balance_difference"].abs() < 0.01).sum()
)

print(
    "Unbalanced documents:",
    (document_balance["balance_difference"].abs() >= 0.01).sum()
)

# %% [notebook cell 50]
print(actuals_analysis["debit_credit"].unique())

# %% [notebook cell 51]
print(actuals_analysis["debit_credit"].value_counts())

# %% [notebook cell 52]
actuals_analysis["signed_amount"] = (
    actuals_analysis["local_currency_amount"]
    .where(
        actuals_analysis["debit_credit"] == "S",
        -actuals_analysis["local_currency_amount"]
    )
)

display(
    actuals_analysis[
        [
            "gl_account",
            "financial_category",
            "debit_credit",
            "local_currency_amount",
            "signed_amount"
        ]
    ].head(10)
)

# %% [notebook cell 53]
actuals_analysis[
    ["debit_credit", "local_currency_amount", "signed_amount"]
].groupby("debit_credit").agg(
    original_total=("local_currency_amount", "sum"),
    signed_total=("signed_amount", "sum")
)

# %% [notebook cell 54]
category_summary = (
    actuals_analysis
    .groupby("financial_category")["signed_amount"]
    .agg(
        transaction_count="count",
        total_signed_amount="sum",
        average_signed_amount="mean"
    )
    .reset_index()
    .sort_values("total_signed_amount", ascending=False)
)

display(category_summary)

# %% [notebook cell 55]
pnl_categories = [
    "REVENUE",
    "COGS",
    "PERSONNEL",
    "OPEX",
    "DEPRECIATION"
]

pnl_data = actuals_analysis[
    actuals_analysis["financial_category"].isin(pnl_categories)
].copy()

print("P&L transactions:", f"{len(pnl_data):,}")

display(
    pnl_data[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "financial_category",
            "debit_credit",
            "local_currency_amount",
            "signed_amount",
            "currency"
        ]
    ].head(10)
)

# %% [notebook cell 56]
monthly_category = (
    pnl_data
    .groupby(
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "financial_category"
        ]
    )["signed_amount"]
    .sum()
    .reset_index()
)

display(monthly_category.head(20))

# %% [notebook cell 57]
monthly_pnl = (
    monthly_category
    .pivot_table(
        index=[
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency"
        ],
        columns="financial_category",
        values="signed_amount",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

monthly_pnl.columns.name = None

display(monthly_pnl.head(10))

# %% [notebook cell 58]
# Convert accounting signs into business-friendly P&L values

monthly_pnl["Revenue"] = -monthly_pnl["REVENUE"]

monthly_pnl["COGS_Expense"] = -monthly_pnl["COGS"]

monthly_pnl["Personnel_Expense"] = -monthly_pnl["PERSONNEL"]

monthly_pnl["OPEX_Expense"] = -monthly_pnl["OPEX"]

monthly_pnl["Depreciation_Expense"] = -monthly_pnl["DEPRECIATION"]


# Calculate Gross Profit
monthly_pnl["Gross_Profit"] = (
    monthly_pnl["Revenue"]
    - monthly_pnl["COGS_Expense"].abs()
)


# Calculate Operating Profit
monthly_pnl["Operating_Profit"] = (
    monthly_pnl["Gross_Profit"]
    - monthly_pnl["Personnel_Expense"].abs()
    - monthly_pnl["OPEX_Expense"].abs()
    - monthly_pnl["Depreciation_Expense"].abs()
)


# Calculate margins
monthly_pnl["Gross_Margin_%"] = (
    monthly_pnl["Gross_Profit"]
    / monthly_pnl["Revenue"]
) * 100

monthly_pnl["Operating_Margin_%"] = (
    monthly_pnl["Operating_Profit"]
    / monthly_pnl["Revenue"]
) * 100


display(
    monthly_pnl[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Revenue",
            "COGS_Expense",
            "Gross_Profit",
            "Personnel_Expense",
            "OPEX_Expense",
            "Depreciation_Expense",
            "Operating_Profit",
            "Gross_Margin_%",
            "Operating_Margin_%"
        ]
    ].head(10)
)

# %% [notebook cell 59]
# Create presentation-friendly expense columns

monthly_pnl["COGS_Display"] = monthly_pnl["COGS"].abs()
monthly_pnl["Personnel_Display"] = monthly_pnl["PERSONNEL"].abs()
monthly_pnl["OPEX_Display"] = monthly_pnl["OPEX"].abs()
monthly_pnl["Depreciation_Display"] = monthly_pnl["DEPRECIATION"].abs()

display(
    monthly_pnl[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Revenue",
            "COGS_Display",
            "Gross_Profit",
            "Personnel_Display",
            "OPEX_Display",
            "Depreciation_Display",
            "Operating_Profit"
        ]
    ].head(10)
)

# %% [notebook cell 60]
plan = pd.read_csv(
    "/kaggle/input/datasets/shrutimeshram29/financial-fpa-analytics-dataset/plan_versions.csv"
)

plan.head()

# %% [notebook cell 61]
plan = plan.rename(columns={
    "BUKRS": "company_code",
    "GJAHR": "fiscal_year",
    "MONAT": "fiscal_month",
    "VERSION": "version_number",
    "VERSION_": "plan_version",
    "KOSTL": "cost_center",
    "PRCTR": "profit_center",
    "HKONT": "gl_account",
    "CATEGORY": "financial_category",
    "WAERS": "currency",
    "DMBTR": "planned_amount"
})

plan.head()

# %% [notebook cell 62]
print(plan.columns.tolist())

# %% [notebook cell 63]
display(plan.head())

# %% [notebook cell 64]
plan_summary = (
    plan
    .groupby(
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "financial_category",
            "VERSION_TXT"
        ]
    )["planned_amount"]
    .sum()
    .reset_index()
)

display(plan_summary.head(20))

# %% [notebook cell 65]
print(plan["VERSION_TXT"].value_counts())

# %% [notebook cell 66]
plan_version_summary = (
    plan_summary
    .groupby("VERSION_TXT")["planned_amount"]
    .agg(
        total_planned_amount="sum",
        average_planned_amount="mean",
        record_count="count"
    )
    .reset_index()
)

display(plan_version_summary)

# %% [notebook cell 67]
plan_comparison = (
    plan_summary
    .groupby(
        [
            "company_code",
            "currency",
            "financial_category",
            "VERSION_TXT"
        ]
    )["planned_amount"]
    .sum()
    .reset_index()
)

display(plan_comparison.head(20))

# %% [notebook cell 68]
plan_pivot = (
    plan_comparison
    .pivot_table(
        index=[
            "company_code",
            "currency",
            "financial_category"
        ],
        columns="VERSION_TXT",
        values="planned_amount",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

plan_pivot.columns.name = None

display(plan_pivot.head(20))

# %% [notebook cell 69]
plan_pivot["Forecast_Variance"] = (
    plan_pivot["Rolling Forecast"]
    - plan_pivot["Budget"]
)

display(plan_pivot.head(20))

# %% [notebook cell 70]
plan_pivot["Forecast_Variance_%"] = (
    plan_pivot["Forecast_Variance"]
    / plan_pivot["Budget"]
) * 100

display(plan_pivot.head(20))

# %% [notebook cell 71]
display(
    plan_pivot[
        [
            "company_code",
            "currency",
            "financial_category",
            "Budget",
            "Rolling Forecast",
            "Forecast_Variance",
            "Forecast_Variance_%"
        ]
    ].head(20)
)

# %% [notebook cell 72]
budget_data = plan[
    plan["VERSION_TXT"] == "Budget"
].copy()

print("Budget records:", f"{len(budget_data):,}")

display(
    budget_data[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "financial_category",
            "currency",
            "planned_amount"
        ]
    ].head(10)
)

# %% [notebook cell 73]
budget_monthly = (
    budget_data
    .groupby(
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "financial_category"
        ]
    )["planned_amount"]
    .sum()
    .reset_index()
)

display(budget_monthly.head(20))

# %% [notebook cell 74]
budget_pnl = (
    budget_monthly
    .pivot_table(
        index=[
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency"
        ],
        columns="financial_category",
        values="planned_amount",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

budget_pnl.columns.name = None

display(budget_pnl.head(10))

# %% [notebook cell 75]
budget_pnl = budget_pnl.rename(columns={
    "REVENUE": "Budget_Revenue",
    "COGS": "Budget_COGS",
    "PERSONNEL": "Budget_Personnel",
    "OPEX": "Budget_OPEX",
    "DEPRECIATION": "Budget_Depreciation"
})

display(budget_pnl.head(10))

# %% [notebook cell 76]
actual_pnl = monthly_pnl[
    [
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency",
        "Revenue",
        "COGS_Expense",
        "Personnel_Expense",
        "OPEX_Expense",
        "Depreciation_Expense"
    ]
].copy()

display(actual_pnl.head(10))

# %% [notebook cell 77]
actual_pnl = actual_pnl.rename(columns={
    "Revenue": "Actual_Revenue",
    "COGS_Expense": "Actual_COGS",
    "Personnel_Expense": "Actual_Personnel",
    "OPEX_Expense": "Actual_OPEX",
    "Depreciation_Expense": "Actual_Depreciation"
})

display(actual_pnl.head(10))

# %% [notebook cell 78]
actual_vs_budget = actual_pnl.merge(
    budget_pnl,
    on=[
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency"
    ],
    how="inner"
)

display(actual_vs_budget.head(10))

# %% [notebook cell 79]
actual_vs_budget["Revenue_Variance"] = (
    actual_vs_budget["Actual_Revenue"]
    - actual_vs_budget["Budget_Revenue"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Budget_Revenue",
            "Revenue_Variance"
        ]
    ].head(10)
)

# %% [notebook cell 80]
actual_vs_budget["Revenue_Variance_%"] = (
    actual_vs_budget["Revenue_Variance"]
    / actual_vs_budget["Budget_Revenue"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Budget_Revenue",
            "Revenue_Variance",
            "Revenue_Variance_%"
        ]
    ].head(10)
)

# %% [notebook cell 81]
# Calculate expense variances using positive expense amounts

actual_vs_budget["COGS_Variance"] = (
    actual_vs_budget["Actual_COGS"].abs()
    - actual_vs_budget["Budget_COGS"]
)

actual_vs_budget["Personnel_Variance"] = (
    actual_vs_budget["Actual_Personnel"].abs()
    - actual_vs_budget["Budget_Personnel"]
)

actual_vs_budget["OPEX_Variance"] = (
    actual_vs_budget["Actual_OPEX"].abs()
    - actual_vs_budget["Budget_OPEX"]
)

actual_vs_budget["Depreciation_Variance"] = (
    actual_vs_budget["Actual_Depreciation"].abs()
    - actual_vs_budget["Budget_Depreciation"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_COGS",
            "Budget_COGS",
            "COGS_Variance",
            "Actual_Personnel",
            "Budget_Personnel",
            "Personnel_Variance",
            "Actual_OPEX",
            "Budget_OPEX",
            "OPEX_Variance",
            "Actual_Depreciation",
            "Budget_Depreciation",
            "Depreciation_Variance"
        ]
    ].head(10)
)

# %% [notebook cell 82]
# Calculate variance percentages

actual_vs_budget["COGS_Variance_%"] = (
    actual_vs_budget["COGS_Variance"]
    / actual_vs_budget["Budget_COGS"]
) * 100

actual_vs_budget["Personnel_Variance_%"] = (
    actual_vs_budget["Personnel_Variance"]
    / actual_vs_budget["Budget_Personnel"]
) * 100

actual_vs_budget["OPEX_Variance_%"] = (
    actual_vs_budget["OPEX_Variance"]
    / actual_vs_budget["Budget_OPEX"]
) * 100

actual_vs_budget["Depreciation_Variance_%"] = (
    actual_vs_budget["Depreciation_Variance"]
    / actual_vs_budget["Budget_Depreciation"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "COGS_Variance",
            "COGS_Variance_%",
            "Personnel_Variance",
            "Personnel_Variance_%",
            "OPEX_Variance",
            "OPEX_Variance_%",
            "Depreciation_Variance",
            "Depreciation_Variance_%"
        ]
    ].head(10)
)

# %% [notebook cell 83]
# Calculate variance percentages

actual_vs_budget["COGS_Variance_%"] = (
    actual_vs_budget["COGS_Variance"]
    / actual_vs_budget["Budget_COGS"]
) * 100

actual_vs_budget["Personnel_Variance_%"] = (
    actual_vs_budget["Personnel_Variance"]
    / actual_vs_budget["Budget_Personnel"]
) * 100

actual_vs_budget["OPEX_Variance_%"] = (
    actual_vs_budget["OPEX_Variance"]
    / actual_vs_budget["Budget_OPEX"]
) * 100

actual_vs_budget["Depreciation_Variance_%"] = (
    actual_vs_budget["Depreciation_Variance"]
    / actual_vs_budget["Budget_Depreciation"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "COGS_Variance",
            "COGS_Variance_%",
            "Personnel_Variance",
            "Personnel_Variance_%",
            "OPEX_Variance",
            "OPEX_Variance_%",
            "Depreciation_Variance",
            "Depreciation_Variance_%"
        ]
    ].head(10)
)

# %% [notebook cell 84]
actual_vs_budget["Actual_Gross_Profit"] = (
    actual_vs_budget["Actual_Revenue"]
    - actual_vs_budget["Actual_COGS"].abs()
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Actual_COGS",
            "Actual_Gross_Profit"
        ]
    ].head(10)
)

# %% [notebook cell 85]
actual_vs_budget["Budget_Gross_Profit"] = (
    actual_vs_budget["Budget_Revenue"]
    - actual_vs_budget["Budget_COGS"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Profit",
            "Budget_Gross_Profit"
        ]
    ].head(10)
)

# %% [notebook cell 86]
actual_vs_budget["Gross_Profit_Variance"] = (
    actual_vs_budget["Actual_Gross_Profit"]
    - actual_vs_budget["Budget_Gross_Profit"]
)

actual_vs_budget["Gross_Profit_Variance_%"] = (
    actual_vs_budget["Gross_Profit_Variance"]
    / actual_vs_budget["Budget_Gross_Profit"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Profit",
            "Budget_Gross_Profit",
            "Gross_Profit_Variance",
            "Gross_Profit_Variance_%"
        ]
    ].head(10)
)

# %% [notebook cell 87]
actual_vs_budget["Actual_Operating_Profit"] = (
    actual_vs_budget["Actual_Gross_Profit"]
    - actual_vs_budget["Actual_Personnel"].abs()
    - actual_vs_budget["Actual_OPEX"].abs()
    - actual_vs_budget["Actual_Depreciation"].abs()
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Profit",
            "Actual_Personnel",
            "Actual_OPEX",
            "Actual_Depreciation",
            "Actual_Operating_Profit"
        ]
    ].head(10)
)

# %% [notebook cell 88]
actual_vs_budget["Budget_Operating_Profit"] = (
    actual_vs_budget["Budget_Gross_Profit"]
    - actual_vs_budget["Budget_Personnel"]
    - actual_vs_budget["Budget_OPEX"]
    - actual_vs_budget["Budget_Depreciation"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Profit",
            "Budget_Operating_Profit"
        ]
    ].head(10)
)

# %% [notebook cell 89]
actual_vs_budget["Operating_Profit_Variance"] = (
    actual_vs_budget["Actual_Operating_Profit"]
    - actual_vs_budget["Budget_Operating_Profit"]
)

actual_vs_budget["Operating_Profit_Variance_%"] = (
    actual_vs_budget["Operating_Profit_Variance"]
    / actual_vs_budget["Budget_Operating_Profit"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Profit",
            "Budget_Operating_Profit",
            "Operating_Profit_Variance",
            "Operating_Profit_Variance_%"
        ]
    ].head(10)
)

# %% [notebook cell 90]
actual_vs_budget["Actual_Gross_Margin_%"] = (
    actual_vs_budget["Actual_Gross_Profit"]
    / actual_vs_budget["Actual_Revenue"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Actual_Gross_Profit",
            "Actual_Gross_Margin_%"
        ]
    ].head(10)
)

# %% [notebook cell 91]
actual_vs_budget["Budget_Gross_Margin_%"] = (
    actual_vs_budget["Budget_Gross_Profit"]
    / actual_vs_budget["Budget_Revenue"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Margin_%",
            "Budget_Gross_Margin_%"
        ]
    ].head(10)
)

# %% [notebook cell 92]
actual_vs_budget["Actual_Operating_Margin_%"] = (
    actual_vs_budget["Actual_Operating_Profit"]
    / actual_vs_budget["Actual_Revenue"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Profit",
            "Actual_Operating_Margin_%"
        ]
    ].head(10)
)

# %% [notebook cell 93]
actual_vs_budget["Budget_Operating_Margin_%"] = (
    actual_vs_budget["Budget_Operating_Profit"]
    / actual_vs_budget["Budget_Revenue"]
) * 100

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Margin_%",
            "Budget_Operating_Margin_%"
        ]
    ].head(10)
)

# %% [notebook cell 94]
actual_vs_budget["Gross_Margin_Variance_pp"] = (
    actual_vs_budget["Actual_Gross_Margin_%"]
    - actual_vs_budget["Budget_Gross_Margin_%"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Margin_%",
            "Budget_Gross_Margin_%",
            "Gross_Margin_Variance_pp"
        ]
    ].head(10)
)

# %% [notebook cell 95]
actual_vs_budget["Operating_Margin_Variance_pp"] = (
    actual_vs_budget["Actual_Operating_Margin_%"]
    - actual_vs_budget["Budget_Operating_Margin_%"]
)

display(
    actual_vs_budget[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Margin_%",
            "Budget_Operating_Margin_%",
            "Operating_Margin_Variance_pp"
        ]
    ].head(10)
)

# %% [notebook cell 96]
executive_summary = actual_vs_budget[
    [
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency",
        "Actual_Revenue",
        "Budget_Revenue",
        "Revenue_Variance",
        "Revenue_Variance_%",
        "Actual_Gross_Profit",
        "Budget_Gross_Profit",
        "Gross_Profit_Variance",
        "Gross_Profit_Variance_%",
        "Actual_Operating_Profit",
        "Budget_Operating_Profit",
        "Operating_Profit_Variance",
        "Operating_Profit_Variance_%",
        "Actual_Gross_Margin_%",
        "Budget_Gross_Margin_%",
        "Gross_Margin_Variance_pp",
        "Actual_Operating_Margin_%",
        "Budget_Operating_Margin_%",
        "Operating_Margin_Variance_pp"
    ]
].copy()

display(executive_summary.head(10))

# %% [notebook cell 97]
print("Rows:", f"{len(executive_summary):,}")
print("Columns:", len(executive_summary.columns))

# %% [notebook cell 98]
kpi_summary = actual_vs_budget[
    [
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency",
        "Actual_Revenue",
        "Budget_Revenue",
        "Revenue_Variance",
        "Actual_Gross_Profit",
        "Budget_Gross_Profit",
        "Gross_Profit_Variance",
        "Actual_Operating_Profit",
        "Budget_Operating_Profit",
        "Operating_Profit_Variance",
        "Actual_Gross_Margin_%",
        "Budget_Gross_Margin_%",
        "Actual_Operating_Margin_%",
        "Budget_Operating_Margin_%"
    ]
].copy()

display(kpi_summary.head(10))

# %% [notebook cell 99]
rolling_forecast_data = plan[
    plan["VERSION_TXT"] == "Rolling Forecast"
].copy()

print(
    "Rolling Forecast records:",
    f"{len(rolling_forecast_data):,}"
)

display(
    rolling_forecast_data[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "financial_category",
            "currency",
            "planned_amount"
        ]
    ].head(10)
)

# %% [notebook cell 100]
rolling_monthly = (
    rolling_forecast_data
    .groupby(
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "financial_category"
        ]
    )["planned_amount"]
    .sum()
    .reset_index()
)

display(rolling_monthly.head(20))

# %% [notebook cell 101]
rolling_pnl = (
    rolling_monthly
    .pivot_table(
        index=[
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency"
        ],
        columns="financial_category",
        values="planned_amount",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

rolling_pnl.columns.name = None

display(rolling_pnl.head(10))

# %% [notebook cell 102]
rolling_pnl = rolling_pnl.rename(columns={
    "REVENUE": "Forecast_Revenue",
    "COGS": "Forecast_COGS",
    "PERSONNEL": "Forecast_Personnel",
    "OPEX": "Forecast_OPEX",
    "DEPRECIATION": "Forecast_Depreciation"
})

display(rolling_pnl.head(10))

# %% [notebook cell 103]
actual_budget_forecast = actual_pnl.merge(
    budget_pnl,
    on=[
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency"
    ],
    how="inner"
)

display(actual_budget_forecast.head(10))

# %% [notebook cell 104]
actual_budget_forecast = actual_budget_forecast.merge(
    rolling_pnl,
    on=[
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency"
    ],
    how="inner"
)

display(actual_budget_forecast.head(10))

# %% [notebook cell 105]
actual_budget_forecast["Revenue_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_Revenue"]
    - actual_budget_forecast["Forecast_Revenue"]
)

actual_budget_forecast["Revenue_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Revenue_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Revenue"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Forecast_Revenue",
            "Revenue_Actual_vs_Forecast",
            "Revenue_Actual_vs_Forecast_%"
        ]
    ].head(10)
)

# %% [notebook cell 106]
actual_budget_forecast["Revenue_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Revenue_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Revenue"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Forecast_Revenue",
            "Revenue_Actual_vs_Forecast",
            "Revenue_Actual_vs_Forecast_%"
        ]
    ].head(10)
)

# %% [notebook cell 107]
# COGS: Actual expense vs Forecast expense
actual_budget_forecast["COGS_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_COGS"].abs()
    - actual_budget_forecast["Forecast_COGS"]
)

# Personnel
actual_budget_forecast["Personnel_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_Personnel"].abs()
    - actual_budget_forecast["Forecast_Personnel"]
)

# OPEX
actual_budget_forecast["OPEX_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_OPEX"].abs()
    - actual_budget_forecast["Forecast_OPEX"]
)

# Depreciation
actual_budget_forecast["Depreciation_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_Depreciation"].abs()
    - actual_budget_forecast["Forecast_Depreciation"]
)

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "COGS_Actual_vs_Forecast",
            "Personnel_Actual_vs_Forecast",
            "OPEX_Actual_vs_Forecast",
            "Depreciation_Actual_vs_Forecast"
        ]
    ].head(10)
)

# %% [notebook cell 108]
actual_budget_forecast["COGS_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["COGS_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_COGS"]
) * 100

actual_budget_forecast["Personnel_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Personnel_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Personnel"]
) * 100

actual_budget_forecast["OPEX_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["OPEX_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_OPEX"]
) * 100

actual_budget_forecast["Depreciation_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Depreciation_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Depreciation"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "COGS_Actual_vs_Forecast_%",
            "Personnel_Actual_vs_Forecast_%",
            "OPEX_Actual_vs_Forecast_%",
            "Depreciation_Actual_vs_Forecast_%"
        ]
    ].head(10)
)

# %% [notebook cell 109]
actual_budget_forecast["Actual_Gross_Profit"] = (
    actual_budget_forecast["Actual_Revenue"]
    - actual_budget_forecast["Actual_COGS"].abs()
)

# %% [notebook cell 110]
actual_budget_forecast["Forecast_Gross_Profit"] = (
    actual_budget_forecast["Forecast_Revenue"]
    - actual_budget_forecast["Forecast_COGS"]
)

# %% [notebook cell 111]
actual_budget_forecast["Gross_Profit_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_Gross_Profit"]
    - actual_budget_forecast["Forecast_Gross_Profit"]
)

actual_budget_forecast["Gross_Profit_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Gross_Profit_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Gross_Profit"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Gross_Profit",
            "Forecast_Gross_Profit",
            "Gross_Profit_Actual_vs_Forecast",
            "Gross_Profit_Actual_vs_Forecast_%"
        ]
    ].head(10)
)

# %% [notebook cell 112]
actual_budget_forecast["Actual_Operating_Profit"] = (
    actual_budget_forecast["Actual_Gross_Profit"]
    - actual_budget_forecast["Actual_Personnel"].abs()
    - actual_budget_forecast["Actual_OPEX"].abs()
    - actual_budget_forecast["Actual_Depreciation"].abs()
)

# %% [notebook cell 113]
actual_budget_forecast["Forecast_Operating_Profit"] = (
    actual_budget_forecast["Forecast_Gross_Profit"]
    - actual_budget_forecast["Forecast_Personnel"]
    - actual_budget_forecast["Forecast_OPEX"]
    - actual_budget_forecast["Forecast_Depreciation"]
)

# %% [notebook cell 114]
actual_budget_forecast["Operating_Profit_Actual_vs_Forecast"] = (
    actual_budget_forecast["Actual_Operating_Profit"]
    - actual_budget_forecast["Forecast_Operating_Profit"]
)

actual_budget_forecast["Operating_Profit_Actual_vs_Forecast_%"] = (
    actual_budget_forecast["Operating_Profit_Actual_vs_Forecast"]
    / actual_budget_forecast["Forecast_Operating_Profit"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Operating_Profit",
            "Forecast_Operating_Profit",
            "Operating_Profit_Actual_vs_Forecast",
            "Operating_Profit_Actual_vs_Forecast_%"
        ]
    ].head(10)
)

# %% [notebook cell 115]
actual_budget_forecast["Revenue_Forecast_Error"] = (
    actual_budget_forecast["Actual_Revenue"]
    - actual_budget_forecast["Forecast_Revenue"]
)

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Forecast_Revenue",
            "Revenue_Forecast_Error"
        ]
    ].head(10)
)

# %% [notebook cell 116]
actual_budget_forecast["Revenue_Absolute_Error"] = (
    actual_budget_forecast["Revenue_Forecast_Error"].abs()
)

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Revenue_Forecast_Error",
            "Revenue_Absolute_Error"
        ]
    ].head(10)
)

# %% [notebook cell 117]
actual_budget_forecast["Revenue_Absolute_Percentage_Error"] = (
    actual_budget_forecast["Revenue_Absolute_Error"]
    / actual_budget_forecast["Actual_Revenue"]
) * 100

display(
    actual_budget_forecast[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "currency",
            "Actual_Revenue",
            "Forecast_Revenue",
            "Revenue_Absolute_Percentage_Error"
        ]
    ].head(10)
)

# %% [notebook cell 118]
revenue_mape = (
    actual_budget_forecast["Revenue_Absolute_Percentage_Error"]
    .mean()
)

print(
    "Revenue MAPE:",
    round(revenue_mape, 2),
    "%"
)

# %% [notebook cell 119]
company_revenue_mape = (
    actual_budget_forecast
    .groupby(["company_code", "currency"])
    ["Revenue_Absolute_Percentage_Error"]
    .mean()
    .reset_index()
)

company_revenue_mape = company_revenue_mape.rename(
    columns={
        "Revenue_Absolute_Percentage_Error": "Revenue_MAPE_%"
    }
)

display(company_revenue_mape)

# %% [notebook cell 120]
total_absolute_error = (
    actual_budget_forecast["Revenue_Absolute_Error"]
    .sum()
)

total_actual_revenue = (
    actual_budget_forecast["Actual_Revenue"]
    .sum()
)

revenue_wape = (
    total_absolute_error
    / total_actual_revenue
) * 100

print(
    "Revenue WAPE:",
    round(revenue_wape, 2),
    "%"
)

# %% [notebook cell 121]
company_wape = (
    actual_budget_forecast
    .groupby(["company_code", "currency"])
    .agg(
        total_absolute_error=(
            "Revenue_Absolute_Error",
            "sum"
        ),
        total_actual_revenue=(
            "Actual_Revenue",
            "sum"
        )
    )
    .reset_index()
)

company_wape["Revenue_WAPE_%"] = (
    company_wape["total_absolute_error"]
    / company_wape["total_actual_revenue"]
) * 100

display(company_wape)

# %% [notebook cell 122]
ml_revenue = actual_budget_forecast[
    actual_budget_forecast["company_code"] == 1000
].copy()

ml_revenue = ml_revenue[
    [
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "currency",
        "Actual_Revenue"
    ]
].copy()

display(ml_revenue.head(10))

# %% [notebook cell 123]
print("Number of monthly observations:", len(ml_revenue))

display(
    ml_revenue[
        ["fiscal_year", "fiscal_month", "Actual_Revenue"]
    ].tail(10)
)

# %% [notebook cell 124]
ml_revenue["date"] = pd.to_datetime(
    ml_revenue["fiscal_year"].astype(str)
    + "-"
    + ml_revenue["fiscal_month"].astype(str)
    + "-01"
)

ml_revenue = ml_revenue.sort_values("date").reset_index(drop=True)

display(
    ml_revenue[
        [
            "date",
            "fiscal_year",
            "fiscal_month",
            "Actual_Revenue"
        ]
    ].head(10)
)

# %% [notebook cell 125]
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))

plt.plot(
    ml_revenue["date"],
    ml_revenue["Actual_Revenue"]
)

plt.title("Company 1000 - Monthly Actual Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %% [notebook cell 126]
train = ml_revenue.iloc[:-12].copy()
test = ml_revenue.iloc[-12:].copy()

print("Training observations:", len(train))
print("Testing observations:", len(test))

print("\nTraining period:")
print(train["date"].min(), "to", train["date"].max())

print("\nTesting period:")
print(test["date"].min(), "to", test["date"].max())

# %% [notebook cell 127]
ml_revenue["lag_1"] = (
    ml_revenue["Actual_Revenue"].shift(1)
)

ml_revenue["lag_2"] = (
    ml_revenue["Actual_Revenue"].shift(2)
)

ml_revenue["lag_3"] = (
    ml_revenue["Actual_Revenue"].shift(3)
)

ml_revenue["lag_12"] = (
    ml_revenue["Actual_Revenue"].shift(12)
)

display(
    ml_revenue[
        [
            "date",
            "Actual_Revenue",
            "lag_1",
            "lag_2",
            "lag_3",
            "lag_12"
        ]
    ].head(20)
)

# %% [notebook cell 128]
ml_revenue_model = ml_revenue.dropna().copy()

print(
    "Rows available for ML:",
    len(ml_revenue_model)
)

display(
    ml_revenue_model.head(10)
)

# %% [notebook cell 129]
ml_train = ml_revenue_model.iloc[:-12].copy()
ml_test = ml_revenue_model.iloc[-12:].copy()

print("ML training observations:", len(ml_train))
print("ML testing observations:", len(ml_test))

print("\nTraining period:")
print(ml_train["date"].min(), "to", ml_train["date"].max())

print("\nTesting period:")
print(ml_test["date"].min(), "to", ml_test["date"].max())

# %% [notebook cell 130]
features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_12"
]

X_train = ml_train[features]
y_train = ml_train["Actual_Revenue"]

X_test = ml_test[features]
y_test = ml_test["Actual_Revenue"]

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# %% [notebook cell 131]
from sklearn.ensemble import RandomForestRegressor

# %% [notebook cell 132]
rf_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    max_depth=5
)

# %% [notebook cell 133]
rf_model.fit(
    X_train,
    y_train
)

print("Random Forest model trained successfully.")

# %% [notebook cell 134]
y_pred = rf_model.predict(X_test)

print("Predictions generated:", len(y_pred))

# %% [notebook cell 135]
forecast_results = ml_test[
    [
        "date",
        "Actual_Revenue"
    ]
].copy()

forecast_results["Predicted_Revenue"] = y_pred

display(forecast_results)

# %% [notebook cell 136]
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

mape = (
    np.mean(
        np.abs(
            (y_test - y_pred) / y_test
        )
    )
    * 100
)

print("ML Revenue Forecast Performance")
print("--------------------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2), "%")

# %% [notebook cell 137]
plt.figure(figsize=(12, 5))

plt.plot(
    forecast_results["date"],
    forecast_results["Actual_Revenue"],
    marker="o",
    label="Actual Revenue"
)

plt.plot(
    forecast_results["date"],
    forecast_results["Predicted_Revenue"],
    marker="o",
    label="ML Predicted Revenue"
)

plt.title("Company 1000 - Actual vs ML Predicted Revenue (2025)")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# %% [notebook cell 138]
feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    "Importance",
    ascending=False
)

display(feature_importance)

# %% [notebook cell 139]
plt.figure(figsize=(8, 5))

plt.bar(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.title("Random Forest Feature Importance")
plt.xlabel("Revenue Lag Feature")
plt.ylabel("Importance")

plt.tight_layout()
plt.show()

# %% [notebook cell 140]
rolling_forecast_2025 = actual_budget_forecast[
    (actual_budget_forecast["company_code"] == 1000) &
    (actual_budget_forecast["fiscal_year"] == 2025)
][
    [
        "fiscal_year",
        "fiscal_month",
        "Forecast_Revenue"
    ]
].copy()

display(rolling_forecast_2025)

# %% [notebook cell 141]
forecast_results["fiscal_year"] = forecast_results["date"].dt.year
forecast_results["fiscal_month"] = forecast_results["date"].dt.month

display(forecast_results.head())

# %% [notebook cell 142]
forecast_comparison = forecast_results.merge(
    rolling_forecast_2025,
    on=["fiscal_year", "fiscal_month"],
    how="inner"
)

forecast_comparison = forecast_comparison[
    [
        "date",
        "Actual_Revenue",
        "Forecast_Revenue",
        "Predicted_Revenue"
    ]
]

display(forecast_comparison)

# %% [notebook cell 143]
rolling_mape = (
    np.mean(
        np.abs(
            (
                forecast_comparison["Actual_Revenue"]
                - forecast_comparison["Forecast_Revenue"]
            )
            / forecast_comparison["Actual_Revenue"]
        )
    )
    * 100
)

print(
    "Rolling Forecast MAPE:",
    round(rolling_mape, 2),
    "%"
)

# %% [notebook cell 144]
ml_mape = (
    np.mean(
        np.abs(
            (
                forecast_comparison["Actual_Revenue"]
                - forecast_comparison["Predicted_Revenue"]
            )
            / forecast_comparison["Actual_Revenue"]
        )
    )
    * 100
)

print(
    "Random Forest MAPE:",
    round(ml_mape, 2),
    "%"
)

# %% [notebook cell 145]
forecast_method_comparison = pd.DataFrame({
    "Forecast_Method": [
        "Rolling Forecast",
        "Random Forest ML"
    ],
    "MAPE_%": [
        rolling_mape,
        ml_mape
    ]
})

forecast_method_comparison["MAPE_%"] = (
    forecast_method_comparison["MAPE_%"].round(2)
)

display(forecast_method_comparison)

# %% [notebook cell 146]
print(
    actuals_analysis["local_currency_amount"].describe()
)

# %% [notebook cell 147]
amount_percentiles = (
    actuals_analysis["local_currency_amount"]
    .quantile([0.50, 0.75, 0.90, 0.95, 0.99, 0.995, 0.999])
)

display(amount_percentiles)

# %% [notebook cell 148]
anomaly_data = actuals_analysis[
    ["company_code", "fiscal_year", "fiscal_month",
     "financial_category", "gl_account",
     "local_currency_amount", "currency"]
].copy()

print("Transactions available for anomaly detection:", len(anomaly_data))

display(anomaly_data.head())

# %% [notebook cell 149]
X_anomaly = anomaly_data[
    ["local_currency_amount"]
]

print("Anomaly model input shape:", X_anomaly.shape)

# %% [notebook cell 150]
from sklearn.ensemble import IsolationForest

isolation_forest = IsolationForest(
    n_estimators=200,
    contamination=0.01,
    random_state=42
)

isolation_forest.fit(X_anomaly)

print("Isolation Forest trained successfully.")

# %% [notebook cell 151]
anomaly_data["anomaly_label"] = isolation_forest.predict(
    X_anomaly
)

display(
    anomaly_data[
        ["local_currency_amount", "anomaly_label"]
    ].head(20)
)

# %% [notebook cell 152]
anomaly_counts = (
    anomaly_data["anomaly_label"]
    .value_counts()
)

print("Normal transactions:", anomaly_counts.get(1, 0))
print("Potential anomalies:", anomaly_counts.get(-1, 0))

# %% [notebook cell 153]
total_transactions = len(anomaly_data)

potential_anomalies = (
    anomaly_data["anomaly_label"] == -1
).sum()

anomaly_percentage = (
    potential_anomalies / total_transactions
) * 100

print(
    "Potential anomaly rate:",
    round(anomaly_percentage, 2),
    "%"
)

# %% [notebook cell 154]
potential_anomalies = anomaly_data[
    anomaly_data["anomaly_label"] == -1
].copy()

potential_anomalies = potential_anomalies.sort_values(
    "local_currency_amount",
    ascending=False
)

display(
    potential_anomalies.head(20)
)

# %% [notebook cell 155]
print("Total transactions:", len(anomaly_data))

print(
    "Potential anomalies:",
    (anomaly_data["anomaly_label"] == -1).sum()
)

print(
    "Anomaly percentage:",
    round(
        (anomaly_data["anomaly_label"] == -1).mean() * 100,
        2
    ),
    "%"
)

# %% [notebook cell 156]
anomaly_amount_summary = (
    potential_anomalies
    .groupby("currency")["local_currency_amount"]
    .agg(
        anomaly_transaction_count="count",
        total_flagged_amount="sum",
        average_flagged_amount="mean",
        maximum_flagged_amount="max"
    )
    .reset_index()
)

display(anomaly_amount_summary)

# %% [notebook cell 157]
anomaly_category_summary = (
    potential_anomalies
    .groupby(
        ["financial_category", "currency"]
    )["local_currency_amount"]
    .agg(
        transaction_count="count",
        total_amount="sum",
        average_amount="mean"
    )
    .reset_index()
    .sort_values(
        "total_amount",
        ascending=False
    )
)

display(anomaly_category_summary)

# %% [notebook cell 158]
anomaly_model_data = anomaly_data.copy()

anomaly_model_data["category_code"] = (
    anomaly_model_data["financial_category"]
    .astype("category")
    .cat.codes
)

anomaly_model_data["debit_credit_code"] = (
    actuals_analysis.loc[
        anomaly_model_data.index,
        "debit_credit"
    ]
    .astype("category")
    .cat.codes
)

print(
    anomaly_model_data[
        [
            "local_currency_amount",
            "category_code",
            "debit_credit_code"
        ]
    ].head(10)
)

# %% [notebook cell 159]
X_anomaly_context = anomaly_model_data[
    [
        "local_currency_amount",
        "category_code",
        "debit_credit_code"
    ]
]

print(
    "Context-aware anomaly input:",
    X_anomaly_context.shape
)

# %% [notebook cell 160]
context_isolation_forest = IsolationForest(
    n_estimators=200,
    contamination=0.01,
    random_state=42
)

context_isolation_forest.fit(X_anomaly_context)

print("Context-aware Isolation Forest trained successfully.")

# %% [notebook cell 161]
anomaly_model_data["context_anomaly_label"] = (
    context_isolation_forest.predict(
        X_anomaly_context
    )
)

display(
    anomaly_model_data[
        [
            "local_currency_amount",
            "category_code",
            "debit_credit_code",
            "context_anomaly_label"
        ]
    ].head(20)
)

# %% [notebook cell 162]
context_anomaly_count = (
    anomaly_model_data["context_anomaly_label"] == -1
).sum()

context_anomaly_rate = (
    context_anomaly_count
    / len(anomaly_model_data)
) * 100

print("Potential anomalies:", context_anomaly_count)
print(
    "Potential anomaly rate:",
    round(context_anomaly_rate, 2),
    "%"
)

# %% [notebook cell 163]
original_anomaly_count = (
    anomaly_data["anomaly_label"] == -1
).sum()

comparison = pd.DataFrame({
    "Model": [
        "Amount Only",
        "Amount + Category + Debit/Credit"
    ],
    "Potential_Anomalies": [
        original_anomaly_count,
        context_anomaly_count
    ]
})

comparison["Anomaly_Rate_%"] = (
    comparison["Potential_Anomalies"]
    / len(anomaly_data)
    * 100
)

comparison["Anomaly_Rate_%"] = (
    comparison["Anomaly_Rate_%"].round(2)
)

display(comparison)

# %% [notebook cell 164]
comparison_details = anomaly_model_data[
    anomaly_model_data["context_anomaly_label"]
    != anomaly_data["anomaly_label"]
].copy()

print(
    "Transactions with different anomaly classification:",
    len(comparison_details)
)

display(
    comparison_details[
        [
            "company_code",
            "fiscal_year",
            "fiscal_month",
            "financial_category",
            "local_currency_amount",
            "category_code",
            "debit_credit_code",
            "context_anomaly_label"
        ]
    ].head(20)
)

# %% [notebook cell 165]
anomaly_investigation = anomaly_model_data[
    anomaly_model_data["context_anomaly_label"] == -1
].copy()

anomaly_investigation = anomaly_investigation[
    [
        "company_code",
        "fiscal_year",
        "fiscal_month",
        "financial_category",
        "gl_account",
        "local_currency_amount",
        "currency",
        "debit_credit_code",
        "context_anomaly_label"
    ]
].copy()

anomaly_investigation = anomaly_investigation.sort_values(
    "local_currency_amount",
    ascending=False
)

print(
    "Potential anomalies for investigation:",
    len(anomaly_investigation)
)

display(anomaly_investigation.head(20))

# %% [notebook cell 166]
anomaly_category_summary = (
    anomaly_investigation
    .groupby(
        ["financial_category", "currency"]
    )
    .agg(
        anomaly_count=("local_currency_amount", "count"),
        total_anomaly_amount=("local_currency_amount", "sum"),
        average_anomaly_amount=("local_currency_amount", "mean")
    )
    .reset_index()
    .sort_values(
        "total_anomaly_amount",
        ascending=False
    )
)

display(anomaly_category_summary)

# %% [notebook cell 167]
category_transaction_counts = (
    actuals_analysis
    .groupby(
        ["financial_category", "currency"]
    )
    .size()
    .reset_index(name="total_transactions")
)

category_anomaly_rate = anomaly_category_summary.merge(
    category_transaction_counts,
    on=["financial_category", "currency"],
    how="left"
)

category_anomaly_rate["anomaly_rate_%"] = (
    category_anomaly_rate["anomaly_count"]
    / category_anomaly_rate["total_transactions"]
    * 100
)

category_anomaly_rate["anomaly_rate_%"] = (
    category_anomaly_rate["anomaly_rate_%"].round(2)
)

display(
    category_anomaly_rate.sort_values(
        "anomaly_rate_%",
        ascending=False
    )
)

# %% [notebook cell 168]
overall_anomaly_rate = (
    (anomaly_model_data["context_anomaly_label"] == -1).sum()
    / len(anomaly_model_data)
) * 100

print(
    "Overall Potential Anomaly Rate:",
    round(overall_anomaly_rate, 2),
    "%"
)

# %% [notebook cell 169]
final_kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Accounting Transactions",
        "Total Documents",
        "Document Reconciliation Rate",
        "Revenue Forecast MAPE",
        "ML Revenue Forecast MAPE",
        "Potential Financial Anomalies",
        "Overall Anomaly Rate"
    ],
    
    "Value": [
        len(actuals_analysis),
        len(document_balance),
        (
            (document_balance["balance_difference"].abs() < 0.01).mean()
            * 100
        ),
        revenue_mape,
        ml_mape,
        context_anomaly_count,
        overall_anomaly_rate
    ]
})

final_kpi_summary["Value"] = final_kpi_summary["Value"].round(2)

display(final_kpi_summary)

# %% [notebook cell 170]
business_insights = pd.DataFrame({
    "Metric": [
        "Best Revenue Forecast MAPE",
        "ML Forecast MAPE",
        "ML vs Revenue Forecast Improvement",
        "ML vs Rolling Forecast Difference",
        "Highest Revenue Anomaly Rate",
        "Overall Potential Anomaly Rate"
    ],
    
    "Value": [
        rolling_mape,
        ml_mape,
        revenue_mape - ml_mape,
        ml_mape - rolling_mape,
        category_anomaly_rate["anomaly_rate_%"].max(),
        overall_anomaly_rate
    ]
})

business_insights["Value"] = (
    business_insights["Value"].round(2)
)

display(business_insights)

# %% [notebook cell 171]
actual_budget_forecast.to_csv(
    "/kaggle/working/actual_budget_forecast.csv",
    index=False
)

print("Main FP&A dataset exported successfully.")

# %% [notebook cell 172]
import os

print(
    "File exists:",
    os.path.exists(
        "/kaggle/working/actual_budget_forecast.csv"
    )
)

# %% [notebook cell 173]
anomaly_investigation.to_csv(
    "/kaggle/working/anomaly_investigation.csv",
    index=False
)

print("Anomaly dataset exported successfully.")

# %% [notebook cell 174]
import os

print(
    "File exists:",
    os.path.exists(
        "/kaggle/working/anomaly_investigation.csv"
    )
)

# %% [notebook cell 175]
forecast_results.to_csv(
    "/kaggle/working/forecast_results.csv",
    index=False
)

print("ML forecast dataset exported successfully.")

# %% [notebook cell 176]
import os

print(
    "File exists:",
    os.path.exists(
        "/kaggle/working/forecast_results.csv"
    )
)

# %% [notebook cell 177]
final_kpi_summary.to_csv(
    "/kaggle/working/final_kpi_summary.csv",
    index=False
)

print("KPI summary exported successfully.")

# %% [notebook cell 178]
import os

print(
    "File exists:",
    os.path.exists(
        "/kaggle/working/final_kpi_summary.csv"
    )
)
