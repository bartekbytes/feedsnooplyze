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
    parser = argparse.ArgumentParser(description="📦 snooplyze", epilog="Example usage:\n  myapp.py --command setup\n  myapp.py -c fetch", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-r", "--run-mode", type=str, choices=["setup", "fetch"], required=True, help="Run mode of snooplyze: setup or fetch")
    parser.add_argument("-p", "--pooling-time", type=int, help="How often to pool data")
    parser.add_argument("-f", "--config-file", type=str, help="Path to configuration file")


    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    print(args) # debug, to delete

    #if args.run_mode == 'fetch' and args.config_file is None:
    #    parser.error("--config_file is required when --run_mode is 'fetch'")

    # TODO: for now only DuckDB engine is supported for setup
    if args.run_mode == 'setup':

        print("🔧 Running setup...")
        pe = PersistenceLayerSetup(persistence_engine_type=PersistenceEngineType.DUCK_DB)
        pe.execute_setup()

    elif args.run_mode == 'fetch':
        
        if args.config_file:
            config = PagesConfig(path_to_file=args.config_file)
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
    #main()
    
    print("haha!")
    
    


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

    from configuration.pages_config import *
    pcr = PagesConfigReader(r"C:\code\snooplyze\snooplyze.yaml")
    print(pcr)

    pcl = PagesConfigLoader(reader=pcr)
    print(pcl)
    pages_monitors = pcl.load_config()

    print(pages_monitors)

    print("---------")

    for pm in pages_monitors:
        print(pm)
        pm.check_for_update_new()
    

    while True:
        time.sleep(10)
        [pm.check_for_update_new() for pm in pages_monitors]

    #for l in lll:
        #print(l)
        #l.check_for_update_new()
        


    ########################

    #c = PagesConfig(path_to_file=r"../snooplyze.yaml")
    #parsing_result = c.parse()

    #if parsing_result:
        #(config, page_monitor) = c.process_config_data()
        #print(config)
        #print(page_monitor)

    #####################

    #config = PagesConfig(path_to_file=r"../snooplyze.yaml")
    #(c, monitors) = config.parse_yaml()
    #print(monitors)

    # Poll every 'pooling_time' seconds
    #while True:
        #time.sleep(10)
        #[m.check_for_update() for m in monitors]


    


