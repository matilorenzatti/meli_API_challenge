explicacion_proceso: |
  # 🧠 Proceso de Diseño y Resolución del ETL – Cotizaciones AwesomeAPI

  Este documento tiene como objetivo explicar en detalle cómo estructuré y resolví el proyecto técnico de ETL solicitado, utilizando la API pública de AwesomeAPI para consumir cotizaciones de monedas extranjeras.

  La solución fue diseñada con foco en modularidad, trazabilidad y buenas prácticas de ingeniería de datos, simulando un entorno real de trabajo con arquitectura por capas y registros detallados de cada etapa.

  ---

  ## 🎯 Objetivo general del challenge

  Se solicitaba:

  1. Consultar cotizaciones de los pares: USD/BRL, EUR/BRL y BTC/BRL (yo decidí generalizarlo a todos los pares `*-BRL`)
  2. Estandarizar los campos resultantes en el siguiente formato:

     ```
     base_currency
     destination_currency
     purchase_value
     sale_value
     date_time (UTC y formato: YYYY-MM-DD HH:mm:ss)
     ```

  3. Guardar los datos normalizados en `.csv`
  4. (Diferencial agregado) Subir la información a una base de datos relacional o BigQuery

  ---


---

## 🔎 Explicación técnica por módulo

### 🔹 1. Extracción (`o1_extraction`)
**Clase:** `CurrencyExtractor`

- Consulta el endpoint `/available` para obtener todos los pares posibles
- Filtra únicamente los que terminan en `-BRL` (dinámicamente)
- Por cada par, solicita los últimos 180 días de cotizaciones
- Guarda un `.json` por par en la carpeta `data/o1_bronze/`

✔️ Esta etapa actúa como "ingesta cruda" (bronze), manteniendo el dato sin tocar.

---

### 🔹 2. Limpieza y unificación (`o2_transformation`)
**Clase:** `DFsCurrencies`

- Lee todos los JSON desde la capa `bronze`
- Extrae la metadata (`code`, `codein`, `name`, `create_date`) del primer registro
- Concatena todos los valores históricos en un solo DataFrame
- Devuelve un único DF consolidado y limpio, listo para transformar

✔️ La separación entre extracción y transformación me permite revisar los datos sin procesarlos aún.

---

### 🔹 3. Transformación (`o3_transformation`)
**Clase:** `CurrencyTransformer`

- Recibe el DF crudo y lo transforma a la estructura pedida:
  - Renombra campos
  - Convierte el `timestamp` a `datetime UTC` con formato legible
  - Reordena columnas
- Guarda el archivo como `.parquet` en `data/o2_silver/`

✔️ Usar `.parquet` permite eficiencia de almacenamiento y velocidad en lecturas posteriores.

---

### 🔹 4. Modelado / Exportación (`o4_modeling`)
**Clase:** `CurrencyModeler`

- Copia el `.parquet` desde Silver a Gold
- Convierte el `.parquet` a `.csv` con separador `;` y codificación `utf-8-sig` (compatible con Excel)
- Guarda ambos archivos en `data/o3_gold/`

✔️ Esto permite cumplir con la consigna del CSV, pero conservar la eficiencia del `.parquet`.

---

### 🔹 5. Serving / BigQuery (`o5_serving`)
**Clase:** `CargadorBigQuery`

- Recorre todos los `.parquet` dentro de `data/o3_gold/`
- Sube cada archivo a BigQuery usando `pandas_gbq` con autodetección de esquema
- Se autentica vía `.json` en `meli_key.json`

✔️ Esto permite usar Looker Studio, Data Studio u otras herramientas para consumo de datos.

---

## ▶️ Ejecución del pipeline completo

El archivo `main.py` orquesta todo el proceso:

```bash
python notebooks/main.py
```

---

---

## 🔚 Conclusión

Este proyecto fue mucho más que una simple extracción y transformación de datos: lo abordé como un desafío real de ingeniería de datos, priorizando la claridad, la modularidad y la posibilidad de escalar o modificar el proceso con facilidad.

Cada etapa del pipeline fue pensada para ser reutilizable y entendible por cualquier analista o desarrollador que se sume al proyecto. Separar la lógica en capas (bronze, silver y gold), aplicar logs por módulo y mantener cada clase con una única responsabilidad me permitió construir una solución ordenada y profesional.

Además, complementé el entregable solicitado (archivo `.csv`) con formatos y flujos que se utilizan en la práctica (como `.parquet` y BigQuery), lo cual suma valor al proceso y lo prepara para integraciones futuras.

Estoy conforme con el resultado final: el proyecto quedó robusto, claro, trazable y alineado a estándares de trabajo en datos reales.
