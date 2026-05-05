import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def generate_password():
    length = length_var.get()

    chars = ""
    if var_letters.get():
        chars += string.ascii_letters
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return

    if length < 4 or length > 50:
        messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 50")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    result_var.set(password)

    history.append(password)
    save_history(history)
    update_history()


def update_history():
    listbox.delete(0, tk.END)
    for item in history:
        listbox.insert(tk.END, item)


# GUI
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x500")

length_var = tk.IntVar(value=8)
result_var = tk.StringVar()

var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

history = load_history()

# Длина
tk.Label(root, text="Длина пароля").pack()
tk.Scale(root, from_=4, to=50, orient="horizontal", variable=length_var).pack()

# Чекбоксы
tk.Checkbutton(root, text="Буквы", variable=var_letters).pack()
tk.Checkbutton(root, text="Цифры", variable=var_digits).pack()
tk.Checkbutton(root, text="Спецсимволы", variable=var_symbols).pack()

# Кнопка
tk.Button(root, text="Сгенерировать", command=generate_password).pack(pady=10)

# Результат
tk.Entry(root, textvariable=result_var, width=30).pack()

# История
tk.Label(root, text="История").pack()
listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True)

update_history()

root.mainloop()
