import pandas as pd
from pathlib import Path

def build_dim_store(data: dict, output_path: Path) -> pd.DataFrame:
    """
    DIM_STORE: store_key + dirección embebida (desnormalizada)
    Guarda: warehouse/dim/dim_store.csv
    """
    store = data["store"].copy()
    addr = data["address"].copy()
    prov = data["province"].copy()

    store = store.merge(addr, how="left", on="address_id")
    store = store.merge(prov, how="left", on="province_id")

    # surrogate y business key
    store["id"] = range(1, len(store) + 1)
    store = store.rename(columns={
        "store_id": "store_key",
        "name_x": "store_name",
        "name_y": "province_name",
        "code": "province_code",
        "created_at_x": "created_at",
    })

    dim = store[[
        "id",
        "store_key",
        "store_name",
        "line1",
        "city",
        "province_name",
        "province_code",
        "postal_code",
        "country_code",
        "created_at",
    ]].drop_duplicates()

    path = Path(output_path) / "dim" / "dim_store.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_store guardado en {path}")
    return dim
