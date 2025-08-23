from pydantic import BaseModel, ValidationError
from dataclasses import dataclass
from abc import ABC
from typing import Dict, Type
import yaml

# feedsnooplyze modules
from feedsnooplyze.notifier import NotifierType




### General Config Classess

@dataclass
class GeneralConfig():
    pooling_time: int


### Persistence Config Classess

class DuckDBConfig(BaseModel):
    persistence: str
    db_file_path: str


class SQLiteConfig(BaseModel):
    persistence: str
    db_file_path: str

class PostgreSQLConfig(BaseModel):
    persistence: str
    host: str
    port: str
    user: str
    password: str
    database: str

class MySQLConfig(BaseModel):
    persistence: str
    host: str
    port: str
    user: str
    password: str
    database: str

class MsSQLServerConfig(BaseModel):
    persistence: str
    host: str
    port: str
    user: str
    password: str
    database: str

class OracleConfig(BaseModel):
    persistence: str
    host: str
    port: str
    user: str
    password: str
    service_name: str


PERSISTENCE_CONFIG_MODELS: Dict[str, Type[BaseModel]] = {
    "sqlite": SQLiteConfig,
    "duckdb": DuckDBConfig,
    "postgresql": PostgreSQLConfig,
    "mysql": MySQLConfig,
    "mssqlserver": MsSQLServerConfig,
    "oracle": OracleConfig
}


# Notification Config Classess

@dataclass
class NotificationConfigBase(ABC):
    pass

@dataclass
class ConsoleNotificationConfig(NotificationConfigBase):
    pass

@dataclass
class FlatFileNotificationConfig(NotificationConfigBase):
    file_path: str

@dataclass
class EmailNotificationConfig(NotificationConfigBase):
    email_address: str
    email_password: str
    recipients: str

@dataclass
class TelegramNotificationConfig(NotificationConfigBase):
    token: str
    chat_id: str



@dataclass
class ConfigReader:
    path_to_file: str
    
    def read(self) -> str:
        with open(self.path_to_file) as f:
            return f.read()


class ConfigLoader:
    def __init__(self, reader: ConfigReader):
        self.reader = reader


    def load_config(self):
        yaml_str = self.reader.read()
        return self._parse_config(yaml_str)
    

    def _create_persistence_config(self, data: dict) -> BaseModel:
        type = data.get("persistence").lower()
        
        if type not in PERSISTENCE_CONFIG_MODELS:
            raise ValueError(f"Unsupported persistence type: {type}")
        
        model = PERSISTENCE_CONFIG_MODELS[type.lower()]

        try:    
            return model(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration for {type}: {e}")  
        


    def _create_notification_config(self, data: dict) -> NotificationConfigBase:
        type_ = data.get("notification_type").upper()

        if type_ == NotifierType.CONSOLE:
            return ConsoleNotificationConfig()
        elif type_ == NotifierType.FLATFILE:
            return FlatFileNotificationConfig(file_path=data["file_path"])
        elif type_ == NotifierType.EMAIL:
            return EmailNotificationConfig(
                email_address=data["email_address"],
                email_password=data["email_password"],
                recipients=data["recipients"]
            )
        elif type_ == NotifierType.TELEGRAM:
            return TelegramNotificationConfig(
                token=data["token"],
                chat_id=data["chat_id"]
            )
        else:
            raise ValueError(f"Unsupported notification type: {type_.upper()}")
    

    def _parse_config(self, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        
        # General config
        general = GeneralConfig(pooling_time=data["GeneralConfig"]["pooling_time"])

        # Persistence config
        persistence = self._create_persistence_config(data["PersistenceConfig"])

        # Notification configs
        notifications = [self._create_notification_config(n) for n in data.get("NotificationConfig", [])]

        return general, persistence, notifications
    