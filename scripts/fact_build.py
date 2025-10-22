from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
STG = BASE / "staging"
DW  = BASE / "DW"
DW.mkdir(exist_ok=True)

def save(df, name):
    out = DW / name
    df.to_csv(out, index=False)
    print(f"[DW] FACT → {out.name} ({df.shape[0]} filas)")

def date_id(s):
    s = pd.to_datetime(s, errors="coerce")
    return pd.to_numeric(s.dt.strftime("%Y%m%d"), errors="coerce")

so = pd.read_csv(STG/"stg_sales_order.csv").copy()
so["date_id"] = date_id(so["order_date"])
fact_orders = so[[
    "order_id","customer_id","channel_id","store_id",
    "billing_address_id","shipping_address_id","shipping_province_id",
    "status","currency_code",
    "subtotal","tax_amount","shipping_fee","total_amount","date_id"
]]
save(fact_orders, "fact_orders.csv")

oi = pd.read_csv(STG/"stg_sales_order_item.csv").copy()
oi["date_id"] = date_id(oi["order_date"])
fact_order_items = oi[[
    "order_item_id","order_id","product_id","quantity","unit_price","discount_amount","line_total","date_id"
]]
save(fact_order_items, "fact_order_items.csv")

pay = pd.read_csv(STG/"stg_payment.csv").copy()
pay["date_id_paid"] = date_id(pay.get("paid_at"))
fact_payments = pay[[
    "payment_id","order_id","method","status","amount","paid_at","transaction_ref","date_id_paid"
]]
save(fact_payments, "fact_payments.csv")

sh = pd.read_csv(STG/"stg_shipment.csv").copy()
sh["date_id_shipped"]   = date_id(sh.get("shipped_at"))
sh["date_id_delivered"] = date_id(sh.get("delivered_at"))
fact_shipments = sh[[
    "shipment_id","order_id","carrier","tracking_number","status",
    "shipped_at","delivered_at","delivery_days","date_id_shipped","date_id_delivered"
]]
save(fact_shipments, "fact_shipments.csv")

ws = pd.read_csv(STG/"stg_web_session.csv").copy()
ws["date_id"] = date_id(ws.get("started_at"))
fact_web_sessions = ws[[
    "session_id","customer_id","started_at","ended_at","source","device","date_id"
    if "ended_at" in ws.columns else "session_id"
]]
if isinstance(fact_web_sessions.columns, pd.Index) and "ended_at" not in ws.columns:
    fact_web_sessions = ws[["session_id","customer_id","started_at","source","device","date_id"]]
save(fact_web_sessions, "fact_web_sessions.csv")

nps = pd.read_csv(STG/"stg_nps_response.csv").copy()
nps["date_id"] = date_id(nps["responded_at"])
fact_nps = nps[[
    "nps_id","customer_id","channel_id","score","comment","responded_at","date_id"
]]
fact_nps["is_promoter"] = (fact_nps["score"] >= 9).astype(int)
fact_nps["is_detractor"]= (fact_nps["score"] <= 6).astype(int)
fact_nps["is_passive"]  = ((fact_nps["score"] >= 7) & (fact_nps["score"] <= 8)).astype(int)
save(fact_nps, "fact_nps.csv")

print("OK: FACTs generadas.")
