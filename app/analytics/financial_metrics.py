import pandas as pd


def calculate_basic_metrics(df):

    income = float(df[df["type"] == "credit"]["amount"].sum())
    expenses = float(df[df["type"] == "debit"]["amount"].sum())

    savings = income - expenses

    return {
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "net_savings": round(savings, 2)
    }

def category_summary(df):

    summary = df[df["type"] == "debit"].groupby("category")["amount"].sum()

    return summary.sort_values(ascending=False)

def top_spending_category(df):

    summary = df[df["type"] == "debit"].groupby("category")["amount"].sum()

    return summary.idxmax()

def average_daily_spend(df):

    expenses = df[df["type"] == "debit"]

    daily = expenses.groupby(df["date"].dt.date)["amount"].sum()

    return daily.mean()

def calculate_weekly_spending(df):

    # filter only expenses
    expenses = df[df["type"] == "debit"].copy()

    # safely convert dates
    expenses["date"] = pd.to_datetime(expenses["date"], errors="coerce")

    # remove rows where date conversion failed
    expenses = expenses.dropna(subset=["date"])

    # extract ISO year and week number (handles Dec 31st correctly)
    expenses["iso_year"] = expenses["date"].dt.isocalendar().year
    expenses["week"] = expenses["date"].dt.isocalendar().week
    print("Expenses with week number:\n", expenses[["date", "amount", "iso_year", "week"]])

    # sum spending per week (grouped by both year and week)
    weekly = (
        expenses.groupby(["iso_year", "week"])["amount"]
        .sum()
        .reset_index()
        .rename(columns={"iso_year": "year"})
    )

    return weekly