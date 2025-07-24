from abc import ABC, abstractmethod
from enum import Enum

class PersistenceEngineType(Enum):
    FLATFILE = 1
    DUCKDB = 2
    SQLITE = 3
    POSTGRESQL = 4


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


