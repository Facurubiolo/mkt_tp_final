import pandas as pd
from pathlib import Path

def build_dim_calendar(data: dict, output_path: Path) -> pd.DataFrame:
    """
    DIM_CALENDAR generado desde fechas presentes en RAW.
    Columnas: id, date_key (YYYYMMDD), date, day, month, month_name, year, quarter, year_month, day_of_week
    Guarda: warehouse/dim/dim_calendar.csv
    """
    cols = []

    def collect(dfname, col):
        if dfname in data and col in data[dfname].columns:
            s = pd.to_datetime(data[dfname][col], errors="coerce").dropna()
            if not s.empty:
                cols.append(s.dt.date)

    collect("sales_order", "order_date")
    collect("payment", "paid_at")
    collect("shipment", "shipped_at")
    collect("shipment", "delivered_at")
    collect("web_session", "started_at")
    if "web_session" in data and "ended_at" in data["web_session"].columns:
        collect("web_session", "ended_at")
    collect("nps_response", "responded_at")

    if not cols:
        dim = pd.DataFrame(columns=[
            "id","date_key","date","day","month","month_name","year","quarter","year_month","day_of_week"
        ])
    else:
        all_dates = pd.to_datetime(pd.concat(cols).drop_duplicates()).sort_values()
        dim = pd.DataFrame({"date": all_dates})
        dim["date_key"] = dim["date"].astype(str).str.replace("-", "", regex=False).astype(int)
        dim["day"] = dim["date"].dt.day
        dim["month"] = dim["date"].dt.month
        try:
            dim["month_name"] = dim["date"].dt.month_name(locale="es_ES")
        except Exception:
            mapper = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
            dim["month_name"] = dim["month"].map(mapper)
        dim["year"] = dim["date"].dt.year
        dim["quarter"] = "Q" + ((dim["month"] - 1) // 3 + 1).astype(str)
        dim["year_month"] = dim["year"].astype(str) + "-" + dim["month"].astype(str).str.zfill(2)
        dim["day_of_week"] = dim["date"].dt.dayofweek + 1  # 1=Lun … 7=Dom
        dim.insert(0, "id", range(1, len(dim) + 1))  # surrogate simple

    path = Path(output_path) / "dim" / "dim_calendar.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_calendar guardado en {path}")
    return dim
