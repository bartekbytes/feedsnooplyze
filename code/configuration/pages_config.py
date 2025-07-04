from dataclasses import dataclass
from typing import List
import yaml

from page.page import PageMonitor, Page
from persistence.persistence_engine import *
from parser.generic_parsers import *
from parser import *

from configuration.config import Config


@dataclass
class PagesConfig:
    pages_config: list[Page]

@dataclass
class PagesConfigReader:
    path_to_file: str
    
    def read(self) -> str:
        with open(self.path_to_file) as f:
            return f.read()


class PagesConfigLoader:
    def __init__(self, reader: PagesConfigReader):
        self.reader = reader


    def load_config(self) -> list[PageMonitor]:
        yaml_str = self.reader.read()
        return self._parse_config(yaml_str)


    def _parse_config(self, yaml_str: str) -> list[PageMonitor]:
        data = yaml.safe_load(yaml_str)
        pages_config_list = data.get("Pages", [])
    
        page_monitors = []

        for item in pages_config_list:
            page_name = item['name'] # get name element from Pages config
            page_url = item['url'] # get URL element from Pages config
            page_parser = item['parser'] # get parser section from Pages config

            if "parser" in item:
                page_parser_type = page_parser[0].get('type').lower()
                cls = PARSER_REGISTRY.get(page_parser_type) # Check if there a class registered in Parser Registry
                if not cls:
                    raise ValueError(f"Unknown Parser type: {page_parser_type}")
                
                print(f"Class of parser {page_parser_type}") # TODO: to delete

                # TODO: these if's here are ugly, must be refactored ASAP!
                if page_parser_type == "alldocument":
                    parser_config_variables = {}
                    #parser_config = cls.from_dict({})
                    parser_config = AllDocumentParser(**parser_config_variables)

                if page_parser_type == "mainelement":
                    parser_config_variables = {}
                    #parser_config = cls.from_dict({})
                    parser_config = MainElementParser(**parser_config_variables)

                if page_parser_type == "divclass":
                    value = page_parser[0].get('class_name')
                    parser_config_variables = {'class_name': value}
                    #parser_config = cls.from_dict(**parser_config_variables)
                    parser_config = DivClassParser(**parser_config_variables)
            else:
                ValueError(f"No parser secion for Page {page_name}")
            
            #elif "pool_time" in item:
                #general_config.pool_time = item["pool_time"]

            if parser_config is None:
                raise ValueError("No persistence configuration found")

            page = Page(name=page_name,url=page_url)
            #page_monitors.append(PageMonitor(page=page,parser=PARSER_REGISTRY.get(page_parser_type).(**parser_config_variables), persistence=None))
            page_monitors.append(PageMonitor(page=page,parser=parser_config))
        return page_monitors




@dataclass
class PagesConfig:
    path_to_file: str
    persistence: PersistenceEngine

    # obsolete
    def _check_pages_part(self, page_data):
        print(page_data)

        # check if all dict keys are available
        required_keys = ['name', 'url', 'parser']
        
        # TODO: add checks on parser level as different parsers can have different set up
        for pd in page_data:
            if set(required_keys).issubset(pd):
                print("All required keys are present")
            else:
                missing_keys = set(required_keys) - pd.keys()
                print("Some required keys are missing")
                print(f"Missing keys are {missing_keys}")
                return False
            
        return True


    #def parse(self) -> bool:
        #with open(self.path_to_file) as f:
            #raw_data = yaml.safe_load(f)

            #pages_data = raw_data.get("pages", {})


            #pages_data_result = self._check_pages_part(page_data=pages_data)
            #print(pages_data_result)

            #if pages_data_result:
                #return True
            #else:
                #return False

    
    def process_config_data(self) -> list[PageMonitor] | None:

        with open(self.path_to_file) as f:
            
            raw_data = yaml.safe_load(f)

            page_data = raw_data.get("pages", {})

            monitors = []

            for p in page_data:
                parser_type = dict(p['parser'][0])['type']
                options = dict(p['parser'][0]).get('classname')
            
                if parser_type == 'divclass':
                    parser = DivClassParser(options)
                elif parser_type == 'alldocument':
                    parser = AllDocumentParser()

                page = Page(name = p['name'], url = p['url'])
                monitor = PageMonitor(page = page, parser = parser, persistence = self.persistence)
                monitors.append(monitor)


        return monitors