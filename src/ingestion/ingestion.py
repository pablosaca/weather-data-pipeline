from typing import Tuple, Dict, Any, Literal
from datetime import date, timedelta
from abc import ABC, abstractmethod
import requests

import pandas as pd


class DataIngestion(ABC):

    def __init__(self, config_file: Dict, data: str):

        available_data = ["forecast", "archive"]
        if data not in available_data:
            raise ValueError(f"Valor incorrecto. Solo disponible {available_data}")

        self.data = data

        self.download_params = config_file["params"]
        self.params = {
            "latitude": self.download_params["location"]["latitude"],
            "longitude": self.download_params["location"]["longitude"],
            self.download_params["type"]: ",".join(self.download_params["features"]),
            "timezone": self.download_params["timezone"]
        }

    def get_request(self) -> pd.DataFrame:

        url, params = self._get_url_params(self.params, self.data)
        response = requests.get(url, params=params, timeout=10)

        if not response.status_code == 200:
            raise ValueError("Incorrecto")

        output = response.json()

        temperature = self.download_params["features"][0]
        precipitation = self.download_params["features"][1]
        df = pd.DataFrame({
            "date": output[self.download_params["type"]]["time"],
            "temperature_2m_max": output[self.download_params["type"]][temperature],
            "precipitation_sum": output[self.download_params["type"]][precipitation]
        })
        return df

    @abstractmethod
    def _get_url_params(
            self,
            params: Dict[str, Any],
            data: str
    ) -> Tuple[str, Dict[str, Any]]:

        pass


class ForecastIngestion(DataIngestion):

    def __init__(self, config_file: Dict[str, Any], data: str):

        super().__init__(config_file, data)

    def _get_url_params(
            self,
            params: Dict[str, Any],
            data: Literal["forecast", "archive"] = "forecast"
    ) -> Tuple[str, Dict[str, Any]]:

        url = f"https://api.open-meteo.com/v1/{data}"
        params["forecast_days"] = self.download_params["forecast_days"]
        return url, params


class ArchiveIngestion(DataIngestion):

    def __init__(self, config_file: Dict[str, Any], data: str, historical_data: bool = False):

        super().__init__(config_file, data)
        self.historical_data = historical_data

    def _get_url_params(
            self,
            params: Dict[str, Any],
            data: Literal["forecast", "archive"] = "archive"
    ) -> Tuple[str, Dict[str, Any]]:

        url = f"https://{data}-api.open-meteo.com/v1/{data}?"

        if self.historical_data:
            params["start_date"] = self.download_params["start_date"].strftime(format="%Y-%m-%d")
        else:
            params["start_date"] = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        params["end_date"] = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        return url, params
