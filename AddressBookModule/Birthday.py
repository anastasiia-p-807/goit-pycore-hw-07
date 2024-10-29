from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday(str):
    def __post_init__(self):
        try:
            self.value = datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise BirthdayValidtionException("Invalid date format. Use DD.MM.YYYY")
        
class BirthdayValidtionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"
