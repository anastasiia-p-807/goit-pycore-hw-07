from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday:
    def __init__(self, date: str):
        self._date = None
        self.date = date
    
    @property
    def date(self) -> datetime:
        return self._date
    
    @date.setter
    def date(self, new_date: str):
        try:
            self._date = datetime.strptime(new_date, "%d.%m.%Y")
        except ValueError:
            raise BirthdayValidtionException("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return f"{self.date.strftime("%Y-%m-%d")}"
    
class BirthdayValidtionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"
