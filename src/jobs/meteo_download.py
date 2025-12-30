from datetime import date

from src.utils.utils import load_config_file, get_global_path
from src.database.db_connect import DataBaseProjectSQLAlchemy
from src.ingestion.ingestion import ForecastIngestion, ArchiveIngestion
from src.utils.logger import get_logger


logger = get_logger()


def main():

    today = date.today().strftime('%Y-%m-%d')
    logger.info(f"Inicio Job Ingesta - Ejecución del día {today}")
    # ruta a añadir (directorio
    config_file_path = "config_file/data.yml"

    base_path = get_global_path()
    config_file_path = base_path / config_file_path  # se añade el directorio con el fichero donde está el fichero yaml
    config_file = load_config_file(config_file_path)  # lee fichero de configuración

    # se instancia la clase de DB
    db = DataBaseProjectSQLAlchemy(db_name=config_file["database"]["database_name"])
    db.db_connect()  # conecta la database (si no está creada, se crea en el momento)

    archive_data = "archive"
    archive_table_exits = db.table_exists(table_name=config_file["database"]["tables"][archive_data]["table_name"])

    if not archive_table_exits:
        archive_ingestion = ArchiveIngestion(config_file=config_file, data=archive_data, historical_data=True)
        archive_df = archive_ingestion.get_request()
        logger.info("Descarga datos históricos")
    else:
        archive_ingestion = ArchiveIngestion(config_file=config_file, data=archive_data, historical_data=False)
        archive_df = archive_ingestion.get_request()
        logger.info("Descarga datos históricos - ampliación")

    db.write_table(
        archive_df, config_file["database"]["tables"][archive_data]["table_name"], "append"
    )
    logger.info(f"Los datos históricos son escritos en {archive_data}")

    forecast_data = "forecast"
    forecast_ingestion = ForecastIngestion(config_file=config_file, data=forecast_data)
    forecast_df = forecast_ingestion.get_request()
    logger.info("Descarga predicciones")

    db.write_table(
        forecast_df, config_file["database"]["tables"][forecast_data]["table_name"], "append"
    )
    logger.info(f"Los datos predichos son escritos en {forecast_data}")

    logger.info(f"Job de Ingesta finalizado - Ejecución del día {today}")


if __name__ == "__main__":
    main()
