import os
import json
import requests
from meli_project.logic.utils.utils import *
from meli_project.params import *





class CurrencyExtractor:



    def __init__(self, numero_dias: int = 180):

        """
        Constructor de la clase. Define los parámetros básicos de la API.
        """

        self.numero_dias = numero_dias

        self.base_url = "https://economia.awesomeapi.com.br/json/daily"

        self.available_url = "https://economia.awesomeapi.com.br/json/available"


        # Ruta donde se guardarán los JSON originales (bronze)
        self.bronze_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../data/o1_bronze")
        )
        os.makedirs(self.bronze_path, exist_ok=True)




    def get_currency_pairs_brl(self) -> list:

        """
        Obtiene todos los pares de monedas disponibles desde la API,
        y filtra solo los que terminan en '-BRL'.
        """

        logger = setup_logger("o1_extraction_logs/available_pairs.log")

        logger.info("INICIANDO consulta de pares de monedas disponibles...")

        headers = {
            "Accept": "application/json",
            "x-api-key": API_KEY_AWESOME
        }



        try:
            response = requests.get(self.available_url, headers=headers)


            if response.status_code == 200:

                data = response.json()

                pares_brl = [k for k in data.keys() if k.endswith("BRL")]

                logger.info(f"FIN consulta. ✅ {len(pares_brl)} pares BRL obtenidos.")

                return pares_brl

            else:

                logger.error(f"FIN consulta. ❌ Error al obtener pares: {response.status_code}")

                return []

        except Exception as e:

            logger.critical(f"FIN consulta. ❌ Excepción al obtener pares: {str(e)}")

            return []




    def descargar_json_moneda(self, pair: str):

        """
        Descarga el JSON de la API para un par de moneda específico
        y lo guarda en la capa bronze.
        """

        logger = setup_logger(f"o1_extraction_logs/PAIRS/{pair}.log")

        url = f"{self.base_url}/{pair}/{self.numero_dias}"

        logger.info(f"INICIO de descarga de datos para {pair}...")

        try:

            response = requests.get(url)

            if response.status_code == 200:

                output_path = os.path.join(self.bronze_path, f"{pair}.json")

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, indent=4, ensure_ascii=False)

                logger.info(f"FIN descarga. ✅ JSON guardado en: {output_path}")

                return output_path

            else:

                logger.error(f"FIN descarga. ❌ Error {response.status_code} al descargar {pair}")


        except Exception as e:

            logger.critical(f"FIN descarga. ❌ Error inesperado al descargar {pair}: {str(e)}")






    def obtener_todos_los_datos(self, pares: list = None):

        """
        Descarga todos los pares BRL disponibles y guarda sus datos en bronze.
        Si se pasa una lista personalizada, solo se descargan esos pares.
        """

        logger = setup_logger("o1_extraction_logs/descarga_masiva.log")

        logger.info("INICIANDO descarga masiva de monedas...")

        if pares is None:
            pares = self.get_currency_pairs_brl()


        descargados = []
        errores = []

        for pair in pares:

            try:
                path = self.descargar_json_moneda(pair)

                if path:
                    descargados.append(pair)

                else:
                    errores.append(pair)

            except Exception as e:

                logger.error(f"❌ Error inesperado al procesar {pair}: {e}")

                errores.append(pair)

        logger.info(f"✅ Monedas descargadas: {len(descargados)}")

        if errores:

            logger.warning(f"⚠️ Monedas con error: {errores}")

            return f"FIN descarga. ❌ Error: Fallaron {len(errores)} de {len(pares)} pares."

        else:

            return f"FIN descarga. ✅ Todos los pares descargados correctamente."
