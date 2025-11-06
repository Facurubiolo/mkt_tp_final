import pandas as pd
from pathlib import Path

def build_fact_sales_order_item(data: dict, output_path: Path) -> pd.DataFrame:
    it = data["sales_order_item"].copy()
    so = data["sales_order"][[
        "order_id", "customer_id", "channel_id", "store_id", "order_date",
        "billing_address_id", "shipping_address_id"
    ]].copy()
    
    # Leer dim_address para mapear los IDs a surrogate keys
    dim_address = pd.read_csv(Path(output_path) / "dim" / "dim_address.csv")
    
    # Procesar billing_address_id
    so["billing_address_id"] = pd.to_numeric(so["billing_address_id"], errors="coerce").astype("Int64")
    so = so.merge(
        dim_address[["address_id", "address_sk"]],
        left_on="billing_address_id",
        right_on="address_id",
        how="left"
    ).drop("billing_address_id", axis=1).rename(columns={"address_sk": "billing_address_id"})
    
    # Procesar shipping_address_id
    so["shipping_address_id"] = pd.to_numeric(so["shipping_address_id"], errors="coerce").astype("Int64")
    so = so.merge(
        dim_address[["address_id", "address_sk"]],
        left_on="shipping_address_id",
        right_on="address_id",
        how="left"
    ).drop("shipping_address_id", axis=1).rename(columns={"address_sk": "shipping_address_id"})
    
    # Convertir a Int64 nullable
    so['billing_address_id'] = so['billing_address_id'].astype('Int64')
    so['shipping_address_id'] = so['shipping_address_id'].astype('Int64')
    
    # Procesar fechas
    so["order_date"] = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_id"] = so["order_date"].dt.strftime("%Y%m%d").astype("Int64")
    so["order_date"] = so["order_date"].dt.strftime("%Y-%m-%d")

    
    # traigo customer/channel/store y fecha desde cabecera
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
        "line_total",
        "order_date_id",
        "order_date",
        "billing_address_id",
        "shipping_address_id"
    ]].rename(columns={"order_item_id": "id"})

    fact.insert(0, "sales_order_item_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_sales_order_item.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_sales_order_item guardado en {path}")
    return fact
