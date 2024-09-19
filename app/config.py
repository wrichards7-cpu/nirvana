import logging
import os
import yaml

from pydantic_settings  import BaseSettings

class Settings(BaseSettings):

    # auth
    default_algoritm: int = 1

    class Config:
        env_file = ".env"  # Load settings from a .env file


APP_SETTINGS = {}