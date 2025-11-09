from dataclasses import dataclass

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def create_config_dict(prefix: str) -> SettingsConfigDict:
    return SettingsConfigDict(
        env_prefix=f'{prefix}_',
        env_nested_delimiter='_',
        env_nested_max_split=1,
        extra='ignore',
    )


class PostgresSettings(BaseSettings):
    model_config = create_config_dict('postgres')

    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    @property
    def url(self):
        password = self.password.get_secret_value()
        return f'postgresql+asyncpg://{self.user}:{password}@{self.host}:{self.port}/{self.name}'


@dataclass(frozen=True)
class Config:
    postgres: PostgresSettings


# noinspection PyArgumentList
config = Config(
    postgres=PostgresSettings(),
)
