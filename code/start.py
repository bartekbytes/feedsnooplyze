import argparse, sys
import time

from parser.generic_parsers import *
from persistence.persistence_engine import PersistenceEngineType


from configuration.config import ConfigLoader, ConfigReader
from configuration.pages_config import PagesConfigReader, PagesConfigLoader

from utils.setup import PersistenceLayerSetup


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

    if args.run_mode == 'fetch' and args.fetch_type == 'interactive' and args.pooling_time is None:
        parser.error("When run-mode is 'fetch' and fetch-type is 'interactive' then pooling-time must be provided")


    # Read app config file
    cr = ConfigReader(r"../config.yaml") # expecting a config file here with this name
    cl = ConfigLoader(reader=cr)
    config = cl.load_config()


    if args.run_mode == 'setup':
        
        print("🔧 Running setup...")

        if config.persistence_config.persistence.upper() == PersistenceEngineType.DUCKDB.name: # TODO: for now only DuckDB engine is supported for setup
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.DUCKDB)
            pe.set_dbname(config.persistence_config.db_file_path)
            pe.execute_setup()
        else:
            print(f"{config.persistence_config.persistence} is not supported")
            exit(1)

    elif args.run_mode == 'fetch':
            
        # Read Pages config file
        pcr = PagesConfigReader(args.config_file)
        pcl = PagesConfigLoader(reader=pcr)
        pages_monitors = pcl.load_config() # parse and load config, return a list of PageMonitor


        # Create and Connect to Persistence Engine
        persistence_engine = None
        if config.persistence_config.persistence.upper() == PersistenceEngineType.DUCKDB.name: # TODO: for now only DuckDB engine is supported
            
            from persistence.persistence_engine import DuckDbPersistenceEngine
            persistence_engine = DuckDbPersistenceEngine(database=f"../persistence/{config.persistence_config.db_file_path}")
        
        elif config.persistence_config.persistence.upper() == PersistenceEngineType.SQLITE: # Dummy, TBD
            pass # Here logic for SQLite            
        
        # Try to connect to Persistence Engine
        if not persistence_engine.connect():
            print("Can't connect to Persistence Engine!")
            exit(1)

        
        #############################
        # Main logic of the app
        #############################
        
        # Mode how app works, interactive or oneshot
        if args.fetch_type == 'interactive':
            
            while True:
                print("📥 Fetching data (interactive)...")

                # For each of PageMonitor instance inside pages_monitors list...
                for pm in pages_monitors:
                
                    # 1. Check if there is already any PageContent available in Persistence Layer for a given Page
                    content_available = persistence_engine.is_content_available(name=pm.page.name)

                    print(f"Is content available? {content_available}")

                    if content_available:
                        page_content = persistence_engine.get_latest_by_name(name=pm.page.name)
                        print("----------------------")
                        print(f"Content for {page_content.name} exists with latest hash {page_content.hash}")
                    
                        # 2. Check if there is any update since last saved content
                        pc = pm.check_for_update(latest_persisted_hash=page_content.hash)
                    
                        # 3. Add new content to Persistence
                        persistence_engine.add_content(name=pc.name, time_added=pc.creation_time, hash=pc.hash, content=pc.content)
                
                    else:
                        print(f"New content for {pm.page.name}")
                        pc = pm.check_for_update(latest_persisted_hash=None)
                        persistence_engine.add_content(name=pc.name, time_added=pc.creation_time, hash=pc.hash, content=pc.content)

                time.sleep(args.pool_time)
        
        elif args.fetch_type == 'oneshot':
            print("📥 Fetching data (oneshot)...")
            
            # For each of PageMonitor instance inside pages_monitors list...
            for pm in pages_monitors:
                
                # 1. Check if there is already any PageContent available in Persistence Layer for a given Page
                content_available = persistence_engine.is_content_available(name=pm.page.name)

                print(f"Is content available? {content_available}")

                if content_available:
                    page_content = persistence_engine.get_latest_by_name(name=pm.page.name)
                    print("----------------------")
                    print(f"Content for {page_content.name} exists with latest hash {page_content.hash}")
                    
                    # 2. Check if there is any update since last saved content
                    pc = pm.check_for_update(latest_persisted_hash=page_content.hash)
                    
                    # 3. Add new content to Persistence
                    persistence_engine.add_content(name=pc.name, time_added=pc.creation_time, hash=pc.hash, content=pc.content)
                
                else:
                    print(f"New content for {pm.page.name}")
                    pc = pm.check_for_update(latest_persisted_hash=None)
                    persistence_engine.add_content(name=pc.name, time_added=pc.creation_time, hash=pc.hash, content=pc.content)
        
        else:
            print("Can't execute fetching data!")



if __name__ == "__main__":
    main()

    
    
    


