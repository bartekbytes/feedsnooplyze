import psycopg

from .base_persistence_engine import PersistenceEngine
from snooplyze.page import PageContent


class PostgreSQLPersistenceEngine(PersistenceEngine):
    """
    PostgreSQLPersistenceEngine provides persistence operations for storing and retrieving page content in a PostgreSQL database.
    Attributes:
        connection_string (str): The connection string used to connect to the PostgreSQL database.
        connection: The active database connection object.
    Methods:
        __init__(connection_string: str):
            Initializes the persistence engine with the given connection string.
        create_structure(connection) -> bool:
            Creates the required database structure by executing a SQL script. Returns True if the structure is created successfully.
        connect():
            Establishes a connection to the PostgreSQL database using the provided connection string. Returns the connection object if successful.
        add_content(page_name: str, content_time: str, content_hash: str, full_content: str, added_content: str):
            Inserts new page content into the database.
        is_content_available(page_name: str) -> bool:
            Checks if content for the specified page name exists in the database. Returns True if available.
        get_latest_by_name(page_name: str) -> PageContent:
            Retrieves the latest content for the specified page name from the database and returns it as a PageContent object.
    """

    def __init__(self, connection_string: str):
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

            result = connection.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'pagecontent'").fetchall()

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
            
    def add_content(self, page_name: str, content_time: str, content_hash: str, full_content: str, added_content: str):
        self.connection.execute("INSERT INTO pagecontent (pagename, contenttime, contenthash, fullcontent, addedcontent) VALUES (%s, %s, %s, %s, %s)", (page_name, content_time, content_hash, full_content, added_content))
        self.connection.commit()

    def is_content_available(self, page_name: str) -> bool:
        sql = f"SELECT 1 FROM pagecontent WHERE pagename = '{page_name}' ORDER BY contenttime DESC"
        if len(self.connection.execute(sql).fetchall()) > 0:
            return True
        else: 
            return False

    def get_latest_by_name(self, page_name: str) -> PageContent:
        sql = f"SELECT pagename, contenttime, contenthash, fullcontent, addedcontent FROM pagecontent WHERE pagename = '{page_name}' ORDER BY contenttime DESC LIMIT 1"
        pc = self.connection.execute(sql).fetchall()
        return PageContent(page_name=pc[0][0], content_time=pc[0][1], content_hash=pc[0][2], full_content=pc[0][3], added_content=pc[0][4])
    