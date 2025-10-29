import pandas as pd
from pathlib import Path

def build_dim_store(data: dict, output_path: Path) -> pd.DataFrame:
    store = data["store"].copy()      # store_id, name, address_id, created_at
    addr  = data["address"].copy()    # address_id, line1, city, province_id, postal_code, country_code, ...
    prov  = data["province"].copy()   # province_id, name, code

    # 1) Merge store + address (con sufijos claros)
    store = store.merge(
        addr,
        on="address_id",
        how="left",
        suffixes=("_store", "_addr")
    )

    # 2) Merge con province (evito name_x/name_y)
    store = store.merge(
        prov.rename(columns={"name": "province_name", "code": "province_code"}),
        on="province_id",
        how="left"
    )

    # 3) Surrogate key
    store.insert(0, "store_sk", range(1, len(store) + 1))

    # 4) Elegir columnas seguras 
    store_name_col = "name_store" if "name_store" in store.columns else "name"
    created_col    = "created_at_store" if "created_at_store" in store.columns else "created_at"

    # 5) Selección final y renombres
    cols = [
        "store_sk",
        "store_id",
        store_name_col,
        "line1",
        "city",
        "province_name",
        "province_code",
        "postal_code",
        "country_code",
        created_col
    ]
    # filtrar por si alguna no existe 
    cols = [c for c in cols if c in store.columns]

    dim = store[cols].drop_duplicates().rename(columns={
        store_name_col: "store_name",
        created_col: "created_at"
    })

    # 6) Guardamos
    path = Path(output_path) / "dim" / "dim_store.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_store guardado en {path}")
    return dim
