import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from meli_project.params import *
from meli_project.logic.utils.utils import *




class CargadorBigQuery:


    def __init__(self, dataset="dataframes_meli", project_id="reportes-bedoya-389011"):

        self.logger = setup_logger('o5_serving_logs/carga_bigquery.log')

        # Inicializar credenciales

        self.credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
        self.project_id = project_id
        self.dataset = dataset

        # Ruta de archivos .parquet en gold
        self.gold_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o3_gold")
        )




    def cargar_archivo(self, nombre_archivo):


        """
        Carga un archivo .parquet específico a BigQuery.
        """

        path = os.path.join(self.gold_path, nombre_archivo)

        if not os.path.exists(path):
            self.logger.error(f"❌ No se encontró el archivo {nombre_archivo}")
            return f"❌ No se encontró el archivo {nombre_archivo}"

        try:
            df = pd.read_parquet(path)

            tabla_destino = nombre_archivo.replace(".parquet", "")

            df.to_gbq(
                destination_table=f"{self.dataset}.{tabla_destino}",
                project_id=self.project_id,
                credentials=self.credentials,
                if_exists="replace"
            )

            self.logger.info(f"✅ Archivo '{nombre_archivo}' cargado con éxito en '{self.dataset}.{tabla_destino}'.")

        except Exception as e:

            self.logger.error(f"❌ Error al cargar '{nombre_archivo}': {e}")



    def cargar_todas_tablas_gold(self):

        """
        Carga todos los archivos .parquet desde la carpeta gold a BigQuery.
        """

        self.logger.info("INICIO CARGA de archivos .parquet a BigQuery")


        if not os.path.exists(self.gold_path):

            self.logger.error("❌ Carpeta GOLD no encontrada.")

            return "❌ Carpeta GOLD no encontrada."


        archivos = [f for f in os.listdir(self.gold_path) if f.endswith(".parquet")]


        if not archivos:

            self.logger.critical("⚠️ No se encontraron archivos .parquet en GOLD.")

            return "⚠️ No se encontraron archivos .parquet en GOLD."


        for archivo in archivos:

            self.cargar_archivo(archivo)

        self.logger.info("FIN CARGA de tablas en BigQuery.")
