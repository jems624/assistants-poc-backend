from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_assistant_id: str
    browserless_token: str
    serpapi_api_key: str

settings = Settings(_env_file='.env', _env_file_encoding='utf-8') # type: ignore