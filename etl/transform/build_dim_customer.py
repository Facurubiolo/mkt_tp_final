import pandas as pd
from pathlib import Path

def build_dim_customer(data: dict, output_path: Path) -> pd.DataFrame:
    df = data["customer"].copy()

    # surrogate key
    df.insert(0, "customer_sk", range(1, len(df) + 1))

    # columnas pedidas
    dim = df[[
        "customer_sk",
        "customer_id",
        "email",
        "first_name",
        "last_name",
        "phone",
        "status",
        "created_at"
    ]].drop_duplicates()

    path = Path(output_path) / "dim" / "dim_customer.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_customer guardado en {path}")
    return dim

