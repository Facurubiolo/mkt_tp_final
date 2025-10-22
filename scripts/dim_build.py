from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "RAW"
STG = BASE / "staging"
DW  = BASE / "DW"
DW.mkdir(exist_ok=True)

def save(df, name):
    out = DW / name
    df.to_csv(out, index=False)
    print(f"[DW] DIM → {out.name} ({df.shape[0]} filas)")

def date_id(s):
    s = pd.to_datetime(s, errors="coerce")
    return pd.to_numeric(s.dt.strftime("%Y%m%d"), errors="coerce")

dim_channel = pd.read_csv(RAW/"channel.csv").rename(
    columns={"code":"channel_code","name":"channel_name"}
)
save(dim_channel, "dim_channel.csv")

dim_province = pd.read_csv(RAW/"province.csv").rename(
    columns={"name":"province_name","code":"province_code"}
)
save(dim_province, "dim_province.csv")

dim_customer = pd.read_csv(RAW/"customer.csv")
save(dim_customer, "dim_customer.csv")

dim_product = pd.read_csv(STG/"stg_product.csv")
save(dim_product, "dim_product.csv")

dim_store = pd.read_csv(STG/"stg_store.csv")
save(dim_store, "dim_store.csv")

addr_path = STG / "stg_address.csv"
if addr_path.exists():
    addr = pd.read_csv(addr_path)
    addr = addr.rename(columns={
        "id": "address_id",
        "customer_id": "customer_id",
        "province_code": "province_code",
        "street": "street",
        "number": "number",
        "floor": "floor",
        "apartment": "apartment",
        "postal_code": "postal_code",
    })
    keep_cols = [c for c in ["address_id","customer_id","province_code","street","number","floor","apartment","postal_code"] if c in addr.columns]
    dim_address = addr[keep_cols].drop_duplicates().reset_index(drop=True)
    if "address_id" in dim_address.columns:
        dim_address["address_id"] = pd.to_numeric(dim_address["address_id"], errors="coerce").astype('Int64')
    save(dim_address, "dim_address.csv")
else:
    print("[DW] WARNING: stg_address.csv no encontrado en staging, omitiendo dim_address")

so  = pd.read_csv(STG/"stg_sales_order.csv")[["order_date"]].rename(columns={"order_date":"dt"})
shp = pd.read_csv(STG/"stg_shipment.csv")[["shipped_at","delivered_at"]].melt(value_name="dt")["dt"]
ws  = pd.read_csv(STG/"stg_web_session.csv")[["started_at"]]
if "ended_at" in pd.read_csv(STG/"stg_web_session.csv").columns:
    ws = pd.read_csv(STG/"stg_web_session.csv")[["started_at","ended_at"]].melt(value_name="dt")[["dt"]]
else:
    ws = pd.read_csv(STG/"stg_web_session.csv")[["started_at"]].rename(columns={"started_at":"dt"})
nps = pd.read_csv(STG/"stg_nps_response.csv")[["responded_at"]].rename(columns={"responded_at":"dt"})

cal = pd.concat([so["dt"], pd.Series(shp), ws["dt"], nps["dt"]], ignore_index=True)
cal = pd.to_datetime(cal, errors="coerce").dropna().drop_duplicates().sort_values()

dim_date = pd.DataFrame({"date": cal.dt.date})
dim_date["date_id"] = date_id(dim_date["date"])
dt = pd.to_datetime(dim_date["date"])
dim_date["year"]       = dt.dt.year
dim_date["month"]      = dt.dt.month
dim_date["day"]        = dt.dt.day
dim_date["year_month"] = dt.dt.strftime("%Y-%m")
save(dim_date[["date_id","date","year","month","day","year_month"]], "dim_date.csv")

print("OK: DIMs generadas.")
