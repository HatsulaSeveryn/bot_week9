import re

CONTACTS = {}


def input_error(message: str = ''):
    """
    Decorator function for handling input errors
    :param message: optional parameter to specify the input error
    """

    def inner(handler):
        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception as error_:
                print(error_, '\n', message)

        return wrapper

    return inner


@input_error()
def hello_handler(*args):
    # Simple greeting function
    print('Hello how can I help you?')


@input_error('Please enter command as follows: add {name} {phone}')
def add_handler(name: str, phone: str, *args):
    # Function to add name and phone to contacts
    CONTACTS[name] = phone
    print(f'{name} {phone} added to contacts')


@input_error('Please enter command as follows: change {name} {phone}')
def change_handler(name: str, phone: str, *args):
    # Function that changes phone number of existing contact
    print(f'{name} phone {CONTACTS[name]} changed to {phone}')
    CONTACTS[name] = phone


@input_error(('Please enter command as follows: phone {name}'))
def phone_handler(name, *args):
    # Function that prints phone number
    print(f'{name} phone is {CONTACTS[name]}')


@input_error()
def show_all_handler(*args):
    print(CONTACTS)


@input_error()
def good_bye_handler(*args):
    # Simple exit function
    print('Good bye!')
    quit()


@input_error()
def input_parser(user_command: str):
    """
    Function for parsing input information
    :param user_command: input from user for parsing
    """
    commands = {
        'hello': hello_handler,
        'add': add_handler,
        'change': change_handler,
        'phone': phone_handler,
        'show all': show_all_handler,
        'good bye': good_bye_handler,
        'close': good_bye_handler,
        'exit': good_bye_handler
    }
    # Pattern for commands(add, change, phone) that require additional arguments
    complex_commands_patterns = (
        re.compile(r'^add [a-zA-Z]{3,20} [+]?\d{10,20}$'),
        re.compile(r'^change [a-zA-Z]{3,20} [+]?\d{10,20}$'),
        re.compile(r'^phone [a-zA-Z]{3,20}')
    )
    if user_command in commands:
        commands[user_command]()
    elif any(regex.match(user_command) for regex in complex_commands_patterns):
        user_command = user_command.split()
        commands[user_command[0]](*user_command[1:])
    else:
        print('Wrong command')


def main():
    while True:
        input_parser(input('...').lower())


if __name__ == '__main__':
    main()
