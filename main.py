from meli_project.logic.o1_extraction.api_wb import CurrencyExtractor
from meli_project.logic.o2_cleaning.clean_json import DFsCurrencies
from meli_project.logic.o3_transformation.transformaciones import CurrencyTransformer
from meli_project.logic.o4_modeling.modelado import CurrencyModeler
from meli_project.logic.o5_serving.carga_gcp import CargadorBigQuery
from meli_project.logic.utils.utils import *



def main():


    """
    Pipeline ETL completo para normalizar cotizaciones de monedas extranjeras,
    exportarlas a CSV y Parquet, y subirlas a BigQuery.
    """

    logger = setup_logger('o6_main_logs/main_etl.log')

    logger.info("🚀 INICIO PIPELINE ETL - Cotizaciones de Monedas")


    try:
        logger.info("📥 Extracción de datos desde AwesomeAPI...")

        extractor = CurrencyExtractor()

        resultado = extractor.obtener_todos_los_datos()

        logger.info(f"✅ Resultado extracción: {resultado}")

    except Exception as e:

        logger.error(f"❌ Error en extracción de monedas: {e}")

    try:

        logger.info("Limpieza y unión de JSONs...")

        cleaner = DFsCurrencies()

        df_unificado = cleaner.obtener_df_unificado()

        logger.info(f"✅ DF unificado generado. Registros: {len(df_unificado)}")

    except Exception as e:

        logger.error(f"❌ Error en limpieza/unificación: {e}")

        df_unificado = None

    if df_unificado is not None:

        try:

            logger.info("⚙️ Transformación de datos y guardado en Silver (.parquet)...")
            transformador = CurrencyTransformer(df_unificado)

            transformador.guardar_en_parquet()
            logger.info("✅ Transformación completada y guardada.")

        except Exception as e:

            logger.error(f"❌ Error en transformación de datos: {e}")

    try:

        logger.info("📦 Modelado: copia a GOLD y exportación a CSV...")


        modelador = CurrencyModeler()

        modelador.procesar_modelado_completo()

        logger.info("✅ Archivo Parquet copiado y CSV generado en GOLD.")

    except Exception as e:

        logger.error(f"❌ Error en modelado/exportación a GOLD: {e}")


    try:

        logger.info("☁️ Carga del archivo Parquet a Google BigQuery...")

        cargador = CargadorBigQuery()

        cargador.cargar_todas_tablas_gold()
        logger.info("✅ Datos cargados correctamente a BigQuery.")

    except Exception as e:

        logger.error(f"❌ Error al subir a BigQuery: {e}")

    logger.info("🏁 FIN PIPELINE ETL finalizado correctamente.")


if __name__ == "__main__":

    main()
