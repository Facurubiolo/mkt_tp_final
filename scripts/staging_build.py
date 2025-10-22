from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "RAW"
STG = BASE / "staging"
STG.mkdir(exist_ok=True)

def to_dt(s):
    return pd.to_datetime(s, errors="coerce")

def save(df, name):
    out = STG / name
    df.to_csv(out, index=False)
    print(f"[STAGING] → {out.name} ({df.shape[0]} filas)")

# --- Cargar RAW ---
channel  = pd.read_csv(RAW/"channel.csv")
province = pd.read_csv(RAW/"province.csv")
category = pd.read_csv(RAW/"product_category.csv")
customer = pd.read_csv(RAW/"customer.csv")
address  = pd.read_csv(RAW/"address.csv")
store    = pd.read_csv(RAW/"store.csv")
product  = pd.read_csv(RAW/"product.csv")
order    = pd.read_csv(RAW/"sales_order.csv")
item     = pd.read_csv(RAW/"sales_order_item.csv")
payment  = pd.read_csv(RAW/"payment.csv")
ship     = pd.read_csv(RAW/"shipment.csv")
session  = pd.read_csv(RAW/"web_session.csv")
nps      = pd.read_csv(RAW/"nps_response.csv")

# --- Tipos de fecha para tablas principales ---
for c in ["created_at"]:
    if c in product.columns:  product[c] = to_dt(product[c])
    if c in address.columns:  address[c] = to_dt(address[c])
    if c in customer.columns: customer[c] = to_dt(customer[c])

order["order_date"] = to_dt(order["order_date"])
payment["paid_at"]  = to_dt(payment.get("paid_at"))
ship["shipped_at"]  = to_dt(ship.get("shipped_at"))
ship["delivered_at"]= to_dt(ship.get("delivered_at"))
session["started_at"]=to_dt(session.get("started_at"))
if "ended_at" in session.columns:
    session["ended_at"] = to_dt(session["ended_at"])
nps["responded_at"] = to_dt(nps["responded_at"])

# --- STG: product + category ---
stg_product = product.merge(
    category.rename(columns={"name":"category_name","parent_id":"parent_category_id"}),
    on="category_id", how="left"
).rename(columns={"name":"product_name"})
save(stg_product, "stg_product.csv")

# --- STG: address + province ---
stg_address = address.merge(
    province.rename(columns={"name":"province_name","code":"province_code"}),
    on="province_id", how="left"
)
save(stg_address, "stg_address.csv")

# --- STG: store + address(+province) ---
stg_store = store.merge(
    stg_address[["address_id","province_id","province_name","province_code"]],
    on="address_id", how="left"
).rename(columns={"name":"store_name"})
save(stg_store, "stg_store.csv")

# --- STG: sales_order + provincia de envío derivada ---
stg_sales_order = order.merge(
    stg_address[["address_id","province_id"]].rename(columns={"address_id":"shipping_address_id"}),
    on="shipping_address_id", how="left"
).rename(columns={"province_id":"shipping_province_id"})
save(stg_sales_order, "stg_sales_order.csv")

# --- STG: sales_order_item + order_date (para calendarizar ítems) ---
stg_sales_order_item = item.merge(
    order[["order_id","order_date"]], on="order_id", how="left"
)
save(stg_sales_order_item, "stg_sales_order_item.csv")

# --- STG: payment (tal cual + limpieza mínima) ---
stg_payment = payment.copy()
save(stg_payment, "stg_payment.csv")

# --- STG: shipment + delivery_days ---
stg_shipment = ship.copy()
stg_shipment["delivery_days"] = (stg_shipment["delivered_at"] - stg_shipment["shipped_at"]).dt.days
save(stg_shipment, "stg_shipment.csv")

# --- STG: web_session (usuarios activos) ---
stg_web_session = session.copy()
save(stg_web_session, "stg_web_session.csv")

# --- STG: nps_response (NPS) ---
stg_nps_response = nps.copy()
save(stg_nps_response, "stg_nps_response.csv")

print("OK: STAGING generado.")
