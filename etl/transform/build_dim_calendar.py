import pandas as pd
from pathlib import Path

def build_dim_calendar(data: dict, output_path: Path) -> pd.DataFrame:
    # recolecto fechas desde tablas transaccionales
    cols = []
    
    ## verifico que existan las tablas y columnas antes de colectar y luego lo concateno
    def collect(df_key, col):
        if df_key in data and col in data[df_key].columns:
            s = pd.to_datetime(data[df_key][col], errors="coerce").dropna()
            if not s.empty:
                cols.append(s.dt.normalize())

    collect("sales_order", "order_date")
    collect("payment", "paid_at")
    collect("shipment", "shipped_at")
    collect("shipment", "delivered_at")
    collect("web_session", "started_at")
    if "ended_at" in data.get("web_session", pd.DataFrame()).columns:
        collect("web_session", "ended_at")
    collect("nps_response", "responded_at")

    if cols:
        all_dates = pd.concat(cols).drop_duplicates().sort_values()
        dim = pd.DataFrame({"date": all_dates})
    else:
        dim = pd.DataFrame({"date": pd.to_datetime([])})

    # claves y atributos
    dim["date_id"] = dim["date"].dt.strftime("%Y%m%d").astype("Int64")
    dim["year"] = dim["date"].dt.year
    dim["month"] = dim["date"].dt.month
    dim["day"] = dim["date"].dt.day
    dim["day_of_week"] = dim["date"].dt.dayofweek + 1  
    dim["quarter"] = "Q" + ((dim["month"] - 1) // 3 + 1).astype(str)
    dim["year_month"] = dim["date"].dt.strftime("%Y-%m")

    # surrogate key 
    dim.insert(0, "calendar_sk", range(1, len(dim) + 1))

    path = Path(output_path) / "dim" / "dim_calendar.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_calendar guardado en {path}")
    return dim
