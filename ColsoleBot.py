from enum import Enum
from AddressBook import AddressBook
from Birthday import Birthday
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
    while True:
        if len(args) != 2:
            user_input = input("Please provide a name and a new phone number (e.g. 'John 1234567890'): ")
            args = user_input.split()
        else: break
    
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
    while True:
        if len(args) != 3:
            user_input = input("Please provide an existing name, phone and a new phone (e.g. 'John 123456 789034'): ")
            args = user_input.split()
        else: break
    
    name, old_phone, new_phone = args[0].rstrip(), args[1].rstrip(), args[2].rstrip()
    record = addressBook.find(name)
    record.edit_phone(Phone(old_phone), Phone(new_phone)) # Phone has validation, exception may occur 
    return addressBook.update(record) # exception may occur if record is not found 

@input_error 
def get(args: list) -> Record: # args expected to be: 'Name'
    while True:
        if len(args) != 1:
            user_input = input("Please provide an existing name (e.g. 'John'): ")
            args = user_input.split()
        else: 
            name = args[0] 
            break
    return addressBook.find(name)

@input_error 
def print_all() -> str:
    if len(addressBook) == 0:
        return "Empty list."
    print('\n'.join(f"{record}" for record in addressBook.get_all()))

@input_error
def add_birthday(args): # args expected to be: 'Name DD.MM.YYYY'
    while True:
        if len(args) < 2:
            user_input = input("Please provide a name and date (e.g. 'John DD.MM.YYYY'): ")
            args = user_input.split()
        else: break
    
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

class Command(Enum):
    GREET = "greet"
    CLOSE = "exit"
    ADD = "add"
    UPDATE = "update"
    GET = "get"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"

commands = {
    Command.GREET: ["hi", "hello", "whatsup"],
    Command.CLOSE: ["close", "exit", "bye", "disappear"],
    Command.ADD: ["new", "add"],
    Command.UPDATE: ["update", "change", "edit"],
    Command.GET: ["get", "phone", "find"],
    Command.ALL: ["all", "show all", "get all"],
    Command.ADD_BIRTHDAY: ["add-birthday"],
    Command.SHOW_BIRTHDAY: ["show-birthday"],
    Command.BIRTHDAYS: ["birthdays"]
}
    
def parse_input(user_input: str):
    if not user_input.strip():
        return None, []  
    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input(f"Enter a command ( like { ', '.join(values[0] for values in commands.values())})")
        command, args = parse_input(user_input)
        
        if command is None:
            print("No command entered, please try again.")
            continue
        
        try:
            if command in commands[Command.GREET]:
                print("Hey. How can I help you?")
            
            elif command in commands[Command.CLOSE]:
                print("Good bye!")
                break
            
            elif command in commands[Command.ADD]: #Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує
                record = add(args)
                print(f"Contact added: {record}")
            
            elif command in commands[Command.UPDATE]: #Змінити телефонний номер для вказаного контакту.
                record = update_phone(args)
                print(f"Contact updated: {record}")
            
            elif command in commands[Command.GET]: #I decided to show the ehole record here.
                record = get(args)
                print(record if record else "Record is not found")
            
            elif command in commands[Command.ALL]:
                print_all()
            
            elif command in commands[Command.ADD_BIRTHDAY]: #Додати дату народження для вказаного контакту.
                add_birthday(args)
                print(f"Birthday aded")
            
            elif command in commands[Command.SHOW_BIRTHDAY]: #Показати дату народження для вказаного контакту.
                print(f"Birthday: {get_birthday(args)}")
            
            elif command in commands[Command.BIRTHDAYS]: #Показати дні народження, які відбудуться протягом наступного тижня.
                records = addressBook.get_upcoming_birthdays()
                print(records)
            
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"An error occurred: {e}. Try again.")
        
        print("\n")


if __name__ == "__main__":
    main()
