from eu_energy_pipeline.pipeline import AgsiPipeline
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.logger import get_logger


def main():
    Config.validate()
    logger = get_logger(__name__)
    logger.info("Starting the AGSI pipeline.")

    pipeline = AgsiPipeline()

    endpoint = "facilities"

    params = {"country": "DE"}

    pipeline.run(endpoint, params)


if __name__ == "__main__":
    main()
