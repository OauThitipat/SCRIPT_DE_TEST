import os
import pandas as pd
from transform import (
    transform_clients,
    transform_instruments,
    transform_trades
)


INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

os.makedirs(OUTPUT_PATH, exist_ok=True)


def get_base_name(filename: str) -> str:
    """
    clients.csv -> clients
    trades_2026-03-09.csv -> trades
    """
    return filename.replace(".csv", "").split("_")[0]



clients_clean = None
instruments_clean = None

files = os.listdir(INPUT_PATH)



for file in files:
    if not file.endswith(".csv"):
        continue

    base_name = get_base_name(file)
    file_path = os.path.join(INPUT_PATH, file)

    if base_name == "clients":
        print(f"\n📂 Processing: {file}")

        df = pd.read_csv(file_path)
        clients_clean = transform_clients(df)

        output_path = os.path.join(OUTPUT_PATH, file)
        clients_clean.to_csv(output_path, index=False)

        print(f"✅ Saved → {output_path}")

    elif base_name == "instruments":
        print(f"\n📂 Processing: {file}")

        df = pd.read_csv(file_path)
        instruments_clean = transform_instruments(df)

        output_path = os.path.join(OUTPUT_PATH, file)
        instruments_clean.to_csv(output_path, index=False)

        print(f"✅ Saved → {output_path}")



if clients_clean is None:
    raise ValueError("❌ clients file not found")

if instruments_clean is None:
    raise ValueError("❌ instruments file not found")





for file in files:
    if not file.endswith(".csv"):
        continue

    base_name = get_base_name(file)
    file_path = os.path.join(INPUT_PATH, file)

    if base_name == "trades":
        print(f"\n📂 Processing: {file}")

        df = pd.read_csv(file_path)

        trades_clean = transform_trades(
            df,
            clients_clean,
            instruments_clean
        )

        output_path = os.path.join(OUTPUT_PATH, file)
        trades_clean.to_csv(output_path, index=False)

        print(f"✅ Saved → {output_path}")

