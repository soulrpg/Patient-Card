import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os


class GUI:
    def __init__(self, title, WIDTH, HEIGHT, RESIZABLE):
        # Tworzenie okna
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.window.resizable(RESIZABLE, RESIZABLE)
                
        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()
        
        self.table_name = ttk.Label(self.container, text="Pacjenci")
        self.table_name.pack(side=tk.TOP, pady=(20, 0))
        
        self.surname_filter_label = ttk.Label(self.container, text="Filtr nazwiska:")
        self.surname_filter_label.pack(side=tk.TOP)
        
        self.surname_filter_entry = ttk.Entry(self.container, width = 30)
        self.surname_filter_entry.pack(side = tk.TOP, pady=(0, 20))
        
        self.tree_view = ttk.Treeview(self.container)
        #Definicja kolumn
        self.tree_view['columns'] = ("Imie", "Nazwisko", "Data urodzenia", "ID")
        
        # Defaultowa kolumna - nie potrzebujemy jej
        self.tree_view.column("#0", width=0)
        
        # Format kolumn
        self.tree_view.column("Imie", anchor=tk.W, width=100)
        self.tree_view.column("Nazwisko", anchor=tk.W, width = 120) 
        self.tree_view.column("Data urodzenia", anchor=tk.W, width=120)
        self.tree_view.column("ID", anchor=tk.W, width=120)
        
        # Nazwy kolumn
        self.tree_view.heading("Imie", text="Imię", anchor=tk.CENTER)
        self.tree_view.heading("Nazwisko", text="Nazwisko", anchor=tk.CENTER)
        self.tree_view.heading("Data urodzenia", text="Data urodzenia", anchor=tk.CENTER)
        self.tree_view.heading("ID", text="ID", anchor=tk.CENTER)
        
        self.tree_view.pack()
        
        self.insert_to_table({"name": "Robert", "family": "Lewandowski", "b_date": "1000-10-01", "ID": 9})
        self.insert_to_table({"name": "Yoda", "family": "Master", "b_date": "5000-02-11", "ID": 66})
        # Listener na klikniecia
        self.tree_view.bind("<Double-1>", self.on_row_clicked)
        
        
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()
        
    def insert_to_table(self, row):
        # index='end' oznacza ze dodajemy na koniec tabeli
        self.tree_view.insert(parent='', index='end', iid=row["ID"], text="", values=(row["name"], row["family"], row["b_date"], row["ID"]))
        
    def clear_table(self):
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        
    def on_row_clicked(self, event):
        item = self.tree_view.selection()[0]
        self.form = tk.Toplevel(self.window)
        self.form.title("Dane pacjenta")
        self.form.geometry("600x700")
        # Tutaj zamieszczamy informacje o pacjencie + edycja?
        print("Kliknieto: ", self.tree_view.item(item)['values'])