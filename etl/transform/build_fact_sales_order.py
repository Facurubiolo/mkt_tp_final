import pandas as pd
from pathlib import Path

def build_fact_sales_order(data: dict, output_path: Path) -> pd.DataFrame:
    # agarro la tabla cruda de sales_order

    so = data["sales_order"].copy()
    
    # Leo dim address para mapear los IDs a surrogate keys
    dim_address = pd.read_csv(Path(output_path) / "dim" / "dim_address.csv")
    
    # Proceso las fechas 
    so["order_date"] = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_id"] = so["order_date"].dt.strftime("%Y%m%d").astype("Int64")
    so["order_time"] = so["order_date"].dt.strftime("%H:%M:%S")
    so["order_date"] = so["order_date"].dt.strftime("%Y-%m-%d")
    
    # normalizo el tipo del billing_address_id (por si venía como texto) no termino haciendo falta
    so["billing_address_id"] = pd.to_numeric(so["billing_address_id"], errors="coerce").astype("Int64")
    
     # hago el merge para reemplazar el id natural de address por el surrogate key (address_sk)
    # left_on = lo que tengo en la fact (billing_address_id de RAW)
    # right_on = la clave natural en la dimensión (address_id)
    so = so.merge(
        dim_address[["address_id", "address_sk"]],
        left_on="billing_address_id",
        right_on="address_id",
        how="left"
        
        # renombro la sk como ID
    ).drop("billing_address_id", axis=1).rename(columns={"address_sk": "billing_address_id"})
    

    so['billing_address_id'] = so['billing_address_id'].astype('Int64')

    fact = so[[
        "order_id",
        "customer_id",
        "channel_id",
        "store_id",
        "order_date_id",
        "order_time",
        "order_date",
        "billing_address_id",
        "shipping_address_id",
        "status",
        "currency_code",
        "subtotal",
        "tax_amount",
        "shipping_fee",
        "total_amount"
    ]].rename(columns={"order_id": "id", "status": "status_order"})

    fact["store_id"] = pd.to_numeric(fact["store_id"], errors="coerce").astype("Int64")
    # creo la surrogate key propia de la fact
    fact.insert(0, "sales_order_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_sales_order.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_sales_order guardado en {path}")
    return fact
