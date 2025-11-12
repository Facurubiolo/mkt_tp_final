# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación:** [DER](./assets/DER.png)


Este proyecto implementa un pipeline **ETL completo** para la materia *Introducción al Marketing y los Negocios Digitales*, utilizando datos crudos (`raw/*.csv`) y generando un **Data Warehouse** con tablas de dimensiones y hechos en la carpeta `warehouse/`.

**Dashboard Final (PowerBI):**  [Click aqui para ver el Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZDBlNWI1ZTQtYWNiNS00MzJjLWE3Y2EtYTk3NDAxZDMyNzkxIiwidCI6IjNlMDUxM2Q2LTY4ZmEtNDE2ZS04ZGUxLTZjNWNkYzMxOWZmYSIsImMiOjR9&pageName=0be84ea9ae3bfa95c784)

## Arquitectura del Proyecto
El proyecto sigue una estructura ETL clásica:

1. raw/: Guarda los 13 archivos .CSV originales que simulan la base de datos transaccional (OLTP) de la empresa.
2. etl/: Contiene toda la lógica de transformación, separada en:
 - etl/extract/: Scripts para leer los datos desde data/raw/.
 - etl/transform/: Scripts para limpiar, denormalizar y construir cada tabla de Dimensión y Hechos.
 - etl/load/: Scripts para guardar los dataframes transformados en el directorio warehouse/.
3. warehouse/: Aqui dentro se encuentran las dim y facts desnormalizadas
 - warehouse/dim/: Contiene las tablas de dimensiones desnormalizadas
 - warehouse/fact/: Contiene las tablas de hechos desnormalizadas
4. main.py: El script orquestador que llama a las funciones de extract, transform y load en el orden correcto.

##  Ejecución

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

##  2. Supuestos y Diseño del Modelo

### 🔹 Diseño general

El modelo del Data Warehouse se construyó siguiendo una **arquitectura en estrella (Star Schema)**, conformada por:

- **6 tablas de dimensiones (DIM)**
- **6 tablas de hechos (FACT)**



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

##  3. Diccionario de Datos
El Data Warehouse está compuesto por **6 dimensiones** y **6 tablas de hechos**.  
Cada tabla de dimensión incluye una *surrogate key (SK)* como PK, mientras que las tablas de hechos contienen las FK necesarias para el análisis en esquema estrella.

| Tipo | Tablas |
|------|---------|
| **Dimensiones** | dim_customer, dim_address, dim_product, dim_store, dim_channel, dim_calendar |
| **Hechos** | fact_sales_order, fact_sales_order_item, fact_payment, fact_shipment, fact_web_session, fact_nps_response |

## DIM_CUSTOMER  

| Atributo     | Tipo de Dato    | Descripción                                                                 |
|----------------|------------|------------------------------------------------------------------------------|
| customer_sk    | INT        | Clave surrogate generada en el DW                                            |
| customer_id    | INT        | Clave de negocio proveniente del sistema transaccional                    |
| email          | VARCHAR    | Correo electrónico del cliente                                              |
| first_name     | VARCHAR    | Nombre del cliente                                                           |
| last_name      | VARCHAR    | Apellido del cliente                                                         |
| phone          | VARCHAR    | Teléfono de contacto                                                         |
| status         | VARCHAR    | Estado del cliente (por ejemplo, 'active')                          |
| created_at     | DATETIME   | Fecha y hora en la que el cliente se dió de alta           |

## DIM_ADDRESS

| Atributo         | Tipo de Dato      | Descripción                                                                 |
|-----------------|------------|------------------------------------------------------------------------------|
| address_sk      | INT        | Clave surrogate generada en el DW                                        |
| address_id      | INT        | Clave de negocio proveniente del sistema transaccional                 |
| line1           | VARCHAR    | Dirección principal (calle y número, sucursal)                        |
| line2           | VARCHAR    | Información adicional de la dirección (piso, departamento)                 |
| city            | VARCHAR    | Ciudad correspondiente a la dirección.                                       |
| province_id     | INT        | ID de la provincia según la tabla de provincias original                   |
| province_name   | VARCHAR    | Nombre de la provincia                                                      |
| province_code   | VARCHAR    | Código corto de la provincia (por ejemplo, BA, CBA)                         |
| postal_code     | VARCHAR    | Código postal                                                               |
| country_code    | VARCHAR    | Código de país ISO (por ejemplo, AR)                                       |
| address_type    | VARCHAR    | Tipo de dirección (billing, shipping)                                       |
| created_at      | DATETIME   | Fecha y hora en la que la dirección fue creada en la fuente original        |

## DIM_PRODUCT

| Atributo              | Tipo de Dato      | Descripción                                                                 |
|----------------------|------------|------------------------------------------------------------------------------|
| product_sk           | INT        | Clave surrogate generada en el DW.                                          |
| product_id           | INT        | Clave de negocio proveniente del sistema transaccional                     |
| sku                  | VARCHAR    | Código único del producto (Stock Keeping Unit)                             |
| name                 | VARCHAR    | Nombre del producto                                                         |
| category_id          | INT        | ID de la categoría asociada                                                |
| category_name        | VARCHAR    | Nombre de la categoría del producto                                        |
| parent_category_name | VARCHAR    | Categoría padre (nivel superior)                                           |
| list_price           | FLOAT      | Precio de lista del producto                                               |
| status               | VARCHAR    | Estado del producto (A = activo)                       |
| created_at           | DATETIME   | Fecha y hora en la que el producto fue creado         |

## DIM_STORE

| Atributo        | Tipo de Dato      | Descripción                                                                 |
|----------------|------------|------------------------------------------------------------------------------|
| store_sk       | INT        | Clave surrogate generada en el DW                                          |
| store_id       | INT        | Clave de negocio proveniente del sistema transaccional                     |
| store_name     | VARCHAR    | Nombre de la tienda                                                         |
| line1          | VARCHAR    | Dirección principal de la tienda                                            |
| city           | VARCHAR    | Ciudad donde se encuentra la tienda                                        |
| province_name  | VARCHAR    | Nombre de la provincia                                                      |
| province_code  | VARCHAR    | Código de la provincia (BA, CBA, etc.)                                      |
| postal_code    | VARCHAR    | Código postal de la ubicación                                               |
| country_code   | VARCHAR    | Código de país ISO (por ejemplo AR)                                         |
| created_at     | DATETIME   | Fecha de creación de la tienda                       |

## DIM_CHANNEL

| Atributo      | Tipo de Dato    | Descripción                                                          |
|--------------|----------|----------------------------------------------------------------------|
| channel_sk   | INT      | Clave surrogate generada en el DW                                   |
| channel_id   | INT      | Clave de negocio proveniente del sistema transaccional              |
| code         | VARCHAR  | Código del canal (ONLINE, OFFLINE)                      |
| name         | VARCHAR  | Nombre del canal de venta                                           |

## DIM_CALENDAR

| Atributo      | Tipo de Dato     | Descripción                                                                  |
|--------------|----------|------------------------------------------------------------------------------|
| calendar_sk  | INT      | Clave surrogate generada en el DW                                           |
| date         | DATE     | Fecha en formato estándar YYYY-MM-DD                               |
| date_id      | INT      | Fecha en formato YYYYMMDD (clave de negocio)                                        |
| year         | INT      | Año correspondiente                                                          |
| month        | INT      | Mes (1 a 12)                                                                 |
| day          | INT      | Día del mes                                                                  |
| day_of_week  | INT      | Día de la semana (1 = lunes, 7 = domingo)                                   |
| quarter      | VARCHAR  | Trimestre (Q1, Q2, Q3, Q4)                                                    |
| year_month   | VARCHAR  | Representación año-mes (YYYY-MM)                                             |

## FACT_SALES_ORDER
Tabla de hechos que registra cada pedido realizado por un cliente

| Atributo            | Tipo de Dato      | Descripción                                                                 |
|--------------------|------------|------------------------------------------------------------------------------|
| sales_order_sk     | INT        | Clave surrogate generada en el DW                                          |
| id                 | INT        | Clave de negocio del pedido (order_id)                                     |
| customer_id        | INT        | Clave de negocio que referencia a DIM_CUSTOMER                             |
| channel_id         | INT        | Clave de negocio que referencia a DIM_CHANNEL                               |
| store_id           | INT        | Clave de negocio que referencia a DIM_STORE                                 |
| order_date_id      | INT        | Clave que referencia a DIM_CALENDAR (YYYYMMDD)                              |
| order_time         | VARCHAR    | Hora del pedido                                                             |
| order_date         | DATE       | Fecha del pedido en formato YYYY-MM-DD                                      |
| billing_address_id | INT        | Clave surrogate que referencia a DIM_ADDRESS (dirección de facturación)     |
| shipping_address_id| INT        | Clave surrogate que referencia a DIM_ADDRESS (dirección de envío)           |
| status_order       | VARCHAR    | Estado del pedido (FULFILLED, PENDING, CANCELLED, etc.)                     |
| currency_code      | VARCHAR    | Código de moneda (por ejemplo, ARS)                                                  |
| subtotal           | FLOAT      | Monto subtotal del pedido antes de impuestos y envío                        |
| tax_amount         | FLOAT      | Monto de impuestos.                                                          |
| shipping_fee       | FLOAT      | Monto del envío.                                                             |
| total_amount       | FLOAT      | Monto final del pedido.                                                      |

## FACT_SALES_ORDER_ITEM
Tabla de hechos que registra cada ítem dentro de un pedido  

| Atributo             | Tipo de Dato      | Descripción                                                                 |
|---------------------|------------|------------------------------------------------------------------------------|
| sales_order_item_sk | INT        | Clave surrogate generada en el DW                                          |
| id                  | INT        | Clave de negocio del ítem (order_item_id)                                   |
| customer_id         | INT        | Clave de negocio que referencia a DIM_CUSTOMER                              |
| channel_id          | INT        | Clave de negocio que referencia a DIM_CHANNEL                               |
| store_id            | INT        | Clave de negocio que referencia a DIM_STORE                                 |
| product_id          | INT        | Clave de negocio que referencia a DIM_PRODUCT                               |
| quantity            | INT        | Cantidad del producto en el ítem                                           |
| unit_price          | FLOAT      | Precio unitario del producto                                                |
| discount_amount     | FLOAT      | Monto de descuento aplicado                                                |
| line_total          | FLOAT      | Total del ítem (quantity × unit_price - discount)                           |
| order_date_id       | INT        | Clave que referencia a DIM_CALENDAR (YYYYMMDD)                              |
| order_date          | DATE       | Fecha del pedido                                                            |
| billing_address_id  | INT        | Clave surrogate hacia DIM_ADDRESS (facturación)                             |
| shipping_address_id | INT        | Clave surrogate hacia DIM_ADDRESS (envío)                                   |

## FACT_PAYMENT
Tabla de hechos que registra los pagos realizados por los clientes.  

| Atributo             | Tipo de Dato       | Descripción                                                                  |
|---------------------|------------|-------------------------------------------------------------------------------|
| payment_sk          | INT        | Clave surrogate generada en el DW                                           |
| id                  | INT        | Clave de negocio del pago (payment_id)                                      |
| customer_id         | INT        | Clave de negocio que referencia a DIM_CUSTOMER                               |
| billing_address_id  | INT        | Clave de negocio hacia DIM_ADDRESS (dirección de facturación)                |
| channel_id          | INT        | Clave de negocio que referencia a DIM_CHANNEL                                |
| store_id            | INT        | Clave de negocio que referencia a DIM_STORE                                  |
| method              | VARCHAR    | Método de pago (CASH, CARD, etc.)                         |
| status_payment      | VARCHAR    | Estado del pago (PAID, REFUNDED, FAILED)                                    |
| amount              | FLOAT      | Monto total del pago                                                         |
| paid_at_date_id     | INT        | Clave de fecha de cobro (YYYYMMDD), referencia a DIM_CALENDAR               |
| paid_at_time        | VARCHAR    | Hora en que se registró el pago                                             |
| transaction_ref     | VARCHAR    | Código de referencia de la transacción                                      |

## FACT_SHIPMENT
Tabla de hechos que registra los envíos realizados a los clientes.  

| Atributo               | Tipo de Dato       | Descripción                                                                   |
|-----------------------|------------|-------------------------------------------------------------------------------|
| shipment_sk           | INT        | Clave surrogate generada en el DW                                            |
| id                    | INT        | Clave de negocio del envío (shipment_id)                                      |
| customer_id           | INT        | Clave de negocio que referencia a DIM_CUSTOMER                                |
| shipping_address_id   | INT        | Clave de negocio hacia DIM_ADDRESS (dirección de entrega)                      |
| channel_id            | INT        | Clave de negocio que referencia a DIM_CHANNEL                                 |
| carrier               | VARCHAR    | Empresa transportista (por ejemplo: Correo Argentino, PICKUP)              |
| shipped_at_date_id    | INT        | Fecha de despacho (YYYYMMDD), referencia a DIM_CALENDAR                       |
| shipped_at_time       | VARCHAR    | Hora de despacho del envío                                                    |
| delivered_at_date_id  | INT        | Fecha de entrega (YYYYMMDD), referencia a DIM_CALENDAR                        |
| delivered_at_time     | VARCHAR    | Hora de entrega del envío                                                     |
| tracking_number       | VARCHAR    | Código de seguimiento del envío                                               |

## FACT_WEB_SESSION
Tabla de hechos que registra las sesiones web de los usuarios en el canal online.  

| Atributo         | Tipo de Dato    | Descripción                                                                  |
|-----------------|------------|------------------------------------------------------------------------------|
| web_session_sk  | INT        | Clave surrogate generada en el DW                                           |
| id              | INT        | Clave de negocio de la sesión (session_id).                                  |
| customer_id     | INT        | Clave de negocio que referencia a DIM_CUSTOMER                              |
| channel_id      | INT        | Clave de negocio que referencia a DIM_CHANNEL                               |
| start_date_id   | INT        | Fecha de inicio (YYYYMMDD), referencia a DIM_CALENDAR                       |
| start_time      | VARCHAR    | Hora de inicio de la sesión                                                 |
| end_date_id     | INT        | Fecha de fin (YYYYMMDD), referencia a DIM_CALENDAR                          |
| end_time        | VARCHAR    | Hora de fin de la sesión                                                    |
| device          | VARCHAR    | Dispositivo utilizado (desktop, mobile)                            |

## FACT_NPS_RESPONSE
Tabla de hechos que registra las respuestas de NPS (Net Promoter Score).  

| Atributo               | Tipo de Dato      | Descripción                                                                  |
|-----------------------|------------|------------------------------------------------------------------------------|
| nps_response_sk       | INT        | Clave surrogate generada en el DW.                                           |
| id                    | INT        | Clave de negocio de la respuesta NPS.                                        |
| customer_id           | INT        | Clave de negocio que referencia a DIM_CUSTOMER.                              |
| channel_id            | INT        | Clave de negocio que referencia a DIM_CHANNEL.                               |
| score                 | INT        | Puntuación dada por el cliente (0 a 10).                                     |
| comment               | VARCHAR    | Comentario ingresado por el cliente.                                         |
| responded_at_date_id  | INT        | Fecha de la respuesta (YYYYMMDD), referencia a DIM_CALENDAR.                 |
| responded_at_time     | VARCHAR    | Hora de la respuesta.                                                        |

### Enlaces a los Esquemas Estrella0

Cada hecho tiene su propio esquema estrella, diseñado con [dbdiagram.io](https://dbdiagram.io).  

| Hecho | Enlace al esquema |
|-------|-------------------|
| **fact_sales_order** | [📊 Star Schema - Ventas](assets/star_sales_order.png) |
| **fact_sales_order_item** | [📊 Star Schema - Ítems de Venta](assets/star_sales_order_item.png) |
| **fact_payment** | [📊 Star Schema - Pagos](assets/star_payment.png) |
| **fact_shipment** | [📊 Star Schema - Envíos](assets/star_shipment.png) |
| **fact_web_session** | [📊 Star Schema - Sesiones Web](assets/star_web_session.png) |
| **fact_nps_response** | [📊 Star Schema - NPS](assets/star_nps_response.png) |


## 4. Consultas CLave 

Para poder calcular los KPIs pedidos y utilizados en las visualizaciones, se crearon medidas DAX en la tabla Medidas en el modelo de Power Bi

### Ticket Promedio
```dax
Ticket Promedio ($K) = 
CALCULATE(
    SUM(fact_sales_order[total_amount]) /
    DISTINCTCOUNT(fact_sales_order[id]),
    fact_sales_order[status_order] IN {"PAID", "FULFILLED"}
)
```

### NPS
```dax
NPS = 
VAR Promoters =
    COUNTROWS(
        FILTER(
            fact_nps_response,
            fact_nps_response[score] >= 9
        )
    )
VAR Detractors =
    COUNTROWS(
        FILTER(
            fact_nps_response,
            fact_nps_response[score] <= 6
        )
    )
VAR TotalResponses =
    COUNTROWS(fact_nps_response)

RETURN
IF(
    TotalResponses > 0,
    ( ( Promoters - Detractors ) / TotalResponses ) * 100
)
```

### Ventas Totales 
```dax
Total Ventas = 
CALCULATE(
    SUM(fact_sales_order[total_amount]),
    fact_sales_order[status_order] IN {"PAID","FULFILLED"}
)
```

### Usuarios Activos
```dax
Usuarios Activos = 
DISTINCTCOUNT(fact_web_session[customer_id])
```

### Tiempo Entrega (Dias)
```dax
Tiempo Entrega (días) = 
AVERAGEX(
    FILTER(
        fact_shipment,
        NOT ISBLANK ( fact_shipment[Shipped Date] ) &&
        NOT ISBLANK ( fact_shipment[Delivered Date] )
    ),
    DATEDIFF( fact_shipment[Shipped Date], fact_shipment[Delivered Date], DAY )
)
```

### Total Envios
```dax
Total Envíos = 
COUNTROWS ( fact_shipment )
```

### Costo Promedio de Envio
```dax
Costo Promedio Envío = 
AVERAGE( fact_sales_order[shipping_fee])
```

### Costo Total Envíos 
```dax
Costo Total Envíos = 
SUM( fact_sales_order[shipping_fee]) 
```

## 5. Licencia y reconocimiento

Este proyecto fue desarrollado por **Facundo Rubiolo** en el marco de la materia *Integración de Marketing* de la Licenciatura en Ciencia de Datos de la Universidad Austral (2025).

Los archivos originales de datos (carpeta `/raw`) y el diagrama entidad–relación (`DER.png`) provienen del repositorio académico del profesor **Augusto Carmona**, utilizados únicamente como base para la práctica de modelado, transformación y análisis de datos.

© 2025 **Facundo Rubiolo** — MIT License.  
Todos los derechos reservados sobre los desarrollos, documentación y arquitectura del proyecto.