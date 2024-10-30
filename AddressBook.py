import uuid
from typing import List
from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, timedelta
from Record import Record
from NewRecord import NewRecord


@dataclass
class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        
    @property
    def count(self):
        return self.count
    
    # Record
    def add(self, new_record: NewRecord) -> Record:
        phones = new_record.phones
        record = Record(name=new_record.name, phones=phones)
        self.data[record.id] = record
        return self.data[record.id]

    def find(self, name: str) -> Record:
        return next((record for record in self.data.values() if record.name.name == name), None)

    def delete(self, name: str):
        record_id = next((record_id for record_id, record in self.data.items() if record.name.name == name), None)
        if record_id:
            del self.data[record_id]

    def get(self, record_id: uuid.UUID) -> Record:
        return self.data[record_id]
    
    def get_all(self) -> List[Record]:
        return self.data.values()

    def update(self, updated_record: Record) -> Record:
        existing_record = self.data.get(updated_record.id)
        if not existing_record:
            raise KeyError("Record not found.")
        existing_record.name = updated_record.name
        existing_record.phones = updated_record.phones
        return existing_record

    # Birthdays          
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthdays = []

        for person in self.data.values():
            birthday_this_year = person.birthday.date.replace(year=today.year).date()

            if birthday_this_year < today:
                birthday_this_year = person.birthday.date.replace(year=today.year + 1).date()

            if today <= birthday_this_year <= end_date:
                day_of_week = birthday_this_year.weekday()
                if day_of_week in (5, 6):  # Saturday or Sunday
                    delta_days = 7 - day_of_week
                    congratulation_date = birthday_this_year + timedelta(days=delta_days)
                else:
                    congratulation_date = birthday_this_year

                upcoming_birthdays.append({
                    "name": person.name.name,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                })

        return upcoming_birthdays
    