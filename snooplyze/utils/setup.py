from enum import Enum

# import persistence module
from persistence import *

class PersistenceLayerSetup:
    
    def __init__(self, persistence_engine_type : PersistenceEngineType):
        self.persistence_engine_type = persistence_engine_type or PersistenceEngineType()

    def set_dbname(self, db_name: str) -> None:
        self.db_name = db_name

    def set_connection_string(self, connection_string: str) -> None:
        self.set_connection_string = connection_string


    def execute_setup(self) -> bool:
    
        if self.persistence_engine_type == PersistenceEngineType.DUCKDB:
            # add try here
            # duckdb.duckdb.IOException: IO Error: File is already open in
            # duckdb.duckdb.CatalogException: Catalog Error: Table with name "content" already exists! 
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.DUCKDB.name
            pe = DuckDbPersistenceEngine(database=f"../persistence/{self.db_name}")
            pe_connection = pe.connect()
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")

                result = pe_connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'Content'").fetchall()
                print(result)

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        pe_connection.execute("DROP TABLE Content")
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
        
        elif self.persistence_engine_type == PersistenceEngineType.POSTGRESQL:
            PERSISTENCE_ENGINE_NAME = PersistenceEngineType.POSTGRESQL.name
            # add try here
            # duckdb.duckdb.IOException: IO Error: File is already open in
            # duckdb.duckdb.CatalogException: Catalog Error: Table with name "content" already exists! 
            pe = PostgreSQLPersistenceEngine(connection_string=self.set_connection_string)
            pe_connection = pe.connect()
            print(pe_connection)
            
            if pe_connection:
                print(f"✅ {PERSISTENCE_ENGINE_NAME} connection established")

                result = pe_connection.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'content'").fetchall()
                print(result)

                if result:
                    print(f"⚠️ {PERSISTENCE_ENGINE_NAME} structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        pe_connection.execute("DROP TABLE content")
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