from collections.abc import Callable
from functools import wraps


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """Перетворює помилки введення на повідомлення для користувача."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter a contact name."
        except ValueError:
            return "Give me name and phone please."

    return wrapper


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()
    if not parts:
        return "", []
    command, *args = parts
    return command.lower(), args


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    name = args[0]
    if len(args) > 1:
        return "Enter only the contact name."
    return contacts[name]


def show_all(contacts: dict[str, str]) -> str:
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items()) or "No contacts saved."


def main() -> None:
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)
        if command in {"close", "exit"}:
            print("Good bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
