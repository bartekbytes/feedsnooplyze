from persistence.persistence_engine import *
from enum import Enum

class PersistenceEngine(Enum):
    FLAT_FILE = 1
    DUCK_DB = 2
    SQLITE = 3

class PersistenceLayerSetup:
    
    def __init__(self, persistence_engine_type : PersistenceEngineType):
        self.persistence_engine_type = persistence_engine_type or PersistenceEngineType()

    def set_dbname(self, db_name: str) -> None:
        self.db_name = db_name


    def execute_setup(self) -> bool:
    
        if self.persistence_engine_type == PersistenceEngineType.DUCK_DB:
            # add try here
            # duckdb.duckdb.IOException: IO Error: File is already open in
            # duckdb.duckdb.CatalogException: Catalog Error: Table with name "content" already exists! 
            ddbpe = DuckDbPersistenceEngine(database=f"../persistence/{self.db_name}")
            ddb_connection = ddbpe.connect()
            
            if ddb_connection:
                print(f"✅ Duck DB connection established")

                result = ddb_connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'content'").fetchall()
                print(result)

                if result:
                    print(f"⚠️ Duck DB structure exists, will be re-created")
                    print(f"⚠️ Warning this procedure is descructibe!")
                    shall_we_proceed = input("Do you want to proceed? [y/n] ")
                    if shall_we_proceed == 'y':
                        ddb_connection.execute("DROP TABLE content")
                        ddbpe.create_structure(connection=ddb_connection)
                        result = ddb_connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'content'").fetchall()
                    
                        if result:
                            print(f"✅ Duck DB structure has been created")
                            return True
                        else:
                            print(f"❌ Duck DB structure has not been created")
                            return False
                    else:
                        print(f"⚠️ Set-up aborted.")
                
                else:
                    print(f"⚠️ Duck DB does not exist, will be created")
                    ddbpe.create_structure(connection=ddb_connection)
                    result = ddb_connection.execute("SELECT * FROM information_schema.tables WHERE table_name = 'content'").fetchall()
                    
                    if result:
                        print(f"✅ Duck DB structure has been created")
                        return True
                    else:
                        print(f"❌ Duck DB structure has not been created")
                        return False
                    
            else:
                print(f"❌ Duck DB connection failed")
                return False
        
        else:
            return False