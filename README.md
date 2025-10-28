# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación:** [DER](./assets/DER.png)

# Marketing Data Warehouse - ETL Final Project

Este proyecto implementa un pipeline **ETL completo** para la materia *Introducción al Marketing y los Negocios Digitales*, utilizando datos crudos (`raw/*.csv`) y generando un **Data Warehouse** con tablas de dimensiones y hechos en la carpeta `warehouse/`.

## 🚀 Ejecución

### 1. Clonar el repositorio
```bash
git clone < https://github.com/Facurubiolo/mkt_tp_final >
cd mkt_tp_final

### 2. Crear y Activar Entorno Virtual
python -m venv .venv
source .venv/Scripts/activate  # En Windows
# o
source .venv/bin/activate      # En Mac/Linux
