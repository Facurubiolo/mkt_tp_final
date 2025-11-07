import pandas as pd
from pathlib import Path

def build_dim_address(data: dict, output_path: Path) -> pd.DataFrame:
    addr = data["address"].copy()
    prov = data["province"].copy()  

    # join para traer nombre y código de provincia
    addr = addr.merge(prov, how="left", on="province_id")

    # completo columnas si faltan 
    if "address_type" not in addr.columns:
        addr["address_type"] = pd.NA
    if "created_at" not in addr.columns:
        addr["created_at"] = pd.NaT

    # surrogate key
    addr.insert(0, "address_sk", range(1, len(addr) + 1))

    # columnas finales
    dim = addr[[
        "address_sk",
        "address_id",
        "line1",
        "line2",
        "city",
        "province_id",
        "name",          # province_name
        "code",          # province_code
        "postal_code",
        "country_code",
        "address_type",
        "created_at"
    ]].rename(columns={"name": "province_name", "code": "province_code"}).drop_duplicates()

    path = Path(output_path) / "dim" / "dim_address.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_address guardado en {path}")
    return dim
