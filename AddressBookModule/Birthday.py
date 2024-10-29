from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday(str):
    def __post_init__(self):
        try:
            self.value = datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")