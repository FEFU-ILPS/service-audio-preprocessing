from pydantic_settings import BaseSettings, SettingsConfigDict

from .graylog import GraylogConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PREPROCESSING_")

    # * Вложенные группы настроек
    graylog: GraylogConfiguration = GraylogConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = True
    SERVICE_NAME: str = "ilps-service-audio-preprocessing"


configs = ProjectConfiguration()

__all__ = ("configs",)
