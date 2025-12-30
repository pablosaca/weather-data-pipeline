from typing import Literal

import pandas as pd

from src.database.db_connect import DataBaseProjectSQLAlchemy


def write_model_data_to_db(
        df: pd.DataFrame,
        config_file: dict,
        table_name: str,
        written_type: Literal["append", "replace"]
) -> None:
    """
    Escritura en la database del las tablas del modelo (se usa para entrenamiento y predicción)
    """

    if table_name in ["weather_training_model", "weather_prediction_model"]:
        # en el df se incluye una variable temporal -> timestamp para que quede la traza
        df["Date_Timestamp"] = pd.Timestamp.now()

    # se instancia la clase de DB
    db = DataBaseProjectSQLAlchemy(db_name=config_file["database"]["database_name"])
    db.db_connect()  # conecta la database (si no está creada, se crea en el momento)
    db.write_table(df, table_name, written_type)
