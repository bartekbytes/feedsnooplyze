from sqlalchemy import Engine, MetaData, Table, Column, String, Text, DateTime, inspect, text
from time import sleep

# feedsnooplyze modules
from .persistence_engine import PersistenceEngineIcon


def _create_structure(engine: Engine):
    metadata = MetaData()

    page_content = Table(
        'page_content', metadata,
        Column('page_name', String(100), nullable=False),
        Column('content_time', DateTime, nullable=False),
        Column('content_hash', String(100), nullable=False),
        Column('full_content', Text),
        Column('added_content', Text)
    )

    page_content.create(engine)


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

                _create_structure(engine)

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

            _create_structure(engine)

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

    