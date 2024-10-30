from dataclasses import dataclass


@dataclass
class Name:
    def __init__(self, name: str):
        self._name = None
        self.name = name
        
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str):
        self._name = new_name
        
    def __str__(self):
        return f"{self.name}"