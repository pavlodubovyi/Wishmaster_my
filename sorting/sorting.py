import os
import re
import shutil
from pathlib import Path


class FileOrganizer:
    def __init__(self, folder):
    
        self.folder = folder
        self.directories = ['images', 'videos', 'documents', 'audio', 'archives', 'other']
        self.new_folders = {directory: list() for directory in self.directories}
        self.extensions_mapping = {
            'images': ['JPEG', 'JPG', 'PNG', 'SVG'],
            'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
            'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
            'archives': ['ZIP', 'GZ', 'TAR'],
            'other': []
        }
        self.translit_table = {
            1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd',
            1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z',
            1080: 'y', 1048: 'Y', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm',
            1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R',
            1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h',
            1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch',
            1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'ye', 1069: 'YE',
            1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji',
            1031: 'JI', 1169: 'g', 1168: 'G'
        }

    def normalize(self, filename):
        file = filename.name
        ext = file[file.rfind('.'):]
        normalized_file = file.removesuffix(ext)
        if normalized_file[normalized_file.rfind('.') + 1:].lower() == 'tar':
            ext = file[normalized_file.rfind('.'):]
            normalized_file = file.removesuffix(ext)
        normalized_file = normalized_file.translate(self.translit_table)
        normalized_file = re.sub(r'\W', '_', normalized_file)
        normalized_file += ext
        new_path = filename.parent / normalized_file
        if file != normalized_file:
            filename.rename(new_path)
        return new_path

    def sort_files(self):
        unknown_list = set()
        for file in self.folder.glob('**/*'):
            if file.is_dir() or not set(file.parts).isdisjoint(set(self.directories)):
                continue
            ext = str(file)[str(file).rfind('.') + 1:]
            for folder, ext_list in self.extensions_mapping.items():
                if ext.upper() in ext_list:
                    self.new_folders[folder].append(self.normalize(file))
                    break
                elif folder == 'other':
                    unknown_list.add(file.name)
                    self.new_folders[folder].append(file)
                    break
        return self.new_folders, list(unknown_list)

    def unpacker(self, archive):
        name = archive
        suffixes = len(name.suffixes)
        while suffixes:
            if Path(name).suffixes[-1][1:].upper() not in self.new_folders['archives']:
                break
            name = Path(name).stem
            suffixes = len(Path(name).suffixes)
        folder = archive.parent / name.stem
        shutil.unpack_archive(archive, folder)
        archive.unlink()
        return folder

    def create_directories(self, folders):
        for key, files in folders.items():
            new_folder = self.folder / key
            if not new_folder.exists():
                new_folder.mkdir()
            for file in files:
                if key == 'archives':
                    parent = file.parent
                    file = parent / self.unpacker(file)
                new_file = new_folder / file.name
                suffix = 1
                while new_file.exists():
                    text = file.name
                    text = 'copy_' + str(suffix) + '_' + text
                    new_file = new_folder / text
                    suffix += 1
                shutil.move(file, new_file)

    def delete_empty(self):
        for item in self.folder.glob('**/*'):
            if item.is_dir():
                try:
                    item.rmdir()
                except OSError:
                    pass


def main():
    while True:
        print('-' * 20)
        print('Сортування')
        print('-' * 20)
        print('1. Сортувати файли')
        print('2. Вийти')
        choice = input('Виберіть опцію: ')

        if choice == '1':
            folder = input('Введіть шлях до теки для сортування, або ENTER, щоб вийти: ')
            if os.path.isdir(folder):
                print(f'Організація файлів у теці: {folder}')
                organizer = FileOrganizer(Path(folder))
                folders, others = organizer.sort_files()
                organizer.create_directories(folders)
                organizer.delete_empty()

                print(f"Фото: {[i.name for i in folders['images']]}")
                print(f"Відео: {[i.name for i in folders['videos']]}")
                print(f"Документи: {[i.name for i in folders['documents']]}")
                print(f"Музика: {[i.name for i in folders['audio']]}")
                print(f"Розархівовані файли: {[i.name for i in folders['archives']]}")
                print(F"Інші: {others}")

                print('Сортування завершено.')

            elif not folder:
                print('Вихід...')
                break

            else:
                print('Невірний шлях до теки. Спробуйте ще раз.')

        elif choice == '2':
            print('Вихід...')
            break

        else:
            print('Невірний вибір. Спробуйте ще раз.')  # /Users/vova/Downloads/Мотлох


if __name__ == '__main__':
    main()
