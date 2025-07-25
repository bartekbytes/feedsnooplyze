import mysql.connector

from .base_persistence_engine import PersistenceEngine
from page import PageContent


class MySQLPersistenceEngine(PersistenceEngine):

    def __init__(self, host: str, port: str, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def create_structure(self, connection) -> bool:
        with open(file=r"persistence/mysql/scripts/structure.sql", mode="r") as f:
            cont = f.read()
        
        if cont:
            import time
            cursor = connection.cursor()
            cursor.execute(cont)
            #connection.commit()
            
            time.sleep(10) # give some time to the engine to create the structure

            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'content'")
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
            
    def add_content(self, name: str, time_added: str, hash: str, content: str):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO content (name, timeadded, hash, content) VALUES (%s, %s, %s, %s)", (name, time_added, hash, content))
        self.connection.commit()
        cursor.close()


    def is_content_available(self, name: str) -> bool:
        cursor = self.connection.cursor()
        sql = f"SELECT 1 FROM content WHERE name = '{name}' ORDER BY timeadded DESC"
        cursor.execute(sql)
        if len(cursor.fetchall()) > 0:
            cursor.close()
            return True
        else: 
            cursor.close()
            return False


    def get_latest_by_name(self, name: str) -> PageContent:
        cursor = self.connection.cursor()
        sql = f"SELECT name, timeadded, hash, content FROM content WHERE name = '{name}' ORDER BY timeadded DESC LIMIT 1"
        cursor.execute(sql)
        pc = cursor.fetchall()
        cursor.close()
        
        return PageContent(name=pc[0][0], is_new=None, is_update=None, creation_time=pc[0][1], update_time=None, hash=pc[0][2], content=pc[0][3])
    

    def get_latest_by_name_with_content(self, name: str) -> PageContent:
        cursor = self.connection.cursor()
        sql = f"SELECT name, timeadded, hash, content FROM content WHERE name = '{name}' AND content is NOT NULL ORDER BY timeadded DESC LIMIT 1"
        cursor.execute(sql)
        pc = cursor.fetchall()
        cursor.close()
        
        return PageContent(name=pc[0][0], is_new=None, is_update=None, creation_time=pc[0][1], update_time=None, hash=pc[0][2], content=pc[0][3])
