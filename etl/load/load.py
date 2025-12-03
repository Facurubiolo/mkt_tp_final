# etl/load/load.py
import pandas as pd
from pathlib import Path

# EXTRACT
from etl.extract.extract import extract_raw_data

# DIMs 
from etl.transform.build_dim_customer import build_dim_customer
from etl.transform.build_dim_address import build_dim_address
from etl.transform.build_dim_product import build_dim_product
from etl.transform.build_dim_store import build_dim_store
from etl.transform.build_dim_channel import build_dim_channel
from etl.transform.build_dim_calendar import build_dim_calendar

# FACTs 
from etl.transform.build_fact_sales_order import build_fact_sales_order
from etl.transform.build_fact_sales_order_item import build_fact_sales_order_item
from etl.transform.build_fact_payment import build_fact_payment
from etl.transform.build_fact_shipment import build_fact_shipment
from etl.transform.build_fact_web_session import build_fact_web_session
from etl.transform.build_fact_nps_response import build_fact_nps_response



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

    # Salida del DW
    output_path = Path("warehouse")

    # 2) DIMENSIONES (cada build guarda su CSV en warehouse/dim)
    build_dim_customer(raw, output_path)
    build_dim_address(raw, output_path)
    build_dim_product(raw, output_path)
    build_dim_store(raw, output_path)
    build_dim_channel(raw, output_path)
    build_dim_calendar(raw, output_path)

    # 3) FACTS (cada build guarda su CSV en warehouse/fact)
    build_fact_sales_order(raw, output_path)
    build_fact_sales_order_item(raw, output_path)
    build_fact_payment(raw, output_path)
    build_fact_shipment(raw, output_path)
    build_fact_web_session(raw, output_path)
    build_fact_nps_response(raw, output_path)

    print("\n✅ Pipeline completada con éxito!")

# Permite ejecutar este archivo directamente
if __name__ == "__main__":
    run_pipeline()
# agrego comentario