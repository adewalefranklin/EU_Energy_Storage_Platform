import os
from dotenv import load_dotenv
from eu_energy_pipeline.exceptions import ConfigError

load_dotenv()


class Config:
    required_variables = [
        "AGSI_API_KEY",
        "AGSI_BASE_URL",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "AWS_BUCKET_NAME",
        "PREFIX",
    ]

    @classmethod
    def get(cls, var_name):
        value = os.getenv(var_name)
        if not value:
            raise ConfigError(f"Variable not found: {var_name}")
        return value

    @classmethod
    def validate(cls):
        for var in cls.required_variables:
            cls.get(var)
