import os
import pandas as pd
from datetime import datetime
from meli_project.logic.utils.utils import *




class CurrencyTransformer:


    def __init__(self, df: pd.DataFrame):

        """
        Inicializa el transformador con un DataFrame unificado.
        """

        self.df = df

        # Definir ruta a capa silver
        self.silver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o2_silver")
        )

        os.makedirs(self.silver_path, exist_ok=True)



    def transformar(self):

        """
        Transforma y normaliza el DataFrame con las columnas necesarias.
        """

        logger = setup_logger("o3_transformation_logs/transformar_moneda.log")

        logger.info("INICIANDO transformación del DataFrame de monedas...")


        try:
            # Filtrar columnas necesarias
            columnas_base = ["code", "codein", "bid", "ask", "timestamp"]

            df = self.df[columnas_base].copy()

            # Renombrar columnas según la consigna
            df = df.rename(columns={
                "code": "base_currency",
                "codein": "destination_currency",
                "bid": "purchase_value",
                "ask": "sale_value"
            })


            # Conversión de tipos

            df["purchase_value"] = pd.to_numeric(df["purchase_value"], errors="coerce")

            df["sale_value"] = pd.to_numeric(df["sale_value"], errors="coerce")


            # Convertir el timestamp a datetime legible

            df["date_time"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)

            df.drop(columns=["timestamp"], inplace=True)

            logger.info(f"FIN transformacion. ✅ Transformación completada. Total de registros: {len(df)}")

            return df


        except Exception as e:

            logger.critical(f"FIN transformacion. ❌ Error en la transformación: {str(e)}")

            return pd.DataFrame()




    def guardar_en_parquet(self, df_transformado = None, nombre_archivo="currencies_transformadas.parquet"):

        """
        Guarda el DataFrame transformado en formato Parquet en la capa silver.
        """

        logger = setup_logger("o3_transformation_logs/guardar_parquet.log")

        logger.info(f"INICIO transformacion a parquete.")

        if df_transformado is None:
            df_transformado = self.transformar()

        try:

            path_salida = os.path.join(self.silver_path, nombre_archivo)

            df_transformado.to_parquet(path_salida, index=False)

            logger.info(f"FIN transformacion. ✅ Archivo guardado en Silver: {path_salida}")

        except Exception as e:

            logger.error(f"FIN transformacion. ❌ Error al guardar el archivo Parquet: {e}")
