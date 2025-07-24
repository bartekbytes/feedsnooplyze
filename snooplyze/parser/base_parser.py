from abc import ABC, abstractmethod

class ParserBase(ABC):
    
    @abstractmethod
    def parse(self, text_to_parse):
        pass

    @classmethod
    @abstractmethod
    def validate(cls, data: dict) -> None:
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate(data)
        return cls(**data)