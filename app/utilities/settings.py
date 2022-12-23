from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME")
    app_description: str = Field(env="APP_DESC")
    app_version: str = Field(env="APP_VERSION")
    redis_endpoint: str = Field(env="REDIS_ENDPOINT")
    redis_port: str = Field(env="REDIS_PORT")
    redis_namespace: str = Field(env="REDIS_NAMESPACE")
    redis_auth: str = Field(env="REDIS_AUTH")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
