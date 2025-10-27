# etl/load/load.py

import pandas as pd
from pathlib import Path

from etl.extract.extract import extract_raw_data

from etl.transform.build_dim_customer import build_dim_customer
from etl.transform.dim_address import build_dim_address
from etl.transform.dim_product import build_dim_product
from etl.transform.dim_store import build_dim_store
from etl.transform.dim_channel import build_dim_channel
from etl.transform.dim_calendar import build_dim_calendar

from etl.transform.fact_sales_order import build_fact_sales_order
from etl.transform.fact_sales_order_item import build_fact_sales_order_item
from etl.transform.fact_payment import build_fact_payment
from etl.transform.fact_shipment import build_fact_shipment
from etl.transform.fact_nps_response import build_fact_nps_response
from etl.transform.fact_web_session import build_fact_web_session


# Directorio base
ROOT = Path(__file__).resolve().parents[2]

# Directorios del Data Warehouse
DW_DIR = ROOT / "warehouse"
DIM_DIR = DW_DIR / "dim"
FACT_DIR = DW_DIR / "fact"

# Crear carpetas si no existen
DIM_DIR.mkdir(parents=True, exist_ok=True)
FACT_DIR.mkdir(parents=True, exist_ok=True)


def save_dim(df: pd.DataFrame, name: str) -> Path:
    path = DIM_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"📁 DIM guardada: {path}")
    return path


def save_fact(df: pd.DataFrame, name: str) -> Path:
    path = FACT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"📦 FACT guardada: {path}")
    return path


def run_pipeline():
    print("\n🚀 Iniciando Pipeline ETL...")

    # 1) EXTRACT
    raw = extract_raw_data()

    # 2) TRANSFORM - DIM
    dim_customer = build_dim_customer(raw)
    dim_address = build_dim_address(raw)
    dim_product = build_dim_product(raw)
    dim_store = build_dim_store(raw)
    dim_channel = build_dim_channel(raw)
    dim_calendar = build_dim_calendar(raw)

    # 3) LOAD - DIM
    save_dim(dim_customer, "dim_customer")
    save_dim(dim_address, "dim_address")
    save_dim(dim_product, "dim_product")
    save_dim(dim_store, "dim_store")
    save_dim(dim_channel, "dim_channel")
    save_dim(dim_calendar, "dim_calendar")

    # 4) TRANSFORM - FACT
    fact_sales_order = build_fact_sales_order(raw, dim_calendar)
    fact_sales_order_item = build_fact_sales_order_item(raw)
    fact_payment = build_fact_payment(raw, dim_calendar)
    fact_shipment = build_fact_shipment(raw, dim_calendar)
    fact_nps_response = build_fact_nps_response(raw, dim_calendar)
    fact_web_session = build_fact_web_session(raw, dim_calendar)

    # 5) LOAD - FACT
    save_fact(fact_sales_order, "fact_sales_order")
    save_fact(fact_sales_order_item, "fact_sales_order_item")
    save_fact(fact_payment, "fact_payment")
    save_fact(fact_shipment, "fact_shipment")
    save_fact(fact_nps_response, "fact_nps_response")
    save_fact(fact_web_session, "fact_web_session")

    print("\n✅ Pipeline completada con éxito!")


# Permite ejecutar este archivo directamente
if __name__ == "__main__":
    run_pipeline()
