import pandas as pd
from pathlib import Path

def build_dim_channel(data: dict, output_path: Path) -> pd.DataFrame:
    ch = data["channel"].copy()

    # surrogate key
    ch.insert(0, "channel_sk", range(1, len(ch) + 1))

    dim = ch[["channel_sk", "channel_id", "code", "name"]].drop_duplicates()

    path = Path(output_path) / "dim" / "dim_channel.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_channel guardado en {path}")
    return dim
