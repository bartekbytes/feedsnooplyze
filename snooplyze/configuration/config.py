from dataclasses import dataclass
from abc import ABC
from typing import Optional
import yaml

from persistence import PersistenceEngineType


### General Config Classess

@dataclass
class GeneralConfig:
    pool_time: Optional[int] = 3600 # 1 hour
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
class PostgreSQLConfig(PersistenceConfigBase):
    persistence: str
    connection_string: str

@dataclass
class MSSQLConfig(PersistenceConfigBase):
    persistence: str
    connection_string: str
    database_name: str

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
class ConsoleNotification(NotificationConfigBase):
    pass

@dataclass
class FlatFileNotification(NotificationConfigBase):
    file_path: str

@dataclass
class EmailNotification(NotificationConfigBase):
    email_address: str
    subject: Optional[str] = None

@dataclass
class SMSNotification(NotificationConfigBase):
    phone_number: str
    provider: Optional[str] = None



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
        type_ = data.get("persistence").upper()
        
        if type_ == PersistenceEngineType.POSTGRESQL:
            return PostgreSQLConfig(persistence=PersistenceEngineType.POSTGRESQL, connection_string=data["connection_string"])
        elif type_ == PersistenceEngineType.DUCKDB:
            return DuckDBConfig(persistence=PersistenceEngineType.DUCKDB, db_file_path=data["db_file_path"])
        elif type_ == PersistenceEngineType.MYSQL:
            return MySQLConfig(persistence=PersistenceEngineType.MYSQL, 
                                host=data["host"],
                                port=data["port"],
                                user=data["user"],
                                password=data["password"],
                                database=data["database"]
                               )
        elif type_ == PersistenceEngineType.MSSQLSERVER:
            return MSSQLConfig(
                persistence=PersistenceEngineType.MSSQLSERVER,
                connection_string=data["connection_string"],
                db_name=data["db_name"]
            )
        else:
            raise ValueError(f"Unsupported persistence type: {type_.upper()}")


    def _create_notification_config(self, data: dict) -> NotificationConfigBase:
        type_ = data.get("notification_type")
        if type_ == "console":
            return ConsoleNotification()
        elif type_ == "flatfile":
            return FlatFileNotification(file_path=data["file_path"])
        elif type_ == "email":
            return EmailNotification(
                email_address=data["email_address"],
                subject=data.get("subject")
            )
        elif type_ == "sms":
            return SMSNotification(
                phone_number=data["phone_number"],
                provider=data.get("provider")
            )
        else:
            raise ValueError(f"Unsupported notification type: {type_.upper()}")
    

    def _parse_config(self, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        
        # General config
        general = GeneralConfig(pool_time=data["GeneralConfig"]["pool_time"], author=data["GeneralConfig"]["author"])

        # Persistence config
        persistence = self._create_persistence_config(data["PersistenceConfig"])

        # Notification configs
        notifications = [self._create_notification_config(n) for n in data.get("NotificationConfig", [])]

        return general, persistence, notifications
    