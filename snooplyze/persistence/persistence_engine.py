from abc import ABC, abstractmethod
from enum import Enum

import duckdb


from page.page import PageContent

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

class DuckDbPersistenceEngine(PersistenceEngine):

    def __init__(self, database : str):
        self.database = database
        self.connection = None

    def create_structure(self, connection):
        with open(file=r"persistence/duckdb/scripts/structure.sql", mode="r") as f:
            cont = f.read()

        if cont:
            import time
            connection.execute(cont)

            time.sleep(10)

            result = connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'Content'").fetchall()

            if result:
                return True
            else:
                return False


    def connect(self):
        connection = duckdb.connect(database=self.database)
        
        if connection:
            self.connection = connection
            return connection
        else:
            return None
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        self.connection.execute("INSERT INTO Content (Name, TimeAdded, Hash, Content) VALUES (?, ?, ?, ?)", (name, time_added, hash, content))

    def is_content_available(self, name : str) -> bool:
        sql = f"SELECT 1 FROM Content WHERE Name = '{name}' ORDER BY TimeAdded DESC"
        if len(self.connection.execute(sql).fetchall()) > 0:
            return True
        else: 
            return False

    def get_latest_by_name(self, name : str) -> PageContent:
        sql = f"SELECT Name, TimeAdded, Hash, Content FROM Content WHERE Name = '{name}' ORDER BY TimeAdded DESC LIMIT 1"
        pc = self.connection.execute(sql).fetchall()
        return PageContent(name=pc[0][0], is_new=None, is_update=None, creation_time=pc[0][1], update_time=None, hash=pc[0][2], content=pc[0][3])

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




class PostgreSQLPersistenceEngine(PersistenceEngine):

    def __init__(self, connection_string : str):
        self.connection_string = connection_string
        self.connection = None

    def create_structure(self, connection) -> bool:
        with open(file=r"persistence/postgresql/scripts/structure.sql", mode="r") as f:
            cont = f.read()
        
        if cont:
            import time
            connection.execute(cont)
            connection.commit()
            
            time.sleep(10) # give some time to the engine to create the structure

            result = connection.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'content'").fetchall()

            if result:
                return True
            else:
                return False


    def connect(self):
        import psycopg
        connection = psycopg.connect(self.connection_string)
        
        if connection:
            self.connection = connection
            return connection
        else:
            return None
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        self.connection.execute("INSERT INTO content (name, timeadded, hash, content) VALUES (%s, %s, %s, %s)", (name, time_added, hash, content))
        self.connection.commit()

    def is_content_available(self, name : str) -> bool:
        sql = f"SELECT 1 FROM content WHERE name = '{name}' ORDER BY timeadded DESC"
        if len(self.connection.execute(sql).fetchall()) > 0:
            return True
        else: 
            return False

    def get_latest_by_name(self, name : str) -> PageContent:
        sql = f"SELECT name, timeadded, hash, content FROM content WHERE name = '{name}' ORDER BY timeadded DESC LIMIT 1"
        pc = self.connection.execute(sql).fetchall()
        return PageContent(name=pc[0][0], is_new=None, is_update=None, creation_time=pc[0][1], update_time=None, hash=pc[0][2], content=pc[0][3])


