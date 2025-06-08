from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class DataParse(ABC):
    
    @abstractmethod
    def parse(self, text_to_parse):
        pass

class AllDocumentDataParse(DataParse):

    def __init__(self):
        pass

    def parse(self, text_to_parse):
            soup = BeautifulSoup(text_to_parse, 'html.parser')
            
            # Extract main content - for now, just the whole body text
            #content = soup.body.get_text(separator=' ', strip=True)
            content = soup.body
            return content
    
class MainElementDataParse(DataParse):
     
    def __init__(self):
        pass

    def parse(self, text_to_parse):
        
        soup = BeautifulSoup(text_to_parse, 'html.parser')
            
        # Extract main content - for now, just the whole body text
        content = soup.find('main')
        return content
    
        #return content.get_text(separator = ' ', strip=True)

class DivClassDataParse(DataParse):
     
    def __init__(self, div_class_name : str):
        self.div_class_name = div_class_name

    def parse(self, text_to_parse):

        soup = BeautifulSoup(text_to_parse, 'html.parser')
            
        # Extract main content - for now, just the whole body text
        content = soup.find('div', class_ = self.div_class_name)
    
        if content:
            #return content.get_text(separator = ' ', strip=True)
            return content
