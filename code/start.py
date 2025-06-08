from data_parse.data_parse import *
from page.page import Page, PageMonitor
import time

if __name__ == "__main__":
    
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassDataParse(div_class_name = "newstiles"), timeout = 10)

    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentDataParse(), timeout = 10)

    duckdb_monitor.check_for_update()
    databricks_monitor.check_for_update()

    # Poll every 60 seconds
    while True:
        time.sleep(60)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]


