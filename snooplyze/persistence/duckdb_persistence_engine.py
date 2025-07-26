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

            result = connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'PageContent'").fetchall()

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
            
    def add_content(self, page_name: str, content_time: str, content_hash: str, full_content : str, added_content: str):
        self.connection.execute("INSERT INTO PageContent (PageName, ContentTime, ContentHash, FullContent, AddedContent) VALUES (?, ?, ?, ?, ?)", (page_name, content_time, content_hash, full_content, added_content))


    def is_content_available(self, page_name : str) -> bool:
        sql = f"SELECT 1 FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC"
        if len(self.connection.execute(sql).fetchall()) > 0:
            return True
        else: 
            return False


    def get_latest_by_name(self, page_name : str) -> PageContent:
        sql = f"SELECT PageName, ContentTime, ContentHash, FullContent, AddedContent FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC LIMIT 1"
        pc = self.connection.execute(sql).fetchall()
        return PageContent(page_name=pc[0][0], content_time=pc[0][1], content_hash=pc[0][2], full_content=pc[0][3], added_content=pc[0][4])
