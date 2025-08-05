from dataclasses import dataclass
import yaml

# import snooplyze modules
from snooplyze.page import PageMonitor, Page
from snooplyze.parser import ParserType, get_parser, DivClassParser


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
            page_description = item.get('description') # get description element from Pages config (optional element)
            page_parser = item['parser'] # get parser section from Pages config

            if "parser" in item:
                page_parser_type = page_parser[0].get('type').lower()

                # TODO: eliminate this ugly if-else structure by adapting a parser registry pattern
                # also for the cases with parameters
                
                # Special case of Perser (DivClassParser) as it has a different structure
                if page_parser_type == ParserType.DIV_CLASS:
                    class_name = page_parser[0].get('class_name')
                    parser_config_variables = {'class_name': class_name}
                    parser_config = DivClassParser(**parser_config_variables)
                else:
                    # For the rest Parsers, use parser registry pattern
                    parser_config_variables = {}
                    parser_config = get_parser(ParserType(page_parser_type))

            else:
                ValueError(f"No parser secion for Page {page_name}")
            

            if parser_config is None:
                raise ValueError("No valid Parser has been found")

            page = Page(name=page_name,url=page_url, description=page_description)
            page_monitors.append(PageMonitor(page=page,parser=parser_config))
        
        return page_monitors
