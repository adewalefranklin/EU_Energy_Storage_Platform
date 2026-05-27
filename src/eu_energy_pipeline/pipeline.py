from eu_energy_pipeline.extract import Extractor
from eu_energy_pipeline.config import Config
from eu_energy_pipeline.load import S3Loader
from eu_energy_pipeline.logger import get_logger

logger = get_logger(__name__)


class AgsiPipeline:
    def __init__(self):

        self.extractor = Extractor()

        self.loader = S3Loader(
            aws_access_key_id=Config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=Config.get("AWS_SECRET_ACCESS_KEY"),
            aws_region=Config.get("AWS_REGION"),
            prefix=Config.get("PREFIX"),
            aws_bucket_name=Config.get("AWS_BUCKET_NAME"),
        )

    def run(self, endpoint, params, ingestion_date):
        logger.info(f"Starting AGSI+ pipeline for endpoint: {endpoint}")

        data = self.extractor.fetch_data(
            endpoint=endpoint,
            params=params,
        )

        s3_key = self.loader.s3_uploader(
            data=data,
            ingestion_date=ingestion_date,
            endpoint=endpoint,
        )

        logger.info(f"Data loaded into S3 with key: {s3_key}")

        return s3_key
