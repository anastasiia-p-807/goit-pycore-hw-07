import re
from dataclasses import dataclass


@dataclass
class Phone(str):
    def __post_init__(self):
        if not self._is_valid_phone(self.value):
            raise ValueError("Phone number must contain exactly 10 digits.")

    @staticmethod
    def _is_valid_phone(value: str) -> bool:
        return bool(re.fullmatch(r'\d{10}', value))