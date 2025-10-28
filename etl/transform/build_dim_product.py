import pandas as pd
from pathlib import Path

def build_dim_product(data: dict, output_path: Path) -> pd.DataFrame:
    prod = data["product"].copy()                 # product_id, sku, name, category_id, list_price, status, created_at
    cat  = data["product_category"].copy()        # category_id, name, parent_id

    # 1) Traigo nombre de categoría con sufijo claro (evita name_x/name_y)
    prod = prod.merge(
        cat[["category_id", "name", "parent_id"]],
        on="category_id",
        how="left",
        suffixes=("", "_category")                # 'name' (producto) y 'name_category' (categoría)
    )

    # 2) Traigo nombre de la categoría padre
    cat_parent = cat[["category_id", "name"]].rename(
        columns={"category_id": "parent_id", "name": "parent_category_name"}
    )
    prod = prod.merge(cat_parent, on="parent_id", how="left")

    # 3) Surrogate key
    prod.insert(0, "product_sk", range(1, len(prod) + 1))

    # 4) Selección y renombres finales
    #    Si tu CSV de productos usa 'product_name' en vez de 'name', lo contemplamos.
    product_name_col = "name" if "name" in prod.columns else "product_name"

    cols = [
        "product_sk",
        "product_id",
        "sku",
        product_name_col,          # nombre del producto
        "category_id",
        "name_category",           # nombre de la categoría
        "parent_category_name",
        "list_price",
        "status",
        "created_at",
    ]

    # Filtrar por columnas que existan (por si alguna faltara en tu CSV)
    cols = [c for c in cols if c in prod.columns]

    dim = prod[cols].drop_duplicates().rename(columns={
        product_name_col: "name",
        "name_category": "category_name",
    })

    # 5) Guardado
    path = Path(output_path) / "dim" / "dim_product.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_product guardado en {path}")
    return dim
