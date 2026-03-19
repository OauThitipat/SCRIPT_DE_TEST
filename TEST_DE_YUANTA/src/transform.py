import pandas as pd

def clean_nulls(df):
    """
    แปลง empty string / space → NULL
    """
    return df.replace(r'^\s*$', pd.NA, regex=True)


def clean_strings(df):
    df.columns = df.columns.str.strip().str.lower()

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    return df


def enforce_pk(df, pk_col):
    df = df.dropna(subset=[pk_col])
    df = df.drop_duplicates(subset=[pk_col], keep="last")

    if df[pk_col].duplicated().any():
        raise ValueError(f"Duplicate {pk_col}!")

    return df


def transform_clients(df):
    df = clean_strings(df)
    df = clean_nulls(df)

    df = enforce_pk(df, "client_id")

    return df


def transform_instruments(df):
    df = clean_strings(df)
    df = clean_nulls(df)

    df = enforce_pk(df, "instrument_id")

    return df


def transform_trades(df, clients, instruments):
        # ---------------------
    # clean strings + null
    # ---------------------
    df = clean_strings(df)
    df = clean_nulls(df)

    # ---------------------
    # normalize case
    # ---------------------
    df["side"] = df["side"].str.upper()
    df["status"] = df["status"].str.upper()

    # ---------------------
    # PK enforcement
    # ---------------------
    df = enforce_pk(df, "trade_id")

    # ---------------------
    # numeric columns
    # ---------------------
    for col in ["quantity", "price", "fees"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")  # invalid → NaN

    # ---------------------
    # datetime columns
    # ---------------------
    for dt_col in ["trade_time", "created_at"] if "created_at" in df.columns else ["trade_time"]:
        df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce", utc=True)
        df[dt_col] = df[dt_col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # ---------------------
    # FK validation
    # ---------------------
    df = df[df["client_id"].isin(clients["client_id"])]
    df = df[df["instrument_id"].isin(instruments["instrument_id"])]

    # ---------------------
    # business rules - ไม่ drop row
    # ---------------------
    # ลบ filter quantity/price/side เดิมออกทั้งหมด
    # เก็บ row แม้ว่า quantity=0 หรือ side ผิด

    # ---------------------
    # final duplicate check
    # ---------------------
    if df["trade_id"].duplicated().any():
        raise ValueError("Duplicate trade_id after cleaning!")

    print(f"After cleaning: {len(df)}")
    print(f"Missing fees: {df['fees'].isna().sum()}")

    return df