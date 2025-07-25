import sqlite3

from .base_persistence_engine import PersistenceEngine
from page import PageContent



class SQLitePersistenceEngine(PersistenceEngine):

    def __init__(self, database : str):
        self.database = database
        self.connection = None

    def create_structure(self, connection):
        with open(file=r"persistence/sqlite/scripts/structure.sql", mode="r") as f:
            cont = f.read()

        if cont:
            import time
            connection.execute(cont)

            time.sleep(10)

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'content'")
            result = cursor.fetchall()

            if result:
                return True
            else:
                return False


    def connect(self):
        connection = sqlite3.connect(database=self.database)
        
        if connection:
            self.connection = connection
            return connection
        else:
            return None
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Content (Name, TimeAdded, Hash, Content) VALUES (?, ?, ?, ?)", (name, time_added, hash, content))
        self.connection.commit()

    def is_content_available(self, name : str) -> bool:
        cursor = self.connection.cursor()
        sql = f"SELECT 1 FROM Content WHERE Name = '{name}' ORDER BY TimeAdded DESC"
        cursor.execute(sql)
        if len(cursor.fetchall()) > 0:
            return True
        else: 
            return False

    def get_latest_by_name(self, name : str) -> PageContent:
        cursor = self.connection.cursor()
        sql = f"SELECT Name, TimeAdded, Hash, Content FROM Content WHERE Name = '{name}' ORDER BY TimeAdded DESC LIMIT 1"
        cursor.execute(sql)
        pc = cursor.fetchall()
        return PageContent(name=pc[0][0], is_new=None, is_update=None, creation_time=pc[0][1], update_time=None, hash=pc[0][2], content=pc[0][3])
