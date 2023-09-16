from .note import Notebook
import os


def saved_files():

    directory = "."  # шлях до каталогу
    extension = ".pickle"  # розширення файлу
    files = []  # список файлів

    # проходимо по всіх елементах у каталозі
    for element in os.listdir(directory):
        # якщо елемент є файлом і має потрібне розширення
        if os.path.isfile(os.path.join(directory, element)) and element.endswith(extension):

            # отримуємо базове ім'я файлу без розширення
            name = os.path.splitext(element)[0]
            # додаємо ім'я файлу до списку
            files.append(name)

    # повертаємо список файлів
    return files


def main():

    notebook = Notebook()

    while True:

        # Виводимо меню з можливими діями
        print("Виберіть дію:")
        print("1 - Створити нотатку")
        print("2 - Редагувати нотатку")
        print("3 - Видалити нотатку")
        print("4 - Пошук по тексту")
        print("5 - Пошук за ключовим словом")
        print("6 - Показати створені нотатки")
        print("7 - Сортування по даті створення")
        print("8 - Завантажити нотатку")
        print("9 - Видалити вибраний файл")
        print("10 - Зберегти та вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                # Зчитуємо текст нотатки
                text = input("Введіть текст нотатки: ")
                keywords = input("Введіть ключові слова нотатки, розділені комами з пробілами: ").split(
                    ",")  # Зчитуємо ключові слова нотатки, розділені комами
                keywords = [kw.strip(' ')
                            for kw in keywords]  # Видаляємо зайві пробіли
                notebook.add_note(text, keywords)  # Додаємо нову нотатку
                print("Нотатку додано")

        elif choice == "2":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                notebook.print_notes()

                # Зчитуємо індекс нотатки для редагування
                try:
                    index = int(
                        input("Введіть індекс нотатки для редагування: "))

                except ValueError:
                    print('Введіть індекс нотатки')

                # Зчитуємо новий текст нотатки або залишаємо пустим
                text = input("Введіть новий текст нотатки чи залиште пустим: ")
                keywords = input("Введіть нові ключові слова нотатки, розділені комами, чи залиште пустим: ").split(
                    ", ")  # Зчитуємо нові ключові слова нотатки або залишаємо пустим

                if text or keywords:  # Якщо текст або ключові слова не пусті

                    try:
                        # Редагуємо нотатку за індексом
                        notebook.edit_note(index-1, text, keywords)
                        print("Нотатку відредаговано")
                    #  Перехоплюємо помилку з відсутністю нотатки
                    except UnboundLocalError:
                        print(
                            'Нотатки з таким індексом не існує. Створіть нову через пункт 1')

                else:
                    # Якщо текст і ключові слова пусті, то виводимо повідомлення про помилку
                    print("Немає даних для редагування")

        elif choice == "3":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                notebook.print_notes()
                # Зчитуємо індекс нотатки для видалення
                index = int(input("Введіть індекс нотатки для видалення: "))
                notebook.delete_note(index-1)  # Видаляємо нотатку за індексом

        elif choice == "4":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:
                # Зчитуємо текст для пошуку
                text = input("Введіть текст для пошуку: ")
                results = notebook.search_by_text(
                    text)  # Пошук нотаток за текстом
                # Виводимо кількість знайдених нотаток
                print(f"Знайдено {len(results)} нотаток:")

                for note in results:  # Проходимо по всіх знайдених нотатках
                    print(note)  # Виводимо рядкове представлення нотатки

        elif choice == "5":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                # Зчитуємо ключове слово для пошуку
                keyword = input("Введіть ключове слово для пошуку: ")
                # Пошук нотаток за ключовим словом
                results = notebook.search_by_keyword(keyword)
                # Виводимо кількість знайдених нотаток
                print(f"Знайдено {len(results)} нотаток:")

                for note in results:  # Проходимо по всіх знайдених нотатках
                    print(note)

        elif choice == "6":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:
                notebook.print_notes()  # Виводить нотатки на екран

        elif choice == "7":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                reverse = int(
                    input("Введіть напрямок сортування (1 - спадання, 0 - зростання): "))
                # Сортуємо список нотаток за датою створення
                notebook.sort_by_date(reverse)
                print("Нотатки відсортовано")

        elif choice == "8":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                print(saved_files())

                filename = input(
                    'Введіть назву файлу без розширення ') + ".pickle"

                try:
                    # Завантажуємо нотатки з файлу
                    notebook.load_from_file(filename)

                except FileNotFoundError:
                    print('Файл не знайдено. Спробуйте ввести знову')

        elif choice == "10":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Вийти (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                if len(notebook.notes):

                    # Зберігаємо список нотаток у файл
                    notebook.save_to_file()
                    print("Нотатки збережено")
                    break

                else:
                    break

        elif choice == "9":

            # Додаємо пропозицію повернутися у цикл вибору
            result = input("Продовжити (y) чи повернутися у меню вибору (n)? ")
            if result == "n":
                continue

            else:

                while True:
                    try:
                        # Видаляємо вибраний файл з каталогу
                        notebook.delete_selected_file()
                        break
                    except ValueError:
                        print("Введіть, будь ласка, номер файлу")
                        continue

        else:
            print("Невірний вибір")


if __name__ == '__main__':
    main()
