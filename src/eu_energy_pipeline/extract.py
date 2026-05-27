import requests
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.exceptions import ExtractError
from eu_energy_pipeline.logger import get_logger


class Extractor:
    def __init__(self):
        self.api_key = Config.get("AGSI_API_KEY")
        self.base_url = Config.get("AGSI_BASE_URL")
        self.logger = get_logger(__name__)

    def fetch_data(self, endpoint, params):

        self.logger.info(f"Fetching AGSI+ data from endpoint: {endpoint}")

        url = f"{self.base_url}/{endpoint}"

        headers = {"x-key": self.api_key}

        try:
            response = requests.get(url=url, headers=headers, params=params, timeout=30)

            response.raise_for_status()

            data = response.json()

            self.logger.info(f"Successfully fetched AGSI+ {endpoint} data")

            return data

        except Exception as e:
            raise ExtractError(f"Failed to fetch AGSI+ {endpoint} data: {str(e)}")
