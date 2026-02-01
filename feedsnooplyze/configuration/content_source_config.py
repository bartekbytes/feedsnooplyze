from dataclasses import dataclass
import yaml

# import feedsnooplyze modules
from feedsnooplyze.sourcer.page import Page, PageMonitor, page
from feedsnooplyze.sourcer.rss import RSS, RSSMonitor
from feedsnooplyze.parser import ParserType, get_parser, DivClassParser


@dataclass
class ContentSourceConfig:
    pages_config: list[Page]
    rsses_config: list[RSS]

@dataclass
class ContentSourceConfigReader:
    path_to_file: str
    
    def read(self) -> str:
        with open(self.path_to_file) as f:
            return f.read()


class ContentSourceConfigLoader:
    def __init__(self, reader: ContentSourceConfigReader):
        self.reader = reader


    def load_config(self) -> ContentSourceConfig:
        yaml_str = self.reader.read()
        return self._parse_config(yaml_str)


    def _parse_config(self, yaml_str: str) -> ContentSourceConfig:
        data = yaml.safe_load(yaml_str)

        page_monitors = []
        rss_monitors = []

        pages_config_list = data.get("Pages", [])
        rsses_config_list = data.get("RSS", [])
    
        if pages_config_list:
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

                        if parser_config is None:
                            raise ValueError("No valid Parser has been found")

                else:
                    raise ValueError(f"No parser section for Page {page_name}")
            
                page = Page(name=page_name,url=page_url, description=page_description)
                page_monitors.append(PageMonitor(page=page,parser=parser_config))


        if rsses_config_list:
            for item in rsses_config_list:
                rss_name = item['name'] # get name element from RSS config
                rss_url = item['url'] # get URL element from RSS config
                rss_description = item.get('description') # get description element from RSS config (optional element)

                rss = RSS(name=rss_name, url=rss_url, description=rss_description)
                rss_monitors.append(RSSMonitor(rss=rss))
        
        return ContentSourceConfig(
                    pages_config=page_monitors,
                    rsses_config=rss_monitors
                )