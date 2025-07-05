from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import yaml


class PersistenceConfigBase(ABC):
    persistence: str

    @classmethod
    @abstractmethod
    def validate(cls, data: dict) -> None:
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate(data)
        return cls(**data)


PERSISTENCE_REGISTRY: dict[str, type[PersistenceConfigBase]] = {}

def register_persistence(cls: type[PersistenceConfigBase]):
    
    if not hasattr(cls, '__name__'):
        raise TypeError(f"Expected a class, got {type(cls).__name__}")
    
    key = cls.__name__.replace("Config", "").lower()
    PERSISTENCE_REGISTRY[key] = cls
    return cls



@dataclass
@register_persistence
class DuckDBConfig(PersistenceConfigBase):
    persistence: str
    db_file_path: str

    @classmethod
    def validate(cls, data: dict):
        if "db_file_path" not in data:
            raise ValueError("Missing 'db_file_path' for DuckDB persistence")


@dataclass
@register_persistence
class PostgreSQLConfig(PersistenceConfigBase):
    persistence: str
    connection_string: str

    @classmethod
    def validate(cls, data: dict):
        if "connection_string" not in data:
            raise ValueError("Missing 'connection_string' for PostgreSQL persistence")
        

@dataclass
@register_persistence
class MSSQLConfig(PersistenceConfigBase):
    persistence: str
    connection_string: str
    database_name: str

    @classmethod
    def validate(cls, data: dict):
        missing = [f for f in ("connection_string", "database_name") if f not in data]
        if missing:
            raise ValueError(f"Missing fields for mssql persistence: {', '.join(missing)}")


@dataclass
class GeneralConfig:
    pool_time: Optional[int] = 3600 # 1 hour


@dataclass
class Config:
    persistence_config: PersistenceConfigBase
    general_config: GeneralConfig

@dataclass
class ConfigReader:
    path_to_file: str
    
    def read(self) -> str:
        with open(self.path_to_file) as f:
            return f.read()


class ConfigLoader:
    def __init__(self, reader: ConfigReader):
        self.reader = reader


    def load_config(self) -> Config:
        yaml_str = self.reader.read()
        return self.parse_config(yaml_str)


    def parse_config(self, yaml_str: str) -> Config:
        data = yaml.safe_load(yaml_str)
        config_list = data.get("Config", [])
    
        persistence_config = None
        general_config = GeneralConfig()
    
        for item in config_list:
            
            if "persistence" in item:
                p = item["persistence"].lower()
                cls = PERSISTENCE_REGISTRY.get(p)
                if not cls:
                    raise ValueError(f"Unknown persistence type: {p}")
                persistence_config = cls.from_dict(item)
            
            elif "pool_time" in item:
                general_config.pool_time = item["pool_time"]

        if persistence_config is None:
            raise ValueError("No persistence configuration found")

        return Config(persistence_config=persistence_config, general_config=general_config)

    