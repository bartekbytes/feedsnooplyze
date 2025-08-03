# import persistence module
from persistence import PersistenceEngineType

class PersistenceLayerSetup:
    """
    Handles the setup and initialization of the persistence layer for various database engines.
    """
    
    def __init__(self, persistence_engine_type : PersistenceEngineType):
        self.persistence_engine_type = persistence_engine_type or PersistenceEngineType()

    def set_dbname(self, db_name: str) -> None:
        self.db_name = db_name

    def set_connection_string(self, connection_string: str) -> None:
        self.set_connection_string = connection_string

    def set_host(self, host: str) -> None:
        self.host = host

    def set_port(self, port: str) -> None:
        self.port = port

    def set_user(self, user: str) -> None:
        self.user = user

    def set_password(self, password: str) -> None:
        self.password = password

    def set_database(self, database: str) -> None:
        self.database = database
        

    def execute_setup(self) -> bool:
    
        if self.persistence_engine_type == PersistenceEngineType.DUCKDB:
            # add try here
            # duckdb.duckdb.IOException: IO Error: File is already open in
            # duckdb.duckdb.CatalogException: Catalog Error: Table with name "content" already exists! 
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.DUCKDB.value
            from persistence import DuckDbPersistenceEngine
            pe = DuckDbPersistenceEngine(database=self.db_name)
            pe_connection = pe.connect()
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")

                result = pe_connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'PageContent'").fetchall()

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        pe_connection.execute("DROP TABLE PageContent")
                        result = pe.create_structure(connection=pe_connection)
                    
                        if result:
                            print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                            return True
                        else:
                            print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                            return False
                    else:
                        print(f"⚠️ Set-up aborted.")
                
                else:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure does not exist, will be created")
                    result = pe.create_structure(connection=pe_connection)

                    
                    if result:
                        print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                        return True
                    else:
                        print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                        return False
                    
            else:
                print(f"❌ {PERSISTENCE_ENGINE_NAME} connection failed")
                return False
        

        if self.persistence_engine_type == PersistenceEngineType.SQLITE:
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.SQLITE.value
            from persistence import SQLitePersistenceEngine
            pe = SQLitePersistenceEngine(database=self.db_name)
            pe_connection = pe.connect()
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")

                result = pe_connection.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'PageContent'").fetchall()

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        pe_connection.execute("DROP TABLE PageContent")
                        result = pe.create_structure(connection=pe_connection)
                    
                        if result:
                            print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                            return True
                        else:
                            print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                            return False
                    else:
                        print(f"⚠️ Set-up aborted.")
                
                else:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure does not exist, will be created")
                    result = pe.create_structure(connection=pe_connection)

                    
                    if result:
                        print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                        return True
                    else:
                        print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                        return False
                    
            else:
                print(f"❌ {PERSISTENCE_ENGINE_NAME} connection failed")
                return False


        elif self.persistence_engine_type == PersistenceEngineType.POSTGRESQL:
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.POSTGRESQL.value
            # add try here 
            from persistence import PostgreSQLPersistenceEngine
            pe = PostgreSQLPersistenceEngine(connection_string=self.set_connection_string)
            pe_connection = pe.connect()
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")

                result = pe_connection.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'pagecontent'").fetchall()

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        pe_connection.execute("DROP TABLE pagecontent")
                        result = pe.create_structure(connection=pe_connection)

                        if result:
                            print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                            return True
                        else:
                            print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                            return False
                    else:
                        print(f"⚠️ Set-up aborted.")
                
                else:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure does not exist, will be created")
                    result = pe.create_structure(connection=pe_connection)
                    
                    if result:
                        print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                        return True
                    else:
                        print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                        return False
                    
            else:
                 print(f"❌ {PERSISTENCE_ENGINE_NAME} connection failed")
                 return False


        elif self.persistence_engine_type == PersistenceEngineType.MYSQL:
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.MYSQL.value
            # add try here 
            from persistence import MySQLPersistenceEngine
            pe = MySQLPersistenceEngine(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database)
            pe_connection = pe.connect()
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")
                cursor = pe_connection.cursor()

                result = cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'PageContent'")
                result = cursor.fetchall()

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        cursor.execute("DROP TABLE PageContent")
                        result = pe.create_structure(connection=pe_connection)

                        if result:
                            print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                            return True
                        else:
                            print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                            return False
                    else:
                        print(f"⚠️ Set-up aborted.")
                
                else:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} does not exist, will be created")
                    result = pe.create_structure(connection=pe_connection)
                    
                    if result:
                        print(f"✅ {PERSISTENCE_ENGINE_NAME} structure has been created")
                        return True
                    else:
                        print(f"❌ {PERSISTENCE_ENGINE_NAME} structure has not been created")
                        return False
                    
            else:
                 print(f"❌ {PERSISTENCE_ENGINE_NAME} connection failed")
                 return False

        else:
            return False