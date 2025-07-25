from dataclasses import dataclass
from typing import List, Optional, Union
import yaml

@dataclass
class GeneralConfig:
    pool_time: int
    author: str

@dataclass
class PersistenceConfig:
    pass

@dataclass
class PostgreSQLConfig(PersistenceConfig):
    connection_string: str

@dataclass
class DuckDBConfig(PersistenceConfig):
    file_path: str

@dataclass
class MSSQLConfig(PersistenceConfig):
    connection_string: str
    db_name: str


@dataclass
class NotificationConfig:
    pass

@dataclass
class ConsoleNotification(NotificationConfig):
    pass

@dataclass
class EmailNotification(NotificationConfig):
    email_address: str
    subject: Optional[str] = None

@dataclass
class SMSNotification(NotificationConfig):
    phone_number: str
    provider: Optional[str] = None


def create_persistence_config(data: dict) -> PersistenceConfig:
    type_ = data.get("persistence")
    if type_ == "postgresql":
        return PostgreSQLConfig(connection_string=data["connection_string"])
    elif type_ == "duckdb":
        return DuckDBConfig(file_path=data["file_path"])
    elif type_ == "mssql":
        return MSSQLConfig(
            connection_string=data["connection_string"],
            db_name=data["db_name"]
        )
    else:
        raise ValueError(f"Unsupported persistence type: {type_}")
    

def create_notification_config(data: dict) -> NotificationConfig:
    type_ = data.get("notification_type")
    if type_ == "console":
        return ConsoleNotification()
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
        raise ValueError(f"Unsupported notification type: {type_}")
    


def load_config(yaml_file_path: str):
    with open(yaml_file_path, "r") as file:
        config = yaml.safe_load(file)

    # General config
    general = GeneralConfig(pool_time=config["GeneralConfig"]["pool_time"], author=config["GeneralConfig"]["author"])

    # Persistence config
    persistence = create_persistence_config(config["PersistenceConfig"])

    # Notification configs
    notifications = [
        create_notification_config(n) for n in config.get("NotificationConfig", [])
    ]

    return general, persistence, notifications