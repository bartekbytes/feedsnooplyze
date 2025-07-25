from abc import ABC, abstractmethod
from enum import Enum

class PersistenceEngineType(str, Enum):
    FLATFILE = "FLATFILE"
    DUCKDB = "DUCKDB"
    SQLITE = "SQLITE"
    POSTGRESQL = "POSTGRESQL"
    MSSQLSERVER = "MSSQLSERVER"


class PersistenceEngine(ABC):
    
    @abstractmethod
    def create_structure(self):
        pass
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add_content(self):
        pass


