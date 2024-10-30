import re
from dataclasses import dataclass


@dataclass
class Phone:
    def __init__(self, phone: str):
        self._phone = None
        self.phone = phone
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return bool(re.fullmatch(r'\d{3}', phone))
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, new_phone: str):
        if not Phone.is_valid_phone(new_phone):
            raise PhoneValidtionException("Phone number must contain exactly 10 digits.")
        self._phone = new_phone
    
    def __str__(self):
        return f"{self.phone}"
    
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.phone == other.phone
        return False
    
class PhoneValidtionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"
