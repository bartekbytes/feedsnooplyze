import argparse, sys
import time

# import snooplyze modules
from parser import *
from persistence import PersistenceEngineType
from configuration.config import ConfigLoader, ConfigReader
from configuration.pages_config import PagesConfigReader, PagesConfigLoader
from utils import PersistenceLayerSetup


def main():
    parser = argparse.ArgumentParser(
        description="📦 snooplyze",
        epilog="Example usage:\n  snooplyze.py --run-mode [setup|fetch]\n --pooling-time [in seconds]\n --config-file [path to conf]",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-r", "--run-mode", type=str, choices=["setup", "fetch"], required=True, help="Run mode of snooplyze: setup or fetch")
    parser.add_argument("-ft", "--fetch-type", type=str, choices=["interactive", "oneshot"], required=False, help="Fetch type: interactive in console, oneshot run from external orchestrator")
    parser.add_argument("-p", "--pooling-time", type=int, help="When fetch-type is interactive, how often to pool data")
    parser.add_argument("-f", "--config-file", type=str, help="Path to configuration file")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Check arguments consistency
    if args.run_mode == 'fetch' and args.config_file is None:
        parser.error("When run-mode is 'fetch', config-file must be provided")
    
    if args.run_mode == 'fetch' and args.fetch_type is None:
        parser.error("When run-mode is 'fetch', fetch-type must be provided")

    # Read app config file
    cr = ConfigReader(r"../config.yaml") # expecting a config file here with this name
    cl = ConfigLoader(reader=cr)
    general_config, persistence_config, notifications_config = cl.load_config() # Get all 3 types of Config: general, persistence and notifications

    print("⚙️ Config loaded:")
    print(f"General Config: {general_config}")
    print(f"Persistence Config: {persistence_config}")
    print(f"Notifications Config:")
    for n in notifications_config:
        print(n)

    if args.run_mode == 'setup':
        
        print("🔧 Running setup...")

        if persistence_config.persistence.upper() == PersistenceEngineType.DUCKDB:
            print(f"... for 🦆 {PersistenceEngineType.DUCKDB.value} Peristence Engine")
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.DUCKDB)
            pe.set_dbname(persistence_config.db_file_path)
            pe.execute_setup()
        
        elif persistence_config.persistence.upper() == PersistenceEngineType.SQLITE:
            print(f"... for 📁 {PersistenceEngineType.SQLITE.value} Peristence Engine")
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.SQLITE)
            pe.set_dbname(persistence_config.db_file_path)
            pe.execute_setup()

        elif persistence_config.persistence.upper() == PersistenceEngineType.POSTGRESQL:
            print(f"... for 🐘 {PersistenceEngineType.POSTGRESQL.value} Peristence Engine")
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.POSTGRESQL)
            pe.set_connection_string(persistence_config.connection_string)
            pe.execute_setup()

        elif persistence_config.persistence.upper() == PersistenceEngineType.MYSQL:
            print(f"... for 🐬 {PersistenceEngineType.MYSQL.value} Peristence Engine")
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.MYSQL)
            pe.set_host(persistence_config.host)
            pe.set_port(persistence_config.port)
            pe.set_user(persistence_config.user)
            pe.set_password(persistence_config.password)
            pe.set_database(persistence_config.database)
            pe.execute_setup()
    
        else:
            print(f"❌ {persistence_config.persistence} is not supported")
            exit(1)

    elif args.run_mode == 'fetch':
            
        # Read Pages config file
        pcr = PagesConfigReader(args.config_file)
        pcl = PagesConfigLoader(reader=pcr)
        pages_monitors = pcl.load_config() # parse and load config, return a list of PageMonitor

        # Create and Connect to Persistence Engine
        persistence_engine = None

        if persistence_config.persistence.upper() == PersistenceEngineType.DUCKDB:
            from persistence import DuckDbPersistenceEngine
            persistence_engine = DuckDbPersistenceEngine(database=persistence_config.db_file_path)
        
        elif persistence_config.persistence.upper() == PersistenceEngineType.SQLITE:
            from persistence import SQLitePersistenceEngine
            persistence_engine = SQLitePersistenceEngine(database=persistence_config.db_file_path)

        elif persistence_config.persistence.upper() == PersistenceEngineType.POSTGRESQL:
            from persistence import PostgreSQLPersistenceEngine
            persistence_engine = PostgreSQLPersistenceEngine(connection_string=persistence_config.connection_string)

        elif persistence_config.persistence.upper() == PersistenceEngineType.MYSQL:
            from persistence import MySQLPersistenceEngine
            persistence_engine = MySQLPersistenceEngine(
                host=persistence_config.host,
                port=persistence_config.port,
                user=persistence_config.user,
                password=persistence_config.password,
                database=persistence_config.database)
        
        # Try to connect to Persistence Engine
        if not persistence_engine.connect():
            print("❌ Can't connect to Persistence Engine!")
            exit(1)

        
        #############################
        # Main logic of the app
        #############################
        
        loop_counter: int = 1
        pooling_time = None
        
        # If running mode is 'interactive' then pooling_time must be setup.
        # pooling_time from command-line arguments takes precedence over pooling_time from the configuration file.
        if args.fetch_type == 'interactive':
            pooling_time = args.pooling_time if args.pooling_time else general_config.pooling_time
            print(f"Pooling time set to: {pooling_time}")

        # Mode how app works, interactive or oneshot
        if args.fetch_type == 'interactive' or args.fetch_type == 'oneshot':
            
            while True:
                
                
                print("\n------------------")
                print(f"- 📥 Fetching data ({args.fetch_type} mode)... Loop counter: {loop_counter}")
                print("-------------------\n")

                # For each of PageMonitor instance inside pages_monitors list...
                for pm in pages_monitors:

                    pm.notifiers = notifications_config
                
                    # 1. Check if there is already any PageContent available in Persistence Layer for a given Page
                    content_available = persistence_engine.is_content_available(page_name=pm.page.name)

                    if content_available:

                        # Get the latest PageContent (ordered by ContentTime) for a given Page
                        page_content = persistence_engine.get_latest_by_name(page_name=pm.page.name)

                        # 2. Check if there is any content change since the last saved content
                        pc = pm.check_for_content_update(latest_persisted_hash=page_content.content_hash, latest_persisted_content=page_content.full_content)
                    
                        # If a new content detected, add it to the Persisitence Layer
                        if pc.page_name:
                    
                            # 3. Add new content to Persistence
                            persistence_engine.add_content(page_name=pc.page_name, content_time=pc.content_time, 
                                                        content_hash=pc.content_hash, full_content=pc.full_content, added_content=pc.added_content)
                
                    else:
                        # There is no content stored in Persistence Layer for a given Page,
                        # so execute check for content update with dummy hash and content
                        pc = pm.check_for_content_update(latest_persisted_hash=None, latest_persisted_content=None)
                        persistence_engine.add_content(page_name=pc.page_name, content_time=pc.content_time,
                                                    content_hash=pc.content_hash, full_content=pc.full_content, added_content=pc.added_content)
                

                # Infinite loop for 'interactive' mode.
                # For 'oneshot' mode, break the loop after the first run.
                if args.fetch_type == 'oneshot':
                    break
                else:
                    loop_counter = loop_counter + 1
                    time.sleep(pooling_time)
                
        else:
            print("❌ Can't execute fetching data")



if __name__ == "__main__":
    main()

    
    
    


