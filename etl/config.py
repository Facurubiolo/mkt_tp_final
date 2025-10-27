# etl/config.py
from pathlib import Path

# === Rutas absolutas, partiendo de este archivo ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # .../MKT_TP_FINAL
RAW_DIR      = PROJECT_ROOT / "raw"                   # <-- tu carpeta real
WH_DIM_DIR   = PROJECT_ROOT / "warehouse" / "dim"
WH_FACT_DIR  = PROJECT_ROOT / "warehouse" / "fact"

WH_DIM_DIR.mkdir(parents=True, exist_ok=True)
WH_FACT_DIR.mkdir(parents=True, exist_ok=True)

# Mapea nombres lógicos → archivo en raw/
RAW = {
    "address":          "address.csv",
    "province":         "province.csv",
    "store":            "store.csv",
    "channel":          "channel.csv",
    "customer":         "customer.csv",
    "product":          "product.csv",
    "product_category": "product_category.csv",
    "sales_order":      "sales_order.csv",
    "sales_order_item": "sales_order_item.csv",
    "payment":          "payment.csv",
    "shipment":         "shipment.csv",
    "web_session":      "web_session.csv",
    "nps_response":     "nps_response.csv",
}

# Nombres de salida
DIM_OUT = {
    "address":  "dim_address.csv",
    "calendar": "dim_calendar.csv",
    "channel":  "dim_channel.csv",
    "customers":"dim_customers.csv",
    "products": "dim_products.csv",
    "store":    "dim_store.csv",
}

FACT_OUT = {
    "nps_response":      "fact_nps_response.csv",
    "payment":           "fact_payment.csv",
    "sales_order":       "fact_sales_order.csv",
    "sales_order_item":  "fact_sales_order_item.csv",
    "shipment":          "fact_shipment.csv",
    "web_session":       "fact_web_session.csv",
}
