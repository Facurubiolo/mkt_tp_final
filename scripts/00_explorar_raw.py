import os
import pandas as pd
from pathlib import Path

# Definimos la ruta base y la carpeta RAW
BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "RAW"

# Verificamos que exista la carpeta RAW
assert RAW.exists(), f"No se encuentra la carpeta RAW en {RAW}"

# Listamos todos los CSV
csvs = sorted(p for p in RAW.glob("*.csv"))
print("\n== CSV encontrados en RAW ==")
for p in csvs:
    print(" -", p.name)
print()

# Función para leer y mostrar información de cada CSV
def ver_csv(nombre):
    p = RAW / nombre
    if not p.exists():
        print(f"[ADVERTENCIA] No está {nombre} en RAW/")
        return
    df = pd.read_csv(p)
    print(f"--- {nombre} ---")
    print("Shape (filas, columnas):", df.shape)
    print("Columnas:", list(df.columns))
    print(df.head(3))  # muestra las primeras 3 filas
    print()

# Listado de los archivos que se esperan encontrar
candidatos = [
    "channel.csv",
    "province.csv",
    "product_category.csv",
    "customer.csv",
    "address.csv",
    "store.csv",
    "product.csv",
    "sales_order.csv",
    "sales_order_item.csv",
    "payment.csv",
    "shipment.csv",
    "web_session.csv",
    "nps_response.csv",
]

# Mostramos cada uno
for nombre in candidatos:
    ver_csv(nombre)
