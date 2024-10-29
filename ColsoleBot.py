from datetime import datetime
from AddressBook import AddressBook
from Name import Name
from NewRecord import NewRecord
from Phone import Phone
from Record import Record


addressBook = AddressBook()

def add(args: list) -> Record: # args expected to be: 'Name Phone'
    if len(args) < 2:
        user_input = input("Please provide a name and a new phone number (e.g. 'John 1234567890'): ")
        args = user_input.split()
    
    name, phone = args[0].rstrip(), args[1].rstrip()
    record = addressBook.find(name)
    if record:
        record.add_phone(phone)
        return addressBook.update(record)
    else: 
        return addressBook.add(NewRecord(name=Name(name), phones=[Phone(phone)]))

def edit_phone(args: list) -> Record: # args expected to be: 'Name OldPhone NewPhone'
    if len(args) < 2:
        user_input = input("Please provide an existing name, phone and a new phone (e.g. 'John 123456 789034'): ")
        args = user_input.split()
    
    name, old_phone, new_phone = args[0].rstrip(), args[1].rstrip()
    record = addressBook.find(name)
    if record.edit_phone(old_phone, new_phone):
        return addressBook.update(record)
    return None

def get(args: list) -> Record: # args expected to be: 'Name'
    if len(args) < 1:
        user_input = input("Please provide an existing name (e.g. 'John'): ")
        args = user_input.rstrip()
    name = args[0]
    return addressBook.find(name)

def print_all() -> str:
    if addressBook.count == 0:
        return "Empty list."
    print('\n'.join(f"{record}" for record in addressBook.get_all()))

def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return f"Error: {str(e)}"
        return wrapper

# to do this
@input_error
def add_birthday(args):
    if len(args) < 2:
        user_input = input("Please provide a name and a new phone number (e.g. 'John 1234567890'): ")
        args = user_input.split()
    
    name, phone = args[0].rstrip(), args[1].rstrip()
    contacts[name] = phone
    return "Contact added."

    try:
        name, date_str = args.split()
        record = book.find(name)
        if not record:
            return "Contact not found."
        birthday = datetime.strptime(date_str, "%d.%m.%Y")
        record.birthday = birthday
        return f"Birthday added for {name}: {date_str}"
    except ValueError:
        return "Please provide the date in DD.MM.YYYY format."

@input_error
def show_birthday(args, book):
        # реалізація

@input_error
def birthdays(args, book):
        # реалізація



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
            elif command in ["new", "add"]:
                record = add(args)
                print(f"Contact added: {record}")
            elif command in ["change", "update"]:
                record = edit_phone(args)
                print(f"Contact updated: {record}")
            elif command in ["get", "get phone", "find"]:
                record = get(args)
                print(f"Record: {record}")
            elif command in ["all", "show"]:
                print_all()
            elif command == "add-birthday":
                add_birthday(args)
            elif command == "show-birthday":
                show_birthday(args)
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