from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoFix AI"
    app_version: str = "0.1.0"

    github_token: str = ""

    database_url: str = (
        "postgresql+psycopg://"
        "repofix:repofix@localhost:5432/repofix"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()