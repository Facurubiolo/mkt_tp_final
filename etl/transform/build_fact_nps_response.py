import pandas as pd
from pathlib import Path

def build_fact_nps_response(data: dict, output_path: Path) -> pd.DataFrame:
    nps = data["nps_response"].copy()
    if "comment" not in nps.columns:
        nps["comment"] = pd.NA

    nps["responded_at"] = pd.to_datetime(nps["responded_at"], errors="coerce")
    nps["responded_at_date_id"] = nps["responded_at"].dt.strftime("%Y%m%d").astype("Int64")
    nps["responded_at_time"] = nps["responded_at"].dt.strftime("%H:%M:%S")

    fact = nps[[
        "nps_id",
        "customer_id",
        "channel_id",
        "score",
        "comment",
        "responded_at_date_id",
        "responded_at_time"
    ]].rename(columns={"nps_id": "id"})

    fact.insert(0, "nps_response_sk", range(1, len(fact) + 1))

    path = Path(output_path) / "fact" / "fact_nps_response.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fact.to_csv(path, index=False)
    print(f"📦 fact_nps_response guardado en {path}")
    return fact
