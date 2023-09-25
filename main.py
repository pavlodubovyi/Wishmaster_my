from phonebook.phonebook_SOLID import main as phonebook_main
from sorting.sorting_SOLID import main as sorting_main
from notes.wrap import main as notes_main


def main():
    while True:
        print("-" * 20)
        print('BOT Wishmaster')
        print("-" * 20)
        print("1. Адресна книга")
        print("2. Сортування")
        print("3. Нотатки")
        print("4. Вийти")
        print("-" * 20)

        choice = input("Виберіть дію: ")

        if choice == '1':
            # Виклик функціональності з phonebook_SOLID.py
            phonebook_main()

        elif choice == '2':
            # Виклик функціональності з sorting_SOLID.py
            sorting_main()
            pass

        elif choice == '3':
            # Виклик функціональності з wrap.py
            notes_main()

        elif choice == '4':
            break


if __name__ == "__main__":
    main()
