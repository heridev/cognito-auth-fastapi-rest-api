from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    dynamodb_table_name: str
    sns_topic_arn: str
    cors_origins: str
    postmark_server_token: str

    class Config:
        env_file = ".env"


settings = Settings()
