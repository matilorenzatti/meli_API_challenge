import os
import json
import pandas as pd
from meli_project.logic.utils.utils import *




class DFsCurrencies:



    def __init__(self):

        """
        Define la ruta a la capa bronze donde se encuentran los JSONs.
        """

        self.bronze_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o1_bronze")
        )



    def listar_jsons_validos(self):

        """
        Lista todos los archivos .json válidos en la carpeta bronze.
        """

        logger = setup_logger('o3_transformation_logs/listar_jsons_validos.log')

        logger.info("INICIO listado de JSONs válidos")

        archivos_validos = []

        for file in os.listdir(self.bronze_path):

            if file.endswith(".json"):

                full_path = os.path.join(self.bronze_path, file)

                try:

                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        if isinstance(data, list) and len(data) > 0:
                            archivos_validos.append(full_path)
                            logger.info(f"FIN listado. ✅ {file} es válido.")

                        else:

                            logger.warning(f"FIN listado. ⚠️ {file} no contiene una lista o está vacío.")

                except Exception as e:
                    logger.error(f"FIN listado. ❌ Error al procesar {file}: {e}")

        return archivos_validos



    def convertir_json_a_df(self, json_path: str) -> pd.DataFrame:

        """
        Convierte un archivo JSON individual en un DataFrame normalizado.
        """

        logger = setup_logger("o3_transformation_logs/convertir_json_a_df.log")

        file_name = os.path.basename(json_path)

        logger.info(f"INICIO proceso {file_name}")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list) or len(data) == 0:
                logger.warning(f"FIN proceso. ⚠️ {file_name} vacío o no es lista.")
                return pd.DataFrame()

            pair = file_name.replace(".json", "")

            header = data[0]  # contiene code, codein, name, create_date, etc.

            rows = data[1:] if len(data) > 1 else []

            # Normalizamos los valores históricos
            df = pd.DataFrame(rows)

            # En cada fila agregamos los datos de contexto
            df["pair"] = pair
            df["code"] = header.get("code")
            df["codein"] = header.get("codein")
            df["name"] = header.get("name")
            df["create_date"] = header.get("create_date")
            df["source_file"] = file_name

            logger.info(f"FIN proceso. ✅ {file_name} convertido con {len(df)} registros.")
            return df

        except Exception as e:
            logger.error(f"FIN proceso. ❌ Error procesando {file_name}: {e}")
            return pd.DataFrame()




    def obtener_df_unificado(self):

        """
        Convierte todos los JSONs válidos en un único DataFrame consolidado.
        """

        logger = setup_logger("o3_transformation_logs/unificar_todo_df.log")

        logger.info("INICIANDO proceso de unificación")

        archivos = self.listar_jsons_validos()

        df_final = pd.DataFrame()

        for path in archivos:

            df = self.convertir_json_a_df(path)

            if not df.empty:
                df_final = pd.concat([df_final, df], ignore_index=True)

        logger.info(f"FIN proceso. ✅ Unificación finalizada. Total de registros: {len(df_final)}")

        return df_final
