from datetime import datetime
from AddressBook import AddressBook
from Birthday import Birthday, BirthdayValidtionException
from Name import Name
from NewRecord import NewRecord
from Phone import Phone
from Record import Record


addressBook = AddressBook()


def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                print(f"Log Error: {str(ex)}")
                raise ex from None
        return wrapper
    
@input_error
def add(args: list) -> Record: # args expected to be: 'Name Phone'
    if len(args) < 2:
        user_input = input("Please provide a name and a new phone number (e.g. 'John 1234567890'): ")
        args = user_input.split()
    
    name, phone = args[0].rstrip(), args[1].rstrip()
    new_phone = Phone(phone) # Phone has validation, exception may occur 
    record = addressBook.find(name)
    if record:
        record.add_phone(new_phone)
        return addressBook.update(record)
    else: 
        return addressBook.add(NewRecord(name=Name(name), phones=[new_phone]))

@input_error 
def update_phone(args: list) -> Record: # args expected to be: 'Name OldPhone NewPhone'
    if len(args) < 2:
        user_input = input("Please provide an existing name, phone and a new phone (e.g. 'John 123456 789034'): ")
        args = user_input.split()
    
    name, old_phone, new_phone = args[0].rstrip(), args[1].rstrip()
    record = addressBook.find(name)
    if record.edit_phone(Phone(old_phone), Phone(new_phone)): # Phone has validation, exception may occur 
        return addressBook.update(record) # exception may occur if record is not found 
    return None

@input_error 
def get(args: list) -> Record: # args expected to be: 'Name'
    name = None
    if len(args) < 1:
        name = input("Please provide an existing name (e.g. 'John'): ")
    else:
        name = args[0]
    return addressBook.find(name)

def print_all() -> str:
    if addressBook.count == 0:
        return "Empty list."
    print('\n'.join(f"{record}" for record in addressBook.get_all()))

@input_error
def add_birthday(args): # args expected to be: 'Name DD.MM.YYYY'
    if len(args) < 2:
        user_input = input("Please provide a name and date (e.g. 'John DD.MM.YYYY'): ")
        args = user_input.split()
    
    name, date = args[0].rstrip(), args[1].rstrip()
    record = addressBook.find(name)
    if record is None:
        raise KeyError("Record not found.") 
    birthday = Birthday(date) # Birthday has validation, exception may occur
    record.set_birthday(birthday)
    addressBook.update(record) # exception may occur if record is not found 

@input_error
def get_birthday(args) -> Birthday: # args expected to be: 'Name'
    name = None
    if len(args) < 1:
        name = input("Please provide an existing name (e.g. 'John'): ")
    else:
        name = args[0]
    record = addressBook.find(name)
    if record is None:
        raise KeyError("Record not found.") 
    return record.birthday

def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        try:
            if command in ["hi", "hello", "whatsup"]:
                print("How can I help you?")
            elif command in ["close", "exit", "bye", "disappear"]:
                print("Good bye!")
                break
            elif command in ["new", "add"]: #Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує
                record = add(args)
                print(f"Contact added: {record}")
            elif command in ["change", "update"]: #Змінити телефонний номер для вказаного контакту.
                record = update_phone(args)
                print(f"Contact updated: {record}")
            elif command in ["get", "phone", "get phone", "find"]: #Показати телефонні номери для вказаного контакту.
                record = get(args)
                print(f"Record: {record}")
            elif command in ["all", "show all", "get all"]:
                print_all()
            elif command == "add-birthday": #Додати дату народження для вказаного контакту.
                add_birthday(args)
            elif command == "show-birthday":
                print(get_birthday(args))
            elif command == "birthdays":
                records = addressBook.get_upcoming_birthdays()
                print(records)
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"An error occurred: {e}. Try again.")

if __name__ == "__main__":
    main()
    
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args