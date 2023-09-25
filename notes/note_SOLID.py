import datetime
import os.path
import pickle
from abc import ABC, abstractmethod

class AbstractNote(ABC):

    def __init__(self, text='', keywords=None):
        self.text = text
        self.keywords = keywords
        self.date = datetime.date.today()

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_keywords(self):
        pass

class Note(AbstractNote):
    def __str__(self):
        return f"Text: {self.text}\nKeywords: {', '.join(self.keywords)}\nDate: {self.date}"

    def get_text(self):
        return self.text

    def get_keywords(self):
        return self.keywords


# Клас, який представляє записник з нотатками.
class Notebook:

    # Конструктор класу, який ініціалізує порожній список нотаток.
    def __init__(self):
        self.notes = []  # Список нотаток.

    # Метод, який додає нову нотатку до нотатника.
    def add_note(self, note):
        self.notes.append(note)  # Додаємо нову нотатку до списку.

    # Метод, який редагує існуючу нотатку за її індексом у списку.
    def edit_note(self, index, text=None, keywords=None):

        # Перевіряємо, чи є такий індекс у списку нотаток.
        if 0 <= index < len(self.notes):
            note = self.notes[index]
            if text:  # Якщо заданий новий текст, то змінюємо текст нотатки.
                note.text = text

            if keywords:  # Якщо заданий новий список ключових слів, то змінюємо ключові слова нотатки.
                note.keywords = keywords

        else:
            print("Неправильно введений індекс")

    # Метод, який видаляє існуючу нотатку за її індексом у списку.
    def delete_note(self, index):

        # Перевіряємо, чи є такий індекс у списку нотаток.
        if 0 <= index < len(self.notes):
            self.notes.pop(index)  # Видаляємо нотатку за індексом.
            print("Нотатку видалено")

        else:
            print("Неправильно введений індекс")

    # Метод, який повертає список нотаток, які містять заданий текст у своїх полях.
    def search_by_text(self, text):

        results = []
        for note in self.notes:  # Проходимо по всіх нотатках у нотатнику.

            # Переводимо текст нотатки та запит у нижній регістр.
            note_text = note.text.lower()
            query = text.lower()

            if query in note_text:  # Перевіряємо, чи є запит у тексті нотатки.
                results.append(note)

        return results

    # Метод, що повертає список нотаток, які мають задане ключове слово у своїх полях.
    def search_by_keyword(self, keyword):

        results = []
        for note in self.notes:

            # Переводимо ключове слово та запит у нижній регістр.
            note_keywords = [k.lower() for k in note.keywords]
            query = keyword.lower()

            if query in note_keywords:
                results.append(note)

        return results

    # Метод, який сортує список нотаток за датою створення в порядку зростання або спадання.
    def sort_by_date(self, reverse=False):

        # Використовуємо метод sort для списку нотаток, вказавши ключ сортування та напрямок.
        self.notes.sort(key=lambda note: note.date, reverse=reverse)

    # Метод, який зберігає список нотаток у pickle файл.
    def save_to_file(self, filename=None):
        '''
          |============================
          | Залишаю filename і його обробку у цьому методі, для можливості
          | розширення. Наприклад, для збереження нотаток вручну.
          |============================
        '''

        # if not filename:

        for note in self.notes:  # Проходимо по всіх нотатках у нотатнику.

            text = note.text  # Отримуємо текст нотатки.
            words = text.split()  # Розбиваємо текст на слова за пробілами.

            if words:
                # Якщо є хоча б одне слово, то використовуємо перше слово як ім'я файлу.
                file = words[0] + ".pickle"
                break

            else:
                # Якщо немає слів, то використовуємо дату створення нотатки як ім'я файлу.
                file = str(note.date) + ".pickle"
                break

        if os.path.exists(file):

            path_list = file.split('.')
            file = path_list[0] + '1.' + path_list[1]
            with open(file, "wb") as f:
                pickle.dump(self, f)

        else:
            with open(file, "wb") as f:
                pickle.dump(self, f)

        # else:

        #     filename = filename + '.pickle'
        #     with open(filename, "wb") as file:

        #         pickle.dump(self, file)

    # Метод, який завантажує список нотаток з файлy.
    def load_from_file(self, filename):

        with open(filename, "rb") as file:

            old_notebook = pickle.load(file)
            for note in old_notebook.notes:
                print(note)
                self.notes.append(note)

    def print_notes(self):

        for i, note in enumerate(self.notes):
            print(f"{i+1}. {note}")

    def show_saved_files(self):

        directory = ".\\"  # шлях до каталогу
        extension = ".pickle"  # розширення файлу
        files = []  # список файлів

        # проходимо по всіх елементах у каталозі
        for element in os.listdir(directory):
            # якщо елемент є файлом і має потрібне розширення
            if os.path.isfile(os.path.join(directory, element)) and element.endswith(extension):

                # додаємо ім'я файлу до списку
                files.append(element)

        # виводимо список файлів на екран
        print("Збережені файли:")
        for i, file in enumerate(files):
            print(f"{i + 1} - {file}")

        # повертаємо список файлів
        return files

    # Метод, який видаляє вибраний файл з каталогу.
    def delete_selected_file(self):

        directory = ".\\"
        files = self.show_saved_files()  # отримуємо список файлів

        if files:  # якщо список не пустий

            # зчитуємо номер файлу для видалення
            number = int(input("Введіть номер файлу для видалення: "))

            if 1 <= number <= len(files):  # якщо номер в межах списку

                file = files[number - 1]  # отримуємо ім'я файлу за номером
                # видаляємо файл з каталогу
                os.remove(os.path.join(directory, file))
                print(f"Файл {file} видалено")

            else:
                print("Невірний номер")

        else:
            print("Немає збережених файлів")
