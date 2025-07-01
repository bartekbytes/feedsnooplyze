import argparse, sys
import time

from parser.generic_parsers import *
from persistence.persistence_engine import PersistenceEngineType
from configuration.pages_config import PagesConfig
from configuration.config import ConfigLoader, ConfigReader

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
    parser.add_argument("-f", "--config-file", type=str, required=True, help="Path to configuration file")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Check arguments consistency
    if args.run_mode == 'fetch' and args.fetch_type is None:
        parser.error("When run-mode is 'fetch', fetch-type must be provided")

    if args.run_mode == 'fetch' and args.fetch_type == 'interactive' and args.pooling_time is None:
        parser.error("When run-mode is 'fetch' and fetch-type is 'interactive' then pooling-time must be provided")


    # TODO: for now only DuckDB engine is supported for setup
    if args.run_mode == 'setup':

        cr = ConfigReader(r"snooplyze/config.yaml") # expecting a config file here with this name
        cl = ConfigLoader(reader=cr)
        config = cl.load_config()
        
        print("🔧 Running setup...")

        if config.persistence_config.persistence == "duckdb":
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.DUCK_DB)
            pe.set_dbname(config.persistence_config.db_file_path)
            pe.execute_setup()
        else:
            print(f"{config.persistence_config.persistence} is not supported")
            exit(1)

    elif args.run_mode == 'fetch':
            
        cr = ConfigReader(r"../config.yaml") # expecting a config file here with this name
        cl = ConfigLoader(reader=cr)
        config = cl.load_config()
        print(config)

        #pe = DuckDbPersistenceEngine(database=config.persistence_config.db_file_path)
        #pages_config = PagesConfig(path_to_file=args.config_file, persistence=pe)
        #print(pages_config)


        from configuration.pages_config import PagesConfigReader, PagesConfigLoader
        pcr = PagesConfigReader(args.config_file)
        print(pcr)

        pcl = PagesConfigLoader(reader=pcr)
        print(pcl)
        pages_monitors = pcl.load_config()

        print(pages_monitors)


        
        for pm in pages_monitors:
            print(pm)
            pm.check_for_update_new()


        # Mode how app works, interactive or onetime
        if args.fetch_type == 'interactive':
            while True:
                print("📥 Fetching data...")
                [mm.check_for_update() for mm in pages_monitors]
                time.sleep(args.pool_time)
        
        elif args.fetch_type == 'onetime':
            print("📥 Fetching data...")
            [mm.check_for_update() for mm in pages_monitors]
        else:
            print("Can't execute fetching data!")



if __name__ == "__main__":
    main()

    
    
    


