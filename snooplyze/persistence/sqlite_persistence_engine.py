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
            cursor = connection.cursor()
            cursor.execute(cont)
            connection.commit()

            time.sleep(10)

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'PageContent'")
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
            
    def add_content(self, page_name: str, content_time: str, content_hash: str, full_content: str, added_content: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO PageContent (PageName, ContentTime, ContentHash, FullContent, AddedContent) VALUES (?, ?, ?, ?, ?)", (page_name, content_time, content_hash, full_content, added_content))
        self.connection.commit()

    def is_content_available(self, page_name : str) -> bool:
        cursor = self.connection.cursor()
        sql = f"SELECT 1 FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC"
        cursor.execute(sql)
        if len(cursor.fetchall()) > 0:
            return True
        else: 
            return False

    def get_latest_by_name(self, page_name : str) -> PageContent:
        cursor = self.connection.cursor()
        sql = f"SELECT PageName, ContentTime, ContentHash, FullContent, AddedContent FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC LIMIT 1"
        cursor.execute(sql)
        pc = cursor.fetchall()
        return PageContent(page_name=pc[0][0], content_time=pc[0][1], content_hash=pc[0][2], full_content=pc[0][3], added_content=pc[0][4])
