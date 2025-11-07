import pandas as pd
from pathlib import Path

def build_dim_product(data: dict, output_path: Path) -> pd.DataFrame:
    # agarro la tabla de productos
    prod = data["product"].copy()  
     # agarro la tabla de categorías              
    cat  = data["product_category"].copy()        

     # traigo el nombre de la categoría y el parent_id
    prod = prod.merge(
        cat[["category_id", "name", "parent_id"]],
        on="category_id",
        how="left",
        suffixes=("", "_category")                
    )

    #  Traigo nombre de la categoría padre
    cat_parent = cat[["category_id", "name"]].rename(
        columns={"category_id": "parent_id", "name": "parent_category_name"}
    )
    prod = prod.merge(cat_parent, on="parent_id", how="left")

    #  Surrogate key
    prod.insert(0, "product_sk", range(1, len(prod) + 1))

    #  Selección y renombres finales
    product_name_col = "name" if "name" in prod.columns else "product_name"

    cols = [
        "product_sk",
        "product_id",
        "sku",
        product_name_col,          
        "category_id",
        "name_category",           
        "parent_category_name",
        "list_price",
        "status",
        "created_at",
    ]

    # Filtro por columnas que existan 
    cols = [c for c in cols if c in prod.columns]

    dim = prod[cols].drop_duplicates().rename(columns={
        product_name_col: "name",
        "name_category": "category_name",
    })

    
    path = Path(output_path) / "dim" / "dim_product.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dim.to_csv(path, index=False)
    print(f"✅ dim_product guardado en {path}")
    return dim
