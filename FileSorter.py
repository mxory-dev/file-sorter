import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

TRANSLATIONS = {
    "en": {
        "title": "File Sorter",
        "instruction": "Please select the folder where files need to be sorted,\nor enter the path manually.",
        "browse": "Browse",
        "start": "Start sorting",
        "toggle": "RU",
        "completed_title": "Completed",
        "completed_message": "Sorting completed!",
        "error_title": "Error",
        "folder_required": "Please specify a folder to sort!",
        "folder_missing": "The folder does not exist!",
        "moved_file": "Moved file: {filename} -> {folder_name}",
        "results_header": "\nSorting results:",
        "sorted_count": "\nSorted {folder_name}: {count}",
        "total_count": "\nTotal files: {count}",
        "end": "Sorting finished",
    },
    "ru": {
        "title": "Сортировщик файлов",
        "instruction": "Пожалуйста, выберите папку, в которой необходимо\nотсортировать файлы, либо введите путь вручную.",
        "browse": "Обзор",
        "start": "Начать сортировку",
        "toggle": "EN",
        "completed_title": "Выполнено",
        "completed_message": "Сортировка завершена!",
        "error_title": "Ошибка",
        "folder_required": "Укажите папку для сортировки!",
        "folder_missing": "Папка не существует!",
        "moved_file": "Перемещён файл: {filename} -> {folder_name}",
        "results_header": "\nРезультаты сортировки:",
        "sorted_count": "\nОтсортировано {folder_name}: {count}",
        "total_count": "\nОбщее количество: {count}",
        "end": "Конец сортировки",
    },
}


def sort_img(sf, lang):
    texts = TRANSLATIONS[lang]
    extension_counts = {}
    moved_count = 0

    for filename in os.listdir(sf):
        file_path = os.path.join(sf, filename)

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower().lstrip('.')
        folder_name = extension if extension else 'no_extension'
        target_folder = os.path.join(sf, folder_name)

        os.makedirs(target_folder, exist_ok=True)

        destination_path = os.path.join(target_folder, filename)
        if os.path.exists(destination_path):
            base_name, file_extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(target_folder, f'{base_name} ({counter}){file_extension}')):
                counter += 1
            destination_path = os.path.join(target_folder, f'{base_name} ({counter}){file_extension}')

        shutil.move(file_path, destination_path)
        moved_count += 1
        extension_counts[folder_name] = extension_counts.get(folder_name, 0) + 1
        print(texts["moved_file"].format(filename=filename, folder_name=folder_name))

    print(texts["results_header"])
    for folder_name, count in sorted(extension_counts.items()):
        print(texts["sorted_count"].format(folder_name=folder_name, count=count))
    print(texts["total_count"].format(count=moved_count))
    print(texts["end"])

    messagebox.showinfo(texts["completed_title"], texts["completed_message"])


mw = tk.Tk()
current_lang = "en"

mw.title(TRANSLATIONS[current_lang]["title"])
mw.geometry('480x160')
mw.resizable(False, False)

header_frame = tk.Frame(mw)
header_frame.pack(fill=tk.X, padx=10, pady=(10, 6))

label_var = tk.StringVar(value=TRANSLATIONS[current_lang]["instruction"])
label = tk.Label(header_frame, textvariable=label_var, justify="center", wraplength=430)
label.pack(side=tk.LEFT, expand=True)


def toggle_language():
    global current_lang
    current_lang = "ru" if current_lang == "en" else "en"
    texts = TRANSLATIONS[current_lang]
    mw.title(texts["title"])
    label_var.set(texts["instruction"])
    browse_button.config(text=texts["browse"])
    start_button.config(text=texts["start"])
    lang_button.config(text=texts["toggle"])


fp = tk.Frame(mw)
fp.pack(pady=6)

ep = tk.Entry(fp, width=32)
ep.pack(side=tk.LEFT, padx=6)


def bf():
    sf = filedialog.askdirectory()
    if sf:
        ep.delete(0, tk.END)
        ep.insert(0, sf)


def ss():
    sf = ep.get()
    if not sf:
        messagebox.showerror(TRANSLATIONS[current_lang]["error_title"], TRANSLATIONS[current_lang]["folder_required"])
        return
    if not os.path.exists(sf):
        messagebox.showerror(TRANSLATIONS[current_lang]["error_title"], TRANSLATIONS[current_lang]["folder_missing"])
        return

    sort_img(sf, current_lang)


browse_button = ttk.Button(fp, text=TRANSLATIONS[current_lang]["browse"], command=bf)
browse_button.pack(side=tk.LEFT)
lang_button = ttk.Button(mw, text=TRANSLATIONS[current_lang]["toggle"], width=4, command=toggle_language)
lang_button.pack(pady=(0, 6))
start_button = ttk.Button(mw, text=TRANSLATIONS[current_lang]["start"], command=ss)
start_button.pack(pady=0)

mw.mainloop()