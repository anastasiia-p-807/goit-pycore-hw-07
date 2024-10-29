import uuid
from dataclasses import dataclass, field
from Birthday import Birthday
from Name import Name
from Phone import Phone


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
        if not old_phone_obj:
            raise KeyError(f"Phone of the record (name = {self.name} not found.")
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
        return f"Name: {self.name.value}, phones: {phones}"