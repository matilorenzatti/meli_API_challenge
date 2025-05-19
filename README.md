# Challenge Técnico – Consumo de API de Cotizaciones de Monedas

Este proyecto fue desarrollado como parte de un **challenge técnico** para evaluar habilidades en extracción, transformación y carga (ETL) de datos desde una API pública de cotizaciones de monedas extranjeras. La solución replica una arquitectura moderna de ingeniería de datos con enfoque en trazabilidad, eficiencia y claridad.

---

## 🎯 Objetivo General

Construir un proceso ETL que:

- Extraiga cotizaciones de monedas (USD, EUR, BTC → BRL) desde una API pública.
- Almacene los datos crudos en formato JSON en una zona *Bronze*.
- Transforme, normalice y limpie la información en formato **Parquet** en una zona *Silver*.
- Genere un archivo `.csv` final en *Gold*, como solicita el ejercicio.
- Cargue los datos a Google BigQuery.
- Registre logs en cada etapa para trazabilidad.
- Mantenga una estructura profesional, escalable y modular.

---

## 🌐 API utilizada

**AwesomeAPI - Cotação de Moedas**
📘 Documentación oficial: [https://docs.awesomeapi.com.br/api-de-moedas](https://docs.awesomeapi.com.br/api-de-moedas)


---

## 🔁 Flujo ETL aplicado

### 🟤 Bronze
- Se extrae el JSON original de la API.
- Se guarda sin modificaciones en `data/o1_bronze/*.json`.

### ⚪ Silver
- Se transforman los JSON a DataFrames.
- Se renombran los campos:
  `base_currency`, `destination_currency`, `purchase_value`, `sale_value`, `date_time`
- Se normaliza la fecha al formato `YYYY-MM-DD HH:mm:ss` (UTC).
- Se guarda como archivo Parquet en `data/o2_silver/*`.

### 🟡 Gold
- Se convierte el Parquet a CSV en `data/o3_gold/data_currencies.csv`.
- Se sube el mismo DataFrame a una tabla de **Google BigQuery**.

---


---

## 🗃️ Estructura de datos generada

El archivo final `data_currencies.csv` contiene:

| Campo                | Descripción                                 |
|----------------------|---------------------------------------------|
| `base_currency`      | Moneda base (ej. USD)                       |
| `destination_currency` | Moneda destino (ej. BRL)                  |
| `purchase_value`     | Valor de compra (`bid`) convertido a float |
| `sale_value`         | Valor de venta (`ask`) convertido a float  |
| `date_time`          | Fecha/hora normalizada (`YYYY-MM-DD HH:mm:ss`) |

---

## 🧪 ¿Cómo ejecutar el proyecto?

Instalá las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Y ejecutá el script principal:

```bash
python main.py
```

---

---

## ✅ Conclusión

Este proyecto simula un flujo real de procesamiento de datos financieros, aplicando estándares y buenas prácticas propias de un entorno profesional de ingeniería de datos.

Se diseñó con el objetivo de cumplir el challenge técnico de forma sólida, clara y escalable, integrando:

- 🧠 **Pensamiento analítico estructurado** para transformar datos semiestructurados en información útil.
- 🏗️ **Arquitectura modular (Bronze → Silver → Gold)** que permite trazabilidad, versionado y reutilización de cada etapa.
- 🔍 **Registro de logs por etapa**, garantizando auditoría y depuración ante errores o futuras automatizaciones.
- 🧹 **Limpieza y estandarización de datos**, asegurando formatos correctos y listos para análisis.
- 🌐 **Interoperabilidad con otras plataformas**, gracias a la carga en CSV y la posibilidad de publicar en Google BigQuery.

Este repositorio representa un flujo completo de datos orientado a producción, con foco en calidad, claridad, y mantenibilidad.

> 📌 Si tenés dudas, sugerencias o querés extender este flujo a nuevas monedas o integraciones, ¡bienvenido a colaborar!


```bash
matilorenzatti99@gmail.com
```
