from meli_project.logic.o1_extraction.api_wb import DataWB
from meli_project.logic.o2_cleaning.clean_json import DFsWB
from meli_project.logic.o3_transformation.transformaciones import TransformadorWB
from meli_project.logic.o4_modeling.modelado import ModeladorWB
from meli_project.logic.o5_serving.carga_gcp import CargadorBigQuery
from meli_project.logic.utils.utils import *




def main():

    """
    ETL completo
    """

    logger = setup_logger('o6_main_logs/main.log')

    logger.info("INICIO PIPELINE ETL completo.")




    try:

        logger.info("📥 Extracción de datos para ARG...")

        wb_arg = DataWB()
        resultado_arg = wb_arg.obtener_all_data()
        logger.info(f"✅ Resultado ARG: {resultado_arg}")

    except Exception as e:

        logger.error(f"❌ Error en la extracción de ARG: {e}")




    try:

        logger.info("🌍 Extracción de datos para WLD...")

        wb_wld = DataWB(ref_area="WLD")

        indicadores_validos_wld = cargar_indicadores_validos_arg()
        resultado_wld = wb_wld.obtener_all_data(indicadores_validos_wld)

        logger.info(f"✅ Resultado WLD: {resultado_wld}")

    except Exception as e:
        logger.error(f"❌ Error en la extracción de WLD: {e}")




    try:
        logger.info("🧼 Iniciando limpieza y conversión a DataFrames...")
        limpiador = DFsWB()
        dfs_dict = limpiador.obtener_todos_df()
        logger.info(f"✅ Se obtuvieron {len(dfs_dict)} DataFrames válidos.")

    except Exception as e:
        logger.error(f"❌ Error en limpieza de datos: {e}")




    try:
        logger.info("⚙️ Iniciando transformación...")
        transformador = TransformadorWB(dfs_dict)
        transformador.transformar_todos()
        logger.info("✅ Transformación completada.")

    except Exception as e:
        logger.error(f"❌ Error en transformación: {e}")




    try:
        logger.info("📦 Construyendo modelo dimensional (capa GOLD)...")
        modelador = ModeladorWB()
        modelador.ejecutar_pipeline_gold_dimensional()
        logger.info("✅ Tablas del modelo dimensional generadas y guardadas en GOLD.")

    except Exception as e:
        logger.error(f"❌ Error en modelado GOLD: {e}")




    try:
        logger.info("☁️ Iniciando carga en BigQuery...")
        cargador = CargadorBigQuery()
        cargador.cargar_todas_tablas_gold()
        logger.info("✅ Todas las tablas de GOLD subidas a BigQuery.")

    except Exception as e:
        logger.error(f"❌ Error al subir a BigQuery: {e}")

    try:
        convertir_parquet_a_csv()
        logger.info("✅ DF de gold convertidos a CSV con exito.")

    except Exception as e:
        logger.error(f"❌ Error al convertir los df a CSV: {e}")



    logger.info("FIN PIPELINE ETL finalizado.")


if __name__ == "__main__":

    main()
