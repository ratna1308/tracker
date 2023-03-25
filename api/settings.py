from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # General Settings
    enable_metrics: bool = Field(
        True,
        title="Enable metrics",
        description="Expose prometheus metrics if set to True. Default: True",
        env="ENABLE_METRICS"
    )
    # MongoDB Settings
    mongo_connection_string: str = Field(
        "mongodb://localhost:27017",
        title="MongoDB Films Connection string",
        description="The connection string for the MongoDB database.",
        env="MONGODB_CONNECTION_STRING",
    )
    mongo_database_name: str = Field(
        "Film_track_db",
        title="MongoDB Films Database name",
        description="The database name for the MongoDB Films database.",
        env="MONGODB_DATABASE_NAME",
    )

    def __hash__(self) -> int:
        # NOTE - we are having to override `hash` function because `Settings`
        # is un-hashable type.
        return 1


@lru_cache()
def settings_instance():
    """
    NOTE - lru_cache decorations saves time in IO bound operations.

    Settings instance to used as a Fast API dependency.
    """
    return Settings()
