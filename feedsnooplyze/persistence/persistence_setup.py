from sqlalchemy import Engine, MetaData, Table, inspect, text
from time import sleep

from .persistence_engine import PersistenceEngineIcon

sql_script = """
    CREATE TABLE IF NOT EXISTS page_content
    (
        page_name TEXT NOT NULL,
        content_time TIMESTAMP NOT NULL,
        content_hash TEXT NOT NULL,
        full_content TEXT ,
        added_content TEXT
    );
    """

def persistence_setup(engine: Engine, config: dict) -> bool:
    
    persistence_engine_name = config.persistence.lower()

    print(f"Setting up the persistence layer for {persistence_engine_name} {PersistenceEngineIcon[persistence_engine_name.upper()]}")

    if engine:
        print(f"✅ Persistence engine {persistence_engine_name} is set up.")

        inspector = inspect(engine)
        if inspector.has_table("page_content"):
            print(f"⚠️ {persistence_engine_name} structure exists, will be re-created")
            print(f"⚠️ Warning this procedure is descructibe!")
            shall_we_proceed = input("Do you want to proceed? [y/n] ")
            if shall_we_proceed == 'y':
                
                metadata = MetaData()
                table = Table('page_content', metadata, autoload_with=engine)
                table.drop(engine)
                print(f"🗑️ 'page_content' table dropped.")
                
                sleep(5)

                with engine.connect() as conn:
                    conn.execute(text(sql_script))
                    conn.commit()

                sleep(5)

                inspector = inspect(engine)
                if inspector.has_table("page_content"):
                    print(f"✅ 'page_content' table successfully created in the database.")
                    return True
                else:
                    print(f"❌ Failed to create 'page_content' table in the database.")
                    return False
            
            else:
                print(f"⚠️ Set-up aborted.")
                return False

        else:
            print(f"⚠️ Structure does not exist, will be created")

            with engine.connect() as conn:
                conn.execute(text(sql_script))
                conn.commit()

            sleep(5)

            inspector = inspect(engine)
            if inspector.has_table("page_content"):
                print(f"✅ 'page_content' table successfully created in the database.")
                return True
            else:
                print(f"❌ Failed to create 'page_content' table in the database.")
                return False

    else:
        print(f"❌ {persistence_engine_name} connection failed")
        return False

    