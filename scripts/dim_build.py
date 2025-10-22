from pathlib import Path
import pandas as pd

# === Rutas base del proyecto ===
BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "RAW"
STG = BASE / "staging"
DW  = BASE / "DW"
DW.mkdir(exist_ok=True)  # crea DW/ si no existe

def save(df, name):
    """Guarda un DataFrame en DW/ y loguea cuántas filas se escribieron."""
    out = DW / name
    df.to_csv(out, index=False)
    print(f"[DW] DIM → {out.name} ({df.shape[0]} filas)")

def date_id(s):
    """
    Convierte una serie de fechas a un entero YYYYMMDD.
    - Acepta string o datetime.
    - Usa errors='coerce' para evitar romper si hay valores inválidos.
    """
    s = pd.to_datetime(s, errors="coerce")
    return pd.to_numeric(s.dt.strftime("%Y%m%d"), errors="coerce")

# ==========
# DIMENSIONES "CATÁLOGO/MAESTRO"
# ==========

# 1) dim_channel: catálogo de canales (se renombra para nombres consistentes)
dim_channel = pd.read_csv(RAW / "channel.csv").rename(
    columns={"code": "channel_code", "name": "channel_name"}
)
save(dim_channel, "dim_channel.csv")

# 2) dim_province: catálogo de provincias (nombres normalizados)
dim_province = pd.read_csv(RAW / "province.csv").rename(
    columns={"name": "province_name", "code": "province_code"}
)
save(dim_province, "dim_province.csv")

# 3) dim_customer: maestro de clientes (tal cual RAW)
dim_customer = pd.read_csv(RAW / "customer.csv")
save(dim_customer, "dim_customer.csv")

# 4) dim_product: desde STAGING ya desnormalizado (product + category)
dim_product = pd.read_csv(STG / "stg_product.csv")
save(dim_product, "dim_product.csv")

# 5) dim_store: desde STAGING (store + address + province)
dim_store = pd.read_csv(STG / "stg_store.csv")
save(dim_store, "dim_store.csv")

# 6) dim_address: opcional (si existe STAGING). Bloque robusto a nombres distintos.
addr_path = STG / "stg_address.csv"
if addr_path.exists():
    addr = pd.read_csv(addr_path)

    # --- Mapeos típicos posibles ---
    # Caso A (address+province crudo): address_id, line1, line2, city, province_id, province_name, province_code, postal_code, country_code, created_at
    # Caso B (tu naming original): id, street, number, floor, apartment, province_code, postal_code, customer_id (si lo hubieras agregado)

    # Normalizamos nombres si vienen en formato "estándar address+province"
    rename_map_standard = {
        "address_id": "address_id",
        "line1": "line1",
        "line2": "line2",
        "city": "city",
        "province_id": "province_id",
        "province_name": "province_name",
        "province_code": "province_code",
        "postal_code": "postal_code",
        "country_code": "country_code",
        "created_at": "created_at",
    }
    # Si vinieran con formato alternativo (como en tu ejemplo)
    rename_map_alt = {
        "id": "address_id",
        "street": "line1",
        "number": "line2",      # si 'number' lo querés en otra columna, ajustalo
        "floor": "floor",
        "apartment": "apartment",
        "province_code": "province_code",
        "postal_code": "postal_code",
        "customer_id": "customer_id",
    }

    # Detectamos automáticamente qué set de nombres usar:
    if "address_id" in addr.columns or "line1" in addr.columns:
        addr = addr.rename(columns=rename_map_standard)
        keep_cols = [c for c in [
            "address_id", "line1", "line2", "city",
            "province_id", "province_name", "province_code",
            "postal_code", "country_code", "created_at"
        ] if c in addr.columns]
    else:
        addr = addr.rename(columns=rename_map_alt)
        keep_cols = [c for c in [
            "address_id", "line1", "line2", "city",
            "province_code", "postal_code", "customer_id"
        ] if c in addr.columns]

    dim_address = addr[keep_cols].drop_duplicates().reset_index(drop=True)

    # Asegurar que address_id sea numérico entero si existe
    if "address_id" in dim_address.columns:
        dim_address["address_id"] = pd.to_numeric(dim_address["address_id"], errors="coerce").astype("Int64")

    save(dim_address, "dim_address.csv")
else:
    print("[DW] WARNING: stg_address.csv no encontrado en staging, omitiendo dim_address")

# ==========
# DIM FECHAS (dim_date)
# ==========

# Leemos una sola vez web_session para no reabrir el archivo varias veces
ws_full = pd.read_csv(STG / "stg_web_session.csv")

# Fechas de cada fuente:
so  = pd.read_csv(STG / "stg_sales_order.csv")[["order_date"]].rename(columns={"order_date": "dt"})
shp = pd.read_csv(STG / "stg_shipment.csv")[["shipped_at", "delivered_at"]].melt(value_name="dt")["dt"]

# started_at es obligatoria; ended_at puede no existir
if "ended_at" in ws_full.columns:
    ws = ws_full[["started_at", "ended_at"]].melt(value_name="dt")[["dt"]]
else:
    ws = ws_full[["started_at"]].rename(columns={"started_at": "dt"})

nps = pd.read_csv(STG / "stg_nps_response.csv")[["responded_at"]].rename(columns={"responded_at": "dt"})

# Unimos todas las fechas relevantes, convertimos, sacamos nulos y duplicados
cal = pd.concat([so["dt"], pd.Series(shp), ws["dt"], nps["dt"]], ignore_index=True)
cal = pd.to_datetime(cal, errors="coerce").dropna().drop_duplicates().sort_values()

# Armamos la dimensión de tiempo
dim_date = pd.DataFrame({"date": cal.dt.date})
dim_date["date_id"] = date_id(dim_date["date"])
dt = pd.to_datetime(dim_date["date"])
dim_date["year"]       = dt.dt.year
dim_date["month"]      = dt.dt.month
dim_date["day"]        = dt.dt.day
dim_date["year_month"] = dt.dt.strftime("%Y-%m")

save(dim_date[["date_id", "date", "year", "month", "day", "year_month"]], "dim_date.csv")

print("OK: DIMs generadas.")
