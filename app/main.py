import os

from parser.transaction_parser import parse_transactions
from categorizer.transaction_categorizer import categorize_by_merchant ,export_to_csv
from analytics.financial_metrics import calculate_basic_metrics, calculate_weekly_spending, category_summary, top_spending_category, average_daily_spend
from reporter.excel_report import generate_excel_report
from extractor.financial_extractor import  extract_merchant
from utils.transaction_id import generate_transaction_id
from analytics.financial_health import (
    calculate_financial_metrics,
    category_spending,
    financial_health_score
)
from ai.financial_advisor import generate_ai_advice

OUTPUT_FILE = "categorized_transactions.csv"

print("Choose input file type:")
print("1. HTML")
print("2. CSV (Excel)")
choice = input("Enter 1 for HTML or 2 for CSV: ").strip()
if choice == '1':
    file_path = "statement.html"
elif choice == '2':
    file_path = "PNB_Statement_Jan2026.xlsx"
else:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found in the current directory.")
    exit()

df = parse_transactions(file_path)

df["merchant"] = df["description"].apply(extract_merchant)
df["transaction_id"] = df.apply(generate_transaction_id, axis=1)


deaaa = categorize_by_merchant(df)

export_to_csv(deaaa, OUTPUT_FILE)

# print("\nCategory Summary:")
# print(df.groupby("category")["amount"].sum())

# print("Transactions processed successfully")
# print(f"CSV saved to: {OUTPUT_FILE}")


metrics = calculate_basic_metrics(df)

# print("\nFinancial Summary")
# print(f"Total Income   : ₹{metrics['total_income']}")
# print(f"Total Expenses : ₹{metrics['total_expenses']}")
# print(f"Net Savings    : ₹{metrics['net_savings']}")

# print("\nCategory Spending")
# print(category_summary(df))

# print("\nTop Spending Category")
# print(top_spending_category(df))

# print("\nAverage Daily Spend")
# print(average_daily_spend(df))

metrics = calculate_financial_metrics(df)

categories = category_spending(df)

# score = financial_health_score(metrics)

# print("Financial Metrics:", metrics)

# print("Category Spending:", categories)

# print("Financial Health Score:", score)
ai_advice=generate_ai_advice(metrics, categories)
# print("\nAI Financial Advice:")
# print(ai_advice)

REPORT_FILE = "financial_report.xlsx"
df = df[
    [
        "transaction_id",
        "date",
        "description",
        "merchant",
        "amount",
        "type",
        "balance",
        "category"
    ]
]
weekly_spending = calculate_weekly_spending(df)
# print(weekly_spending)

generate_excel_report(
    df,
    metrics,
    categories,
    ai_advice,
    weekly_spending
)


print("\nExcel report generated:")
# print(REPORT_FILE)