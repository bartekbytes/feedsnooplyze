from sqlalchemy import Engine, MetaData, Table, Column, String, Text, DateTime, inspect, text
from time import sleep

# feedsnooplyze modules
from .persistence_engine import PersistenceEngineIcon

TABLES = ['page_content', 'rss_content', 'rss_feed_content']

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

    rss_content = Table(
        'rss_content', metadata,
        Column('rss_name', String(100), nullable=False),
        Column('content_time', DateTime, nullable=False),
        Column('content_hash', String(100), nullable=False),
        Column('full_content', Text),
        Column('added_content', Text)
        
    )
    rss_content.create(engine)

    rss_feed_content = Table(
        'rss_feed_content', metadata,
        Column('rss_name', String(100), nullable=False),
        Column('rss_feed_name', String(200), nullable=False),
        Column('content_time', DateTime),
        Column('content_hash', String(100)),
        Column('full_content', Text),
        Column('added_content', Text),
        Column('title', Text),
        Column('link', Text),
        Column('published', Text),
        Column('summary', Text)
        
    )
    rss_feed_content.create(engine)


def persistence_setup(engine: Engine, config: dict) -> bool:
    
    persistence_engine_name = config.persistence.lower()

    print(f"Setting up the persistence layer for {persistence_engine_name} {PersistenceEngineIcon[persistence_engine_name.upper()]}")

    if engine:
        print(f"✅ Persistence engine {persistence_engine_name} is set up.")

        inspector = inspect(engine)
        if any([inspector.has_table(x) for x in TABLES]): # TODO: all or any?
            print(f"⚠️ {persistence_engine_name} structure exists, will be re-created")
            print(f"⚠️ Warning this procedure is descructibe!")
            shall_we_proceed = input("Do you want to proceed? [y/n] ")
            if shall_we_proceed == 'y':
                
                metadata = MetaData()
                
                for t in TABLES:
                    table = Table(t, metadata, autoload_with=engine)
                    table.drop(engine)
                    print(f"🗑️ '{t}' table dropped.")

                # give some time for the DB Engine
                sleep(5)

                _create_structure(engine)

                # ...here too :) Can be done maybe with a thread and async?
                sleep(5)

                inspector = inspect(engine)
                if all([inspector.has_table(x) for x in TABLES]):
                    for t in TABLES:
                        print(f"✅ '{t}' table successfully created in the database.")
                    return True
                else:
                    print(f"❌ Failed to create the structure in the database.")
                    return False
            
            else:
                print(f"⚠️ Set-up aborted.")
                return False

        else:
            print(f"⚠️ Structure does not exist, will be created")

            _create_structure(engine)

            # give some time for the DB Engine
            sleep(5)

            inspector = inspect(engine)
            if all([inspector.has_table(x) for x in TABLES]):
                for t in TABLES:
                    print(f"✅ '{t}' table successfully created in the database.")
                return True
            else:
                print(f"❌ Failed to create the structure in the database.")
                return False

    else:
        print(f"❌ {persistence_engine_name} connection failed")
        return False

    