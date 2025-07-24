import psycopg

from .base_persistence_engine import PersistenceEngine
from page import PageContent


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
