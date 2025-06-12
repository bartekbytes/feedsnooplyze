import argparse, sys
import time

from data_parse.data_parse import *
from page.page import Page, PageMonitor
from persistence.persistence_engine import DuckDbPersistenceEngine, FlatFilePersistenceEngine

from utils.setup import PersistenceLayerSetup, PersistenceEngine

def fetch(pooling_time : int):
    ddbpe = DuckDbPersistenceEngine(database="../persistence/viz.duckdb")
    ddbpe.connect()

    # Create a fetch for Duck DB blog
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassDataParse(div_class_name = "newstiles"), persistence = ddbpe, timeout = 10)

    # Create a fetch for Databricks blog
    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentDataParse(), persistence = ddbpe, timeout = 10)

    # Poll every 'pooling_time' seconds
    while True:
        time.sleep(pooling_time)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]

def fetch_csv(pooling_time : int):
    csvpe = FlatFilePersistenceEngine(file_path=r'C:\code\snooplyze\persistence\viz.csv')
    csvpe.create_structure()

    # Create a fetch for Duck DB blog
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassDataParse(div_class_name = "newstiles"), persistence = csvpe, timeout = 10)

    # Create a fetch for Databricks blog
    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentDataParse(), persistence = csvpe, timeout = 10)

    # Poll every 'pooling_time' seconds
    while True:
        time.sleep(pooling_time)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]



def main():
    parser = argparse.ArgumentParser(description="📦 snooplyze", epilog="Example usage:\n  myapp.py --command setup\n  myapp.py -c fetch", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-r", "--run-mode", type=str, choices=["setup", "fetch"], required=True, help="Run mode of snooplyze: setup or fetch")
    parser.add_argument("-p", "--pooling-time", type=int, help="How often to pool data")


    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    print(args) # to delete

    if args.run_mode == 'fetch' and args.pooling_time is None:
        parser.error("--pooling_time is required when --run_mode is 'fetch'")


    if args.run_mode == 'setup':
        print("🔧 Running setup...")
        pe = PersistenceLayerSetup(persistence_engine=PersistenceEngine.DUCK_DB)
        pe.execute_setup()
    elif args.run_mode == 'fetch':
        print("📥 Fetching data...")
        fetch_csv(pooling_time=args.pooling_time)


if __name__ == "__main__":
    main()


    


