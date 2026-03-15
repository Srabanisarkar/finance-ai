import pandas as pd

def parse_transactions(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    required_columns = {
    "txn date",
    "description",
    "dr amount",
    "cr amount",
    "balance"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    clean_rows = []
    for idx, row in df.iterrows():
        txn_date = row["txn date"]
        desc = row["description"]
        dr = row["dr amount"]
        cr = row["cr amount"]
        balance = row["balance"]

        
        if pd.notna(dr):
            amount = dr
            txn_type = "debit"
        elif pd.notna(cr):
            amount = cr
            txn_type = "credit"
        else:
            continue  # skip empty rows

        try:
            txn_date = pd.to_datetime(txn_date, dayfirst=True)
        except Exception:
            continue

        clean_rows.append({
        "date": txn_date,
        "description": str(desc).strip(),
        "amount": float(amount),
        "type": txn_type,
        "balance": balance
        })

    clean_df = pd.DataFrame(clean_rows)
    return clean_df
        

  


# print(parse_transactions("PNB_Statement_Jan2026.xlsx"))