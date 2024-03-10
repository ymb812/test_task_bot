from pydantic import BaseModel, SecretStr, fields
from pydantic_settings import SettingsConfigDict


class BotSettings(BaseModel):
    bot_token: SecretStr = fields.Field(max_length=100, alias='TELEGRAM_BOT_TOKEN')
    payments_provider_token: SecretStr = fields.Field(max_length=100, alias='PAYMENTS_PROVIDER_TOKEN')
    admin_password: SecretStr = fields.Field(max_length=100, alias='ADMIN_PASSWORD')
    required_chat_id: str = fields.Field(alias='REQUIRED_CHAT_ID')
    required_channel_id: str = fields.Field(alias='REQUIRED_CHANNEL_ID')
    orders_per_msg: int = fields.Field(alias='ORDERS_PER_MSG', default=5)


class Broadcaster(BaseModel):
    mailing_batch_size: int = fields.Field(alias='MAILING_BATCH_SIZE', default=25)
    broadcaster_sleep: int = fields.Field(alias='BROADCASTER_SLEEP', default=1)


class Dialogues(BaseModel):
    categories_per_page_height: int = fields.Field(alias='CATEGORIES_HEIGHT')
    categories_per_page_width: int = fields.Field(alias='CATEGORIES_WIDTH')
    products_per_page_height: int = fields.Field(alias='PRODUCTS_HEIGHT')
    products_per_page_width: int = fields.Field(alias='PRODUCTS_WIDTH')


class AppSettings(BaseModel):
    prod_mode: bool = fields.Field(alias='PROD_MODE', default=False)
    logs_file: str = fields.Field(alias='LOGS_FILE', default='logs_file.txt')
    excel_file: str = fields.Field(alias='EXCEL_FILE', default='Users stats.xlsx')


class PostgresSettings(BaseModel):
    db_user: str = fields.Field(alias='POSTGRES_USER')
    db_host: str = fields.Field(alias='POSTGRES_HOST')
    db_port: int = fields.Field(alias='POSTGRES_PORT')
    db_pass: SecretStr = fields.Field(alias='POSTGRES_PASSWORD')
    db_name: SecretStr = fields.Field(alias='POSTGRES_DATABASE')


class RedisSettings(BaseModel):
    redis_host: str = fields.Field(alias='REDIS_HOST')
    redis_port: int = fields.Field(alias='REDIS_PORT')
    redis_name: str = fields.Field(alias='REDIS_NAME')


class Settings(
    BotSettings,
    AppSettings,
    PostgresSettings,
    Broadcaster,
    Dialogues,
    RedisSettings
):
    model_config = SettingsConfigDict(extra='ignore')
