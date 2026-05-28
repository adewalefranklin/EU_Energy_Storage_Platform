from eu_energy_pipeline.pipeline import AgsiPipeline
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.logger import get_logger


def main():
    Config.validate()

    logger = get_logger(__name__)

    logger.info("Starting the AGSI pipeline.")

    pipeline = AgsiPipeline()

    endpoint = "storage"

    params = {
        "country": "DE",
        "from": "2026-01-01",
        "to": "2026-06-27",
    }

    pipeline.run(endpoint, params, ingestion_date="2026-06-27")


if __name__ == "__main__":
    main()
