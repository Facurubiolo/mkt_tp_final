import pandas as pd
from pathlib import Path

def build_dim_channel(data: dict, output_path: Path) -> pd.DataFrame:
    """
    DIM_CHANNEL: channel_key + code + name
    Guarda: warehouse/dim/dim_channel.csv
    """
    ch = data["channel"].copy()

    ch["id"] = range(1, len(ch) + 1)
    ch = ch.rename(columns={"channel_id": "channel_key"})

    dim = ch[["id", "channel_key", "code", "name"]].drop_duplicates()

    path = Path(output_path) / "dim" / "dim_channel.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_channel guardado en {path}")
    return dim
