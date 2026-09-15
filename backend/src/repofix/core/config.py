from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RepoFix AI"
    app_version: str = "0.1.0"

    github_token: str = ""

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"

    use_mock_llm: bool = True
    
    database_url: str = (
        "postgresql+psycopg://"
        "repofix:repofix@localhost:5432/repofix"
    )

    model_config = SettingsConfigDict(
        env_file=r"C:\Users\Rahul\RepoFix-AI\backend\.env",
        env_file_encoding="utf-8",
        extra="ignore",
)


settings = Settings()