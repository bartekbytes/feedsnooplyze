from dataclasses import dataclass
from abc import ABC
from typing import Optional
import yaml

from persistence import PersistenceEngineType
from notifier import NotifierType


### General Config Classess

@dataclass
class GeneralConfig:
    pooling_time: int
    author: Optional[str] = "snooplyze"



### Persistence Config Classess

@dataclass
class PersistenceConfigBase(ABC):
    persistence: str

@dataclass
class DuckDBConfig(PersistenceConfigBase):
    persistence: str
    db_file_path: str

@dataclass
class SQLiteConfig(PersistenceConfigBase):
    persistence: str
    db_file_path: str

@dataclass
class PostgreSQLConfig(PersistenceConfigBase):
    persistence: str
    connection_string: str

@dataclass
class MySQLConfig(PersistenceConfigBase):
    persistence: str
    host: str
    port: str
    user: str
    password: str
    database: str



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
    

    def _create_persistence_config(self, data: dict) -> PersistenceConfigBase:
        type = data.get("persistence").upper()
        
        if type == PersistenceEngineType.POSTGRESQL:
            return PostgreSQLConfig(persistence=PersistenceEngineType.POSTGRESQL, connection_string=data["connection_string"])
        elif type == PersistenceEngineType.DUCKDB:
            return DuckDBConfig(persistence=PersistenceEngineType.DUCKDB, db_file_path=data["db_file_path"])
        elif type == PersistenceEngineType.SQLITE:
            return SQLiteConfig(persistence=PersistenceEngineType.SQLITE, db_file_path=data["db_file_path"])
        elif type == PersistenceEngineType.MYSQL:
            return MySQLConfig(persistence=PersistenceEngineType.MYSQL, 
                                host=data["host"],
                                port=data["port"],
                                user=data["user"],
                                password=data["password"],
                                database=data["database"]
                               )
        else:
            raise ValueError(f"Unsupported persistence type: {type_.upper()}")


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
        else:
            raise ValueError(f"Unsupported notification type: {type_.upper()}")
    

    def _parse_config(self, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        
        # General config
        general = GeneralConfig(pooling_time=data["GeneralConfig"]["pooling_time"], author=data["GeneralConfig"]["author"])

        # Persistence config
        persistence = self._create_persistence_config(data["PersistenceConfig"])

        # Notification configs
        notifications = [self._create_notification_config(n) for n in data.get("NotificationConfig", [])]

        return general, persistence, notifications
    