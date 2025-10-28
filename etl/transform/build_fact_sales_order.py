import pandas as pd
from pathlib import Path

def build_fact_sales_order(data: dict, output_path: Path) -> pd.DataFrame:
    so = data["sales_order"].copy()

    # date_id y hora
    so["order_date"] = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_id"] = so["order_date"].dt.strftime("%Y%m%d").astype("Int64")
    so["order_time"] = so["order_date"].dt.strftime("%H:%M:%S")

    fact = so[[
        "order_id",
        "customer_id",
        "channel_id",
        "store_id",
        "order_date_id",
        "order_time",
        "billing_address_id",
        "shipping_address_id",
        "status",
        "currency_code",
        "subtotal",
        "tax_amount",
        "shipping_fee",
        "total_amount"
    ]].rename(columns={"order_id": "id", "status": "status_order"})

    fact.insert(0, "sales_order_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_sales_order.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_sales_order guardado en {path}")
    return fact
