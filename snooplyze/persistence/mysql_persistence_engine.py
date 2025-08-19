import mysql.connector

from .base_persistence_engine import PersistenceEngine
from snooplyze.page import PageContent


class MySQLPersistenceEngine(PersistenceEngine):
    """
    MySQLPersistenceEngine provides persistence operations for storing and retrieving page content in a MySQL database.
    Args:
        host (str): The hostname of the MySQL server.
        port (str): The port number of the MySQL server.
        user (str): The username for authentication.
        password (str): The password for authentication.
        database (str): The name of the database to use.
    Attributes:
        host (str): Hostname of the MySQL server.
        port (str): Port number of the MySQL server.
        user (str): Username for authentication.
        password (str): Password for authentication.
        database (str): Database name.
        connection: MySQL connection object.
    Methods:
        __init__(host: str, port: str, user: str, password: str, database: str):
            Initializes the MySQLPersistenceEngine with connection parameters.
        create_structure(connection) -> bool:
            Creates the required database structure by executing SQL from a file.
            Returns True if the structure is created successfully, otherwise False.
        connect():
            Establishes a connection to the MySQL database and returns the connection object.
        add_content(page_name: str, content_time: str, content_hash: str, full_content: str, added_content: str):
            Inserts new page content into the database.
        is_content_available(page_name: str) -> bool:
            Checks if content for the specified page name exists in the database.
        get_latest_by_name(page_name: str) -> PageContent:
            Retrieves the latest content entry for the specified page name.
    """

    def __init__(self, host: str, port: str, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def create_structure(self, connection) -> bool:
        with open(file=r"snooplyze/persistence/mysql/scripts/structure.sql", mode="r") as f:
            cont = f.read()
        
        if cont:
            import time
            cursor = connection.cursor()
            cursor.execute(cont)
            #connection.commit()
            
            time.sleep(10) # give some time to the engine to create the structure

            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'PageContent'")
            result = cursor.fetchall()

            if result:
                return True
            else:
                return False


    def connect(self):
        
        connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        
        if connection:
            self.connection = connection
            return connection
        else:
            return None
            
    def add_content(self, page_name: str, content_time: str, content_hash: str, full_content: str, added_content: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO PageContent (PageName, ContentTime, ContentHash, FullContent, AddedContent) VALUES (%s, %s, %s, %s, %s)", (page_name, content_time, content_hash, full_content, added_content))
        self.connection.commit()
        cursor.close()


    def is_content_available(self, page_name: str) -> bool:
        cursor = self.connection.cursor()
        sql = f"SELECT 1 FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC"
        cursor.execute(sql)
        if len(cursor.fetchall()) > 0:
            cursor.close()
            return True
        else: 
            cursor.close()
            return False


    def get_latest_by_name(self, page_name: str) -> PageContent:
        cursor = self.connection.cursor()
        sql = f"SELECT PageName, ContentTime, ContentHash, FullContent, AddedContent FROM PageContent WHERE PageName = '{page_name}' ORDER BY ContentTime DESC LIMIT 1"
        cursor.execute(sql)
        pc = cursor.fetchall()
        cursor.close()        
        return PageContent(page_name=pc[0][0], content_time=pc[0][1], content_hash=pc[0][2], full_content=pc[0][3], added_content=pc[0][4])