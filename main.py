from eu_energy_pipeline.pipeline import AgsiPipeline
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.logger import get_logger


def main():
    Config.validate()
    logger = get_logger(__name__)
    logger.info("Starting the AGSI pipeline.")

    pipeline = AgsiPipeline()

    targets = [
        {
            "country": "DE",
            "company_eic": "21X000000001160J",
            "facility_eic": "21Z000000000271O",
        },
        {
            "country": "DE",
            "company_eic": "21X000000001160J",
            "facility_eic": "21Z000000000271O",
        },
        {
            "country": "AT",
            "company_eic": "25X-OMVGASSTORA5",
            "facility_eic": "21W000000000081Y",
        },
        {
            "country": "DE",
            "company_eic": "21X000000001160J",
            "facility_eic": "21Z000000000271O",
        },
        {
            "country": "DE",
            "company_eic": "21X000000001160J",
            "facility_eic": "21Z000000000271O",
        },
    ]
    for target in targets:

        s3_key = pipeline.run(
            start_date="2026-05-01",
            end_date="2026-05-05",
            country=target["country"],
            company=target["company_eic"],
            facility=target["facility_eic"],
            ingestion_date="2026-05-26",
        )

        logger.info(
            f"Loaded dataset for "
            f"{target['country']} | "
            f"{target['company_eic']} | "
            f"{target['facility_eic']} "
            f"-> {s3_key}"
        )


if __name__ == "__main__":
    main()
