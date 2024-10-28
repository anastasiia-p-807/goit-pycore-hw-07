from collections import UserDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import re
import uuid

@dataclass
class Field:
    value: str

@dataclass
class Name(Field):
    pass

@dataclass
class Phone(Field):
    def __post_init__(self):
        if not self._is_valid_phone(self.value):
            raise ValueError("Phone number must contain exactly 10 digits.")
    
    @staticmethod
    def _is_valid_phone(value: str) -> bool:
        return bool(re.fullmatch(r'\d{10}', value))

@dataclass
class Birthday(Field):
    def __post_init__(self):
        try:
            self.value = datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


@dataclass
class Record:
    _id: uuid.UUID = field(default_factory=uuid.uuid4, init=False, repr=False)
    name: Name
    phones: list[Phone] = field(default_factory=list)
    birthday: Birthday = None

    @property
    def id(self) -> uuid.UUID:
        return self._id
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        old_phone_obj = self.find_phone(old_phone)
        if old_phone_obj:
            self.phones.remove(old_phone_obj)
            self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Phone:
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

@dataclass
class NewRecord:
    name: Name
    phones: list[Phone] = field(default_factory=list)
    
class AddressBook(UserDict):
    def add_record(self, new_record: NewRecord):
        record = Record(name=new_record.name, phones=new_record.phones)
        self.data[record.id] = record

    def find(self, name: str) -> Record:
        return next((record for record in self.data.values() if record.name.value == name), None)

    def delete(self, name: str):
        record_id = next((record_id for record_id, record in self.data.items() if record.name.value == name), None)
        if record_id:
            del self.data[record_id]
    
    def get(self, record_id: uuid.UUID) -> Record:
        return self.data.get(record_id)
    
    def edit_record(self, updated_record: Record) -> Record:
        existing_record = self.data.get(updated_record.id)
        if not existing_record:
            raise KeyError("Record not found.")
        
        existing_record.name = updated_record.name
        existing_record.phones = updated_record.phones
        return existing_record
        
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthdays = []

        for person in self.data:
            birthday_this_year = person.birthday.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = person.birthday.replace(year=today.year + 1)
            
            if today <= birthday_this_year <= end_date:
                day_of_week = birthday_this_year.weekday()
                if day_of_week in (5, 6):  # Saturday or Sunday
                    delta_days = 7 - day_of_week
                    congratulation_date = birthday_this_year + timedelta(days=delta_days)
                else:
                    congratulation_date = birthday_this_year

                upcoming_birthdays.append({
                    "name": person["name"],
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })

        return upcoming_birthdays