import os
import pandas as pd


def _extract_name_from_field(field: str) -> str | None:
    """Extract the display name from fields like 'id@bank(Name Surname)'."""
    if not field or not isinstance(field, str):
        return None

    if "(" in field and ")" in field:
        start = field.find("(") + 1
        end = field.rfind(")")
        name = field[start:end].strip()
        if name:
            return name.lower()

    return None


def _parse_html_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]
    print(f"Found columns in HTML: {df.columns.tolist()}")

    required_columns = {
        "time",
        "bank name",
        "account number",
        "sender",
        "receiver",
        "payment id/reference number",
        "pay/collect",
        "amount (in rs.)",
        "dr/cr",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in HTML file: {missing}")

    clean_rows = []

    for _, row in df.iterrows():
        date_val = row.get("date") if "date" in row.index else None
        time_val = row.get("time")

        date_time_val = None
        if pd.notna(date_val) and pd.notna(time_val):
            date_time_val = f"{date_val} {time_val}"
        elif pd.notna(date_val):
            date_time_val = date_val
        elif pd.notna(time_val):
            date_time_val = time_val

        date_time = None
        if pd.notna(date_time_val):
            try:
                date_time = pd.to_datetime(date_time_val, dayfirst=True)
            except Exception:
                date_time = None

        dr_cr = str(row.get("dr/cr", "")).strip().upper()
        amount_raw = row.get("amount (in rs.)")

        if pd.isna(amount_raw) or not str(amount_raw).strip():
            continue

        try:
            amount = float(str(amount_raw).replace(",", ""))
        except Exception:
            continue

        txn_type = "credit" if "CR" in dr_cr else "debit"

        sender = str(row.get("sender", "")).strip()
        receiver = str(row.get("receiver", "")).strip()
        pay_collect = str(row.get("pay/collect", "")).strip()
        payment_ref = str(row.get("payment id/reference number", "")).strip()

        description = " | ".join(
            [x for x in [pay_collect, payment_ref, sender, receiver] if x]
        )

        merchant = None
        if txn_type == "debit":
            merchant = _extract_name_from_field(receiver) or receiver
        else:
            merchant = _extract_name_from_field(sender) or sender

        clean_rows.append({
            "date": date_time,
            "description": description,
            "amount": amount,
            "type": txn_type,
            "balance": None,
            "merchant": merchant,
        })

    return pd.DataFrame(clean_rows)


def parse_transactions(file_path: str) -> pd.DataFrame:
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in [".html", ".htm"]:
        tables = pd.read_html(file_path)
        if not tables:
            raise ValueError("No table found in HTML file")
        return _parse_html_transactions(tables[0])

    if ext not in [".xls", ".xlsx"]:
        raise ValueError(f"Unsupported file type: {ext}")

    df = pd.read_excel(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    print(f"Found columns in Excel: {df.columns.tolist()}")
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
    for _, row in df.iterrows():
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

    return pd.DataFrame(clean_rows)
        

  


# print(parse_transactions("PNB_Statement_Jan2026.xlsx"))