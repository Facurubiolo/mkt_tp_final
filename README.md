# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación:** [DER](./assets/DER.png)


Este proyecto implementa un pipeline **ETL completo** para la materia *Introducción al Marketing y los Negocios Digitales*, utilizando datos crudos (`raw/*.csv`) y generando un **Data Warehouse** con tablas de dimensiones y hechos en la carpeta `warehouse/`.

## 🚀 Ejecución

### 1. Clonar el repositorio
```bash
git clone < https://github.com/Facurubiolo/mkt_tp_final >
cd mkt_tp_final
```

### 2. Crear y Activar Entorno Virtual
``` bash
python -m venv .venv
source .venv/Scripts/activate  
```

### 3. Instalar dependencias
``` bash
pip install -r requirements.txt
```

### 4. Ejecutar el pipeline ETL
``` bash
python main.py
```

## 🧱 2. Supuestos y Diseño del Modelo

### 🔹 Diseño general

El modelo del Data Warehouse se construyó siguiendo una **arquitectura en estrella (Star Schema)**, conformada por:

- **6 tablas de dimensiones (DIM)**
- **6 tablas de hechos (FACT)**

Cada tabla de dimensión contiene una **surrogate key (clave artificial incremental)** que se utiliza como **clave primaria (PK)**.  
Las tablas de hechos utilizan dichas claves como **claves foráneas (FK)** para permitir la integración y análisis cruzado.

---

### 🔹 Supuestos principales del diseño

1. **Integridad referencial**:  
   Todas las claves en las tablas de hechos (`customer_id`, `channel_id`, `store_id`, etc.) se relacionan con las claves de las tablas de dimensiones correspondientes.

2. **Surrogate Keys (claves sustitutas):**  
   Cada tabla de dimensión genera una clave incremental (`dim_xxx_sk`) para evitar dependencias de claves de negocio originales.

3. **Fechas normalizadas:**  
   La dimensión `dim_calendar` fue construida para reemplazar fechas en las tablas de hechos con `date_id` en formato `YYYYMMDD`.

4. **Desnormalización controlada:**  
   Se combinaron campos de distintas tablas `raw/` (por ejemplo, `store` + `address` + `province`) para obtener una vista unificada y optimizada para análisis.

5. **Campos monetarios:**  
   Los valores numéricos (`subtotal`, `tax_amount`, `shipping_fee`, `total_amount`) fueron convertidos a tipo `float`, reemplazando comas por puntos en caso de ser necesario.

6. **Fuentes de datos:**  
   Todos los datos provienen de archivos CSV ubicados en la carpeta `raw/`, los cuales representan distintas entidades del negocio de e-commerce.

7. **Pipeline reproducible:**  
   El proceso ETL completo puede ejecutarse de forma automática mediante `python main.py`, generando los resultados en `warehouse/`.

---

## 📘 3. Diccionario de Datos
El Data Warehouse está compuesto por **6 dimensiones** y **6 tablas de hechos**.  
Cada tabla de dimensión incluye una *surrogate key (SK)* como PK, mientras que las tablas de hechos contienen las FK necesarias para el análisis en esquema estrella.

| Tipo | Tablas |
|------|---------|
| **Dimensiones** | dim_customer, dim_address, dim_product, dim_store, dim_channel, dim_calendar |
| **Hechos** | fact_sales_order, fact_sales_order_item, fact_payment, fact_shipment, fact_web_session, fact_nps_response |

### 📎 Enlaces a los Esquemas Estrella0

Cada hecho tiene su propio esquema estrella, diseñado con [dbdiagram.io](https://dbdiagram.io).  

| Hecho | Enlace al esquema |
|-------|-------------------|
| **fact_sales_order** | [📊 Star Schema - Ventas](assets/star_sales_order.png) |
| **fact_sales_order_item** | [📊 Star Schema - Ítems de Venta](assets/star_sales_order_item.png) |
| **fact_payment** | [📊 Star Schema - Pagos](assets/star_payment.png) |
| **fact_shipment** | [📊 Star Schema - Envíos](assets/star_shipment.png) |
| **fact_web_session** | [📊 Star Schema - Sesiones Web](assets/star_web_session.png) |
| **fact_nps_response** | [📊 Star Schema - NPS](assets/star_nps_response.png) |


