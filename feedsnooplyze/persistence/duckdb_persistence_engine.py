import duckdb

from .base_persistence_engine import PersistenceEngine
from feedsnooplyze.page import PageContent



class DuckDbPersistenceEngine(PersistenceEngine):
    """
    Persistence engine implementation using DuckDB as the backend database.
    Args:
        database (str): Path to the DuckDB database file.
    Attributes:
        database (str): Path to the DuckDB database file.
        connection: DuckDB connection object.
    Methods:
        __init__(database: str):
            Initializes the DuckDbPersistenceEngine with the database file path.
        create_structure(connection):
            Reads and executes the SQL structure script to initialize the database schema.
            Waits for 10 seconds after execution and checks if the 'PageContent' table exists.
            Returns True if the table exists, False otherwise.
        connect():
            Establishes a connection to the DuckDB database.
            Sets the connection attribute and returns the connection object.
        add_content(page_name, content_time, content_hash, full_content, added_content):
            Inserts a new record into the 'PageContent' table with the provided content details.
        is_content_available(page_name):
            Checks if any content is available for the given page name.
            Returns True if content exists, False otherwise.
        get_latest_by_name(page_name):
            Retrieves the latest content entry for the specified page name from the 'PageContent' table.
            Returns a PageContent object with the latest entry's details.
    """

    def __init__(self, database : str):
        self.database = database
        self.connection = None

    def create_structure(self, connection):
        with open(file=r"feedsnooplyze/persistence/duckdb/scripts/structure.sql", mode="r") as f:
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
