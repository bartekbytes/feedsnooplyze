from abc import ABC, abstractmethod
from enum import Enum

import duckdb

class PersistenceEngineType(Enum):
    FLAT_FILE = 1
    DUCK_DB = 2
    SQLITE = 3


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

class DuckDbPersistenceEngine(PersistenceEngine):

    def __init__(self, database : str):
        self.database = database
        self.connection = None

    def create_structure(self, connection):
        with open(file=r"persistence/duckdb/scripts/structure.sql", mode="r") as f:
            cont = f.read()

        if cont:
            connection.execute(cont)


    def connect(self):
        connection = duckdb.connect(database=self.database)
        
        if connection:
            self.connection = connection
            return connection
        else:
            return None
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        self.connection.execute("INSERT INTO content (Id, Name, TimeAdded, Hash, Content) VALUES (?, ?, ?, ?, ?)", (666, name, time_added, hash, content))


class FlatFilePersistenceEngine(PersistenceEngine):

    def __init__(self, file_path : str):
        self.file_path = file_path

    def create_structure(self) -> bool:
        import os, csv

        file_exists = os.path.isfile(self.file_path)
        
        if file_exists:
            os.remove(self.file_path)

        header = ['Id', 'Name', 'TimeAdded', 'Hash', 'Content']

        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

        return True


    def connect(self) -> bool:
        
        import os
        file_exists = os.path.isfile(self.file_path)
        
        if file_exists:
            return True
        else:
            return False
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        
        import os, csv

        header = ['Id', 'Name', 'TimeAdded', 'Hash', 'Content']

        file_exists = os.path.isfile(self.file_path)

        with open(file=self.file_path, mode="a", newline='') as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(header)

            writer.writerow([666, name, time_added, hash, content])



