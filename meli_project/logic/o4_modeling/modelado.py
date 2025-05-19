import os
import pandas as pd
from meli_project.logic.utils.utils import *




class ModeladorWB:

    """
    Clase encargada de construir el modelo dimensional a partir de los DataFrames
    procesados en la capa silver. Crea y guarda las tablas de hechos y dimensiones en gold.
    """


    def __init__(self):

        self.silver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o2_silver")
        )
        self.gold_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o3_gold")
        )
        os.makedirs(self.gold_path, exist_ok=True)



    def cargar_todos_df_silver(self):
        """
        Carga todos los archivos .parquet de la capa silver en un solo DataFrame unificado.
        """

        df_list = []

        if not os.path.exists(self.silver_path):
            print("❌ Carpeta silver no encontrada.")
            return pd.DataFrame()


        for file in os.listdir(self.silver_path):

            if file.endswith(".parquet"):

                try:
                    df_path = os.path.join(self.silver_path, file)
                    df = pd.read_parquet(df_path)
                    df_list.append(df)

                except Exception as e:

                    continue


        if not df_list:
            return "⚠️ No se pudieron cargar archivos .parquet desde silver."

        return pd.concat(df_list, ignore_index=True)



    def crear_tabla_dim_time(self, df):

        d_time = df[["TIME_PERIOD"]].drop_duplicates().sort_values("TIME_PERIOD")

        d_time["time_id"] = range(1, len(d_time) + 1)

        return d_time[["time_id", "TIME_PERIOD"]]




    def crear_tabla_dim_area(self, df):

        d_area = df[["REF_AREA"]].drop_duplicates().sort_values("REF_AREA")

        d_area["area_id"] = range(1, len(d_area) + 1)

        return d_area[["area_id", "REF_AREA"]]





    def crear_tabla_dim_indicadores(self, df):

        d_ind = df[["INDICATOR", "INDICATOR_NAME", "CATEGORY"]].drop_duplicates().reset_index(drop=True)

        # Crear ID numérico para cada indicador
        d_ind["indicator_id"] = range(1, len(d_ind) + 1)

        # Crear una etiqueta legible
        d_ind["indicator_label"] = d_ind["INDICATOR"].map(
            lambda x: diccionario_indicadores_info.get(x, {}).get("indicator_label")
        )

        d_ind["indicator_description"] = d_ind["INDICATOR"].map(
            lambda x: diccionario_indicadores_info.get(x, {}).get("indicator_description")
        )

        return d_ind[["indicator_id", "INDICATOR", "INDICATOR_NAME", "CATEGORY", "indicator_label", "indicator_description"]]




    def crear_tabla_hechos(self, df, d_time, d_area, d_indicadores):

        f = df[["OBS_VALUE", "TIME_PERIOD", "REF_AREA", "INDICATOR"]].copy()

        f = f.merge(d_time, on="TIME_PERIOD", how="left")

        f = f.merge(d_area, on="REF_AREA", how="left")

        f = f.merge(d_indicadores, on="INDICATOR", how="left")


        return f[["time_id", "area_id", "indicator_id", "OBS_VALUE"]]




    def guardar_en_gold(self, nombre, df):

        path = os.path.join(self.gold_path, f"{nombre}.parquet")

        try:

            df.to_parquet(path, index=False)

            return f"✅ Guardado {nombre} en: {path}"

        except Exception as e:

            return f"❌ Error al guardar {nombre}: {e}"




    def ejecutar_pipeline_gold_dimensional(self):

        """
        Ejecuta el pipeline dimensional completo: unifica todos los .parquet de silver,
        genera las tablas dimensionales y de hechos, y las guarda en gold.
        """

        logger = setup_logger("o4_modeling_logs/pipeline_gold_dimensional.log")


        logger.info("INICIO PIPELINE para construir el modelo dimensional desde silver.")


        df_master = self.cargar_todos_df_silver()


        if not isinstance(df_master,pd.DataFrame) or df_master.empty:

            logger.error("FIN del pipeline. ❌ No se pudo generar el modelo dimensional por falta de datos.")

            return "❌ No se pudo generar el modelo dimensional por falta de datos."


        # Crear dimensiones y tabla de hechos
        try:
            d_time = self.crear_tabla_dim_time(df_master)
            logger.info(f"✅ Tabla 'd_time' creada con {len(d_time)} registros.")

            d_area = self.crear_tabla_dim_area(df_master)
            logger.info(f"✅ Tabla 'd_area' creada con {len(d_area)} registros.")

            d_indicadores = self.crear_tabla_dim_indicadores(df_master)
            logger.info(f"✅ Tabla 'd_indicadores' creada con {len(d_indicadores)} registros.")

            f_valores = self.crear_tabla_hechos(df_master, d_time, d_area, d_indicadores)
            logger.info(f"✅ Tabla de hechos 'f_valores' creada con {len(f_valores)} registros.")


        except Exception as e:
            logger.error(f"FIN pipeline. ❌ Error durante la creación de las tablas: {e}")
            return f"❌ Error durante el procesamiento: {e}"



        # Guardar todas las tablas
        tablas = {
            "dim_time_period": d_time,
            "dim_ref_area": d_area,
            "dim_indicadores": d_indicadores,
            "fact_obs_values": f_valores
        }


        for nombre, df in tablas.items():
            resultado = self.guardar_en_gold(nombre, df)

            if "✅" in resultado:
                logger.info(resultado)
            else:
                logger.error(resultado)


        logger.info("FIN PIPELINE. 🎯 Modelo dimensional generado y guardado correctamente.")

        return "✅ Modelo dimensional generado y guardado correctamente."
