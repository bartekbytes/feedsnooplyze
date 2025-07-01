import argparse, sys
import time

from parser.generic_parsers import *
from page.page import Page, PageMonitor
from persistence.persistence_engine import PersistenceEngineType, DuckDbPersistenceEngine, FlatFilePersistenceEngine
from configuration.pages_config import PagesConfig


from utils.setup import PersistenceLayerSetup, PersistenceEngine



# obsolete
def fetch(pooling_time : int):
    ddbpe = DuckDbPersistenceEngine(database="../persistence/viz.duckdb")
    ddbpe.connect()

    # Create a fetch for Duck DB blog
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassParser(div_class_name = "newstiles"), persistence = ddbpe, timeout = 10)

    # Create a fetch for Databricks blog
    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentParser(), persistence = ddbpe, timeout = 10)

    # Poll every 'pooling_time' seconds
    while True:
        time.sleep(pooling_time)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]

# obsolete
def fetch_csv(pooling_time : int):
    csvpe = FlatFilePersistenceEngine(file_path=r'C:\code\snooplyze\persistence\viz.csv')
    csvpe.create_structure()

    # Create a fetch for Duck DB blog
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassParser(div_class_name = "newstiles"), persistence = csvpe, timeout = 10)

    # Create a fetch for Databricks blog
    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentParser(), persistence = csvpe, timeout = 10)

    # Poll every 'pooling_time' seconds
    while True:
        time.sleep(pooling_time)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]



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
    print(args) # debug, to delete

    # Check arguments consistency
    if args.run_mode == 'fetch' and args.fetch_type is None:
        parser.error("When run-mode is 'fetch', fetch-type must be provided")

    if args.run_mode == 'fetch' and args.fetch_type == 'interactive' and args.pooling_time is None:
        parser.error("When run-mode is 'fetch' and fetch-type is 'interactive' then pooling-time must be provided")


    # TODO: for now only DuckDB engine is supported for setup
    if args.run_mode == 'setup':

        from configuration.config import ConfigLoader, ConfigReader, Config
        cr = ConfigReader(args.config_file)
        cl = ConfigLoader(reader=cr)
        config = cl.load_config()
        print(config)

        config.persistence_config.persistence
        
        print("🔧 Running setup...")

        if config.persistence_config.persistence == "duckdb":
            pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.DUCK_DB)
            pe.set_dbname(config.persistence_config.db_file_path)
            pe.execute_setup()
        else:
            print(f"{config.persistence_config.persistence} is not supported")
            exit(1)

    elif args.run_mode == 'fetch':
        
        config = PagesConfig(path_to_file=args.config_file)
        print(config)
        #(c, m) = config.parse_yaml()
        #print(c)
        #print(m)

        # One time pooling
        #if c.pool_time == 0:
            #print("📥 Fetching data...")
            #[mm.check_for_update() for mm in m]
        
        #else:
            
            # pooling in a loop
            #while True:
                #print("📥 Fetching data...")
                #time.sleep(c.pool_time)
                #[mm.check_for_update() for mm in m]
        
    #else:
        #print("📥 Fetching data...")
        #fetch_csv(pooling_time=args.pooling_time)


if __name__ == "__main__":
    main()
    
    #print("haha!")
    
    


    #### workable code for getting config
    #from configuration.config import ConfigLoader, ConfigReader, Config
    #cr = ConfigReader(r"C:\code\snooplyze\_config_duckdb.yaml")
    #cl = ConfigLoader(reader=cr)
    #config = cl.load_config()
    #dbname = f"../persistence/{config.persistence_config.db_file_path}"

    #from configuration.pages_config import PagesConfig
    #pe = DuckDbPersistenceEngine(database=dbname)

    #pc = PagesConfig(path_to_file=r"C:\code\snooplyze\snooplyze.yaml", persistence=pe)
    #print(f"Parsing result: {pc.parse}")
    #pages_monitores = pc.process_config_data()
    #print(pages_monitores)
    #for pm in pages_monitores:
    #    print(pm)

    ###################################

    #from configuration.pages_config import *
    #pcr = PagesConfigReader(r"C:\code\snooplyze\snooplyze.yaml")
    #print(pcr)

    #pcl = PagesConfigLoader(reader=pcr)
    #print(pcl)
    #pages_monitors = pcl.load_config()

    #print(pages_monitors)

    #print("---------")

    #for pm in pages_monitors:
        #print(pm)
        #pm.check_for_update_new()
    

    #while True:
        #time.sleep(10)
        #[pm.check_for_update_new() for pm in pages_monitors]


    


