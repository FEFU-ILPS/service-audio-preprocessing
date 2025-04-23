from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MANAGER_")

    # * Опциональные переменные
    DEBUG_MODE: bool = True
    SERVICE_NAME: str = "ilps-service-task-manager"


configs = ProjectConfiguration()

__all__ = ("configs",)
