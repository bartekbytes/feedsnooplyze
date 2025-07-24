import duckdb

from .base_persistence_engine import PersistenceEngine
from page import PageContent



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
