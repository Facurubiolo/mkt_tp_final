import pandas as pd
from pathlib import Path

def build_fact_web_session(data: dict, output_path: Path) -> pd.DataFrame:
    #  Copiamos las tablas que necesito
    ws = data["web_session"].copy()
    ch = data["channel"].copy()

    #  Hacemos el merge directo por el código del canal
    ws = ws.merge(
        ch[["channel_id", "code"]],
        left_on="source",
        right_on="code",
        how="left"
    )

    #  Convertimos las fechas y horas
    ws["started_at"] = pd.to_datetime(ws["started_at"], errors="coerce")
    ws["ended_at"] = pd.to_datetime(ws["ended_at"], errors="coerce")

    ws["start_date_id"] = ws["started_at"].dt.strftime("%Y%m%d").astype("Int64")
    ws["start_time"] = ws["started_at"].dt.strftime("%H:%M:%S")
    ws["end_date_id"] = ws["ended_at"].dt.strftime("%Y%m%d").astype("Int64")
    ws["end_time"] = ws["ended_at"].dt.strftime("%H:%M:%S")

   
    fact = ws[[
        "session_id",
        "customer_id",
        "channel_id",
        "start_date_id", ## surrogate
        "start_time",
        "end_date_id", ## surrogate 
        "end_time",
        "device"
    ]].rename(columns={"session_id": "id"})

    
    fact.insert(0, "web_session_sk", range(1, len(fact) + 1))

    
    path = Path(output_path) / "fact" / "fact_web_session.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_web_session guardado en {path}")
    return fact
