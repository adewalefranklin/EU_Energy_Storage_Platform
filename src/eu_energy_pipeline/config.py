import os
from dotenv import load_dotenv
from src.eu_energy_pipeline.exceptions import ConfigError

load_dotenv()

class Config:
    required_variables = ['AGSI_API_KEY', 'AGSI_BASE_URL']

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

                
    