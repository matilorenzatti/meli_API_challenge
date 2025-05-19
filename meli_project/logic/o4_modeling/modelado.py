import os
import shutil
import pandas as pd
from meli_project.logic.utils.utils import *



class CurrencyModeler:

    def __init__(self, nombre_parquet="currencies_transformadas.parquet"):

        """
        Clase que gestiona el modelado de datos:
        - Copia el archivo .parquet desde Silver a Gold
        - Convierte el archivo .parquet a .csv y lo guarda en Gold
        """

        self.nombre_parquet = nombre_parquet

        self.silver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o2_silver")
        )

        self.gold_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o3_gold")
        )

        os.makedirs(self.gold_path, exist_ok=True)



    def copiar_parquet_a_gold(self):

        """
        Copia el archivo .parquet desde Silver a Gold sin modificarlo.
        """

        logger = setup_logger("o4_modeling_logs/copiar_parquet_a_gold.log")

        logger.info("INICIO copia del archivo Parquet desde Silver a Gold...")


        source_path = os.path.join(self.silver_path, self.nombre_parquet)
        target_path = os.path.join(self.gold_path, self.nombre_parquet)


        try:

            if not os.path.isfile(source_path):

                logger.error(f"❌ Archivo no encontrado: {source_path}")

                return f"❌ Archivo no encontrado: {source_path}"


            shutil.copyfile(source_path, target_path)

            logger.info(f"✅ Archivo copiado correctamente a: {target_path}")

        except Exception as e:

            logger.error(f"❌ Error al copiar el archivo Parquet: {e}")



    def convertir_a_csv(self):

        """
        Carga el archivo .parquet desde Silver, lo convierte a .csv y lo guarda en Gold.
        """

        logger = setup_logger("o4_modeling_logs/convertir_a_csv.log")

        logger.info("INICIO conversión Parquet → CSV...")

        parquet_file = os.path.join(self.silver_path, self.nombre_parquet)

        try:

            if not os.path.isfile(parquet_file):

                logger.error(f"❌ Archivo no encontrado: {parquet_file}")

                return f"❌ Archivo no encontrado: {parquet_file}"

            df = pd.read_parquet(parquet_file)

            csv_name = self.nombre_parquet.replace(".parquet", ".csv")

            csv_path = os.path.join(self.gold_path, csv_name)

            df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")

            logger.info(f"✅ CSV generado correctamente en: {csv_path}")

        except Exception as e:

            logger.error(f"❌ Error al convertir a CSV: {e}")



    def procesar_modelado_completo(self):

        """
        Ejecuta toda la etapa de modelado:
        - Copia el archivo .parquet a Gold
        - Genera el archivo .csv en Gold
        """

        logger = setup_logger("o4_modeling_logs/procesar_modelado_completo.log")

        logger.info("INICIO del proceso completo de modelado...")

        self.copiar_parquet_a_gold()

        self.convertir_a_csv()

        logger.info("FIN del proceso de modelado.")
