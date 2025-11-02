import pandas as pd
from pathlib import Path

def build_fact_payment(data: dict, output_path: Path) -> pd.DataFrame:
    pay = data["payment"].copy()
    so = data["sales_order"][["order_id","customer_id","billing_address_id","channel_id","store_id"]].copy()

    # traigo datos de cabecera
    pay = pay.merge(so, how="left", on="order_id")

    # date_id y hora del pago
    pay["paid_at"] = pd.to_datetime(pay["paid_at"], errors="coerce")
    pay["paid_at_date_id"] = pay["paid_at"].dt.strftime("%Y%m%d").astype("Int64")
    pay["paid_at_time"] = pay["paid_at"].dt.strftime("%H:%M:%S")
    pay['billing_address_id'] = pay['billing_address_id'].astype('Int64')
    fact = pay[[
        "payment_id",
        "customer_id",
        "billing_address_id",
        "channel_id",
        "store_id",
        "method",
        "status",
        "amount",
        "paid_at_date_id",
        "paid_at_time",
        "transaction_ref"
    ]].rename(columns={"payment_id": "id", "status": "status_payment"})

    fact.insert(0, "payment_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_payment.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_payment guardado en {path}")
    return fact
