# etl/transform/dim_customer.py
import pandas as pd

def build_dim_customer(raw: dict) -> pd.DataFrame:
    """
    Construye la dimensión de clientes.
    Columnas finales:
    customer_id, first_name, last_name, email, phone, status, created_at
    """
    df = raw["customer"].copy()

    dim = df[[
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "status",
        "created_at"
    ]].drop_duplicates()

    return dim
