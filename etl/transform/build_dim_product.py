import pandas as pd
from pathlib import Path

def build_dim_product(data: dict, output_path: Path) -> pd.DataFrame:
    """
    DIM_PRODUCT: product_key + categoría desnormalizada
    Guarda: warehouse/dim/dim_product.csv
    """
    prod = data["product"].copy()
    cat = data["product_category"].copy()

    # join a categoría y categoría padre (si existe)
    prod = prod.merge(cat[["category_id", "name", "parent_id"]], how="left", on="category_id")
    cat_parent = cat[["category_id", "name"]].rename(columns={
        "category_id": "parent_id", "name": "parent_category_name"
    })
    prod = prod.merge(cat_parent, how="left", on="parent_id")

    # surrogate y business key
    prod["id"] = range(1, len(prod) + 1)
    prod = prod.rename(columns={
        "product_id": "product_key",
        "name_y": "category_name"
    })

    dim = prod[[
        "id",
        "product_key",
        "sku",
        "name",
        "category_id",
        "category_name",
        "parent_category_name",
        "list_price",
        "status",
        "created_at",
    ]].drop_duplicates()

    path = Path(output_path) / "dim" / "dim_product.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_product guardado en {path}")
    return dim
