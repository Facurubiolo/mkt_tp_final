# etl/extract/extract.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "raw"



def load_csv(filename: str) -> pd.DataFrame:
    """Carga un CSV desde RAW_PATH y lo devuelve como DataFrame."""
    file_path = RAW_PATH / filename
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró {file_path}. Verificá la ruta y el nombre del archivo.")
    return pd.read_csv(file_path)


def extract_raw_data() -> dict:
    """Carga todas las tablas raw y devuelve un diccionario {nombre: DataFrame}."""
    data = {
        # catálogos y maestros
        "address": load_csv("address.csv"),
        "channel": load_csv("channel.csv"),
        "customer": load_csv("customer.csv"),
        "product_category": load_csv("product_category.csv"),
        "product": load_csv("product.csv"),
        "province": load_csv("province.csv"),
        "store": load_csv("store.csv"),
        # transaccionales
        "sales_order": load_csv("sales_order.csv"),
        "sales_order_item": load_csv("sales_order_item.csv"),
        "payment": load_csv("payment.csv"),
        "shipment": load_csv("shipment.csv"),
        # digital y encuestas
        "web_session": load_csv("web_session.csv"),
        "nps_response": load_csv("nps_response.csv"),
    }
    return data



if __name__ == "__main__":
    dfs = extract_raw_data()

    for name, df in dfs.items():
        print(f"{name}: {df.shape[0]} filas, {df.shape[1]} columnas")
