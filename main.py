import tkinter as tk
from tkinter import messagebox
import random
import json

# Цитаты
spisok = [
    {"text": "Будь изменением, которое хочешь видеть в мире.", "author": "Ганди", "theme": "мотивация"},
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Леннон", "theme": "жизнь"},
    {"text": "Воображение важнее знаний.", "author": "Эйнштейн", "theme": "мудрость"},
]

# Загрузка
try:
    with open("history.json", "r", encoding="utf-8") as f:
        istoriya = json.load(f)
except:
    istoriya = []

def gen():
    c = random.choice(spisok)
    quote_label.config(text=f'"{c["text"]}"')
    author_label.config(text=f"— {c['author']} ({c['theme']})")
    
    istoriya.append(c)
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(istoriya, f, ensure_ascii=False, indent=4)
    
    obnovit_listbox()

def dobavit():
    t = entry_text.get().strip()
    a = entry_author.get().strip()
    tm = entry_theme.get().strip()
    
    if t == "" or a == "" or tm == "":
        messagebox.showerror("Ошибка", "Заполните всё!")
        return
    
    spisok.append({"text": t, "author": a, "theme": tm})
    messagebox.showinfo("Успех", "Добавлено!")
    
    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_theme.delete(0, tk.END)

def filtr():
    a = filter_a.get().strip().lower()
    t = filter_t.get().strip().lower()
    
    rez = []
    for h in istoriya:
        if a and a not in h["author"].lower():
            continue
        if t and t not in h["theme"].lower():
            continue
        rez.append(h)
    
    obnovit_listbox(rez)

def sbros():
    filter_a.delete(0, tk.END)
    filter_t.delete(0, tk.END)
    obnovit_listbox()

def obnovit_listbox(spisok_hist=None):
    listbox.delete(0, tk.END)
    
    if spisok_hist is None:
        spisok_hist = istoriya
    
    if not spisok_hist:
        listbox.insert(tk.END, "История пуста")
        return
    
    for i, h in enumerate(spisok_hist, 1):
        listbox.insert(tk.END, f"{i}. {h['text'][:35]} — {h['author']}")

def ochistit():
    if messagebox.askyesno("Очистка", "Точно?"):
        global istoriya
        istoriya = []
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(istoriya, f, ensure_ascii=False, indent=4)
        obnovit_listbox()

# Окно
okno = tk.Tk()
okno.title("Генератор цитат")
okno.geometry("500x600")

tk.Label(okno, text="ГЕНЕРАТОР ЦИТАТ", font=("Arial", 14, "bold")).pack(pady=10)

quote_label = tk.Label(okno, text="", font=("Arial", 12), wraplength=450)
quote_label.pack(pady=15)

author_label = tk.Label(okno, text="", font=("Arial", 10), fg="gray")
author_label.pack()

tk.Button(okno, text="Сгенерировать", command=gen, bg="green", fg="white").pack(pady=10)

# Добавление
tk.Label(okno, text="--- Добавить цитату ---", font=("Arial", 10, "bold")).pack(pady=5)

tk.Label(okno, text="Текст:").pack()
entry_text = tk.Entry(okno, width=50)
entry_text.pack()

tk.Label(okno, text="Автор:").pack()
entry_author = tk.Entry(okno, width=30)
entry_author.pack()

tk.Label(okno, text="Тема:").pack()
entry_theme = tk.Entry(okno, width=20)
entry_theme.pack()

tk.Button(okno, text="Добавить", command=dobavit, bg="orange").pack(pady=5)

# Фильтры
tk.Label(okno, text="--- Фильтр истории ---", font=("Arial", 10, "bold")).pack(pady=5)

f_row = tk.Frame(okno)
f_row.pack()

tk.Label(f_row, text="Автор:").pack(side="left", padx=5)
filter_a = tk.Entry(f_row, width=15)
filter_a.pack(side="left", padx=5)

tk.Label(f_row, text="Тема:").pack(side="left", padx=5)
filter_t = tk.Entry(f_row, width=15)
filter_t.pack(side="left", padx=5)

tk.Button(f_row, text="Фильтр", command=filtr).pack(side="left", padx=5)
tk.Button(f_row, text="Сброс", command=sbros).pack(side="left", padx=5)

# История
tk.Label(okno, text="--- История ---", font=("Arial", 10, "bold")).pack(pady=5)

listbox = tk.Listbox(okno, width=60, height=8)
listbox.pack(pady=5)

tk.Button(okno, text="Очистить историю", command=ochistit, bg="red", fg="white").pack(pady=5)

obnovit_listbox()

okno.mainloop()