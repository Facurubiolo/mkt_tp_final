import pandas as pd
from pathlib import Path

def build_fact_sales_order_item(data: dict, output_path: Path) -> pd.DataFrame:
    it = data["sales_order_item"].copy()
    so = data["sales_order"][["order_id", "customer_id", "channel_id", "store_id"]].copy()

    # traigo customer/channel/store desde cabecera
    it = it.merge(so, how="left", on="order_id")

    fact = it[[
        "order_item_id",
        "customer_id",
        "channel_id",
        "store_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_amount",
        "line_total"
    ]].rename(columns={"order_item_id": "id"})

    fact.insert(0, "sales_order_item_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_sales_order_item.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_sales_order_item guardado en {path}")
    return fact
