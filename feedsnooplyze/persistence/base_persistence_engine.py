from abc import ABC, abstractmethod
from enum import Enum

class PersistenceEngineType(str, Enum):
    """
    Enumeration of supported persistence engine types.

    Attributes:
        DUCKDB: Represents the DuckDB database engine.
        SQLITE: Represents the SQLite database engine.
        POSTGRESQL: Represents the PostgreSQL database engine.
        MSSQLSERVER: Represents the Microsoft SQL Server database engine.
        MYSQL: Represents the MySQL database engine.
    """
    DUCKDB = "DUCKDB"
    SQLITE = "SQLITE"
    POSTGRESQL = "POSTGRESQL"
    MSSQLSERVER = "MSSQLSERVER"
    MYSQL = "MYSQL"


class PersistenceEngine(ABC):
    """
    Abstract base class for persistence engines.
    This class defines the interface for persistence engines that manage the storage and retrieval of content.
    Subclasses must implement methods for creating the storage structure, connecting to the storage backend,
    adding content, checking content availability, and retrieving the latest content by name.
    Methods
    -------
    create_structure():
        Set up the necessary structure for persistence (e.g., database tables, file directories).
    connect():
        Establish a connection to the persistence backend.
    add_content():
        Add new content to the persistence storage.
    is_content_available():
        Check if the desired content is available in the storage.
    get_latest_by_name():
        Retrieve the latest content entry by its Page name.
    """
    
    @abstractmethod
    def create_structure(self):
        pass
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add_content(self):
        pass

    @abstractmethod
    def is_content_available(self):
        pass

    @abstractmethod
    def get_latest_by_name(self):
        pass


