CATEGORY_RULES = {
    "Food": ["swiggy", "zomato", "restaurant", "dominos"],
    "Transport": ["uber", "ola", "rapido", "fuel", "petrol"],
    "Shopping": ["amazon", "flipkart", "myntra"],
    "Bills": ["electricity", "mobile", "recharge", "broadband"],
    "Income": ["salary", "interest", "refund"],
    "ATM": ["atm withdrawal"],
}
import pandas as pd

RULE_FILE = "./data/raw/processed/rules/merchant_categories.csv"
# \data\raw\processed\rules\merchant_categories.csv


def load_rules():
    print(f"Loading rules from: {RULE_FILE}");
    rules_df = pd.read_csv(RULE_FILE)

    rule_dict = dict(zip(rules_df["merchant"].str.strip(), rules_df["category"].str.strip()))
    print("Loaded rules:\n", rule_dict)
    return rule_dict

def detect_category(description: str) -> str:

    desc = description.lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in desc:
                return category

    return "Others"

def categorize_transactions(df):

    df["category"] = df["description"].apply(detect_category)

    return df

def export_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

def categorize_by_merchant(df):

    rules = load_rules()

    def get_category(merchant):

        merchant = merchant.lower()

        for key in rules:
            if key in merchant:
                return rules[key]

        return "Others"

    df["category"] = df["merchant"].apply(get_category)

    return df