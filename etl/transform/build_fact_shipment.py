import pandas as pd
from pathlib import Path

def build_fact_shipment(data: dict, output_path: Path) -> pd.DataFrame:
    shp = data["shipment"].copy()
    so  = data["sales_order"][["order_id","customer_id","shipping_address_id","channel_id"]].copy()

    # traigo datos de cabecera
    shp = shp.merge(so, how="left", on="order_id")

    # fechas y horas
    shp["shipped_at"]   = pd.to_datetime(shp["shipped_at"], errors="coerce")
    shp["delivered_at"] = pd.to_datetime(shp["delivered_at"], errors="coerce")

    shp["shipped_at_date_id"]   = shp["shipped_at"].dt.strftime("%Y%m%d").astype("Int64")
    shp["shipped_at_time"]      = shp["shipped_at"].dt.strftime("%H:%M:%S")
    shp["delivered_at_date_id"] = shp["delivered_at"].dt.strftime("%Y%m%d").astype("Int64")
    shp["delivered_at_time"]    = shp["delivered_at"].dt.strftime("%H:%M:%S")

    fact = shp[[
        "shipment_id",
        "customer_id",
        "shipping_address_id",
        "channel_id",
        "carrier",
        "shipped_at_date_id",
        "shipped_at_time",
        "delivered_at_date_id",
        "delivered_at_time",
        "tracking_number"
    ]].rename(columns={"shipment_id": "id"})

    fact.insert(0, "shipment_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_shipment.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_shipment guardado en {path}")
    return fact
