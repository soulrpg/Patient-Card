import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os
from main import Patient, PatientsData, create_plot
import copy
from tkcalendar import Calendar, DateEntry
import datetime


class GUI:
    def __init__(self, title, WIDTH, HEIGHT, RESIZABLE, patients):
        # Tworzenie okna
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.window.resizable(RESIZABLE, RESIZABLE)
        
        self.block_new_info_window = False
        
        # Obiekt przechowujacy informacje o wszystkich pacjentach
        self.patients_data = patients
        
        # Zmienne
        self.filter_text_value = tk.StringVar()
        self.filter_text_value.set("")
                
        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()
        
        self.table_name = ttk.Label(self.container, text="Pacjenci")
        self.table_name.pack(side=tk.TOP, pady=(20, 0))
        
        #self.surname_filter_label = ttk.Label(self.container, text="Filtr nazwiska:")
        #self.surname_filter_label.pack(side=tk.TOP)
        
        vcmd = (self.window.register(self.filter_applied),
                '%P')
        self.surname_filter_entry = ttk.Entry(self.container, validate="key", validatecommand=vcmd, width = 30)
        self.surname_filter_entry.pack(side = tk.TOP, pady=(0, 20))
        
        self.tree_scroll = tk.Scrollbar(self.container)
        self.tree_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree_view = ttk.Treeview(self.container, yscrollcommand=self.tree_scroll.set)
        
        #konfiguracja scrollbara
        self.tree_scroll.config(command=self.tree_view.yview)
        
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
        self.tree_view.heading("Imie", text="Name", anchor=tk.CENTER)
        self.tree_view.heading("Nazwisko", text="Surname", anchor=tk.CENTER)
        self.tree_view.heading("Data urodzenia", text="Birth date", anchor=tk.CENTER)
        self.tree_view.heading("ID", text="ID", anchor=tk.CENTER)
        
        self.tree_view.pack()
        
        #self.insert_to_table({"name": "Robert", "family": "Lewandowski", "b_date": "1000-10-01", "ID": 9})
        #self.insert_to_table({"name": "Yoda", "family": "Master", "b_date": "5000-02-11", "ID": 66})
        for patient in self.patients_data.patients:
            self.insert_to_table(patient)
        
        
        # Listener na klikniecia
        self.tree_view.bind("<Double-1>", self.on_row_clicked)
        
        
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()
        
    def filter_applied(self, input):
        if input == "":
            self.clear_table()
            print("GET ALL PATIENTS")
            for patient in self.patients_data.patients:
                self.insert_to_table(patient)
            return True
        patients_filtered = self.patients_data.get_patients_filtered(input)
        self.clear_table()
        print("GET PATIENTS WITH", input)
        for patient in patients_filtered:
            self.insert_to_table(patient)
        return True
        
    def insert_to_table(self, patient):
        # index='end' oznacza ze dodajemy na koniec tabeli
        self.tree_view.insert(parent='', index='end', iid=patient.id, text="", values=(patient.name, patient.surname, patient.birth_date, patient.identifier))
        
    def clear_table(self):
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        
    def on_row_clicked(self, event):
        if self.block_new_info_window == False:
            item = self.tree_view.selection()[0]
            # Tutaj zamieszczamy informacje o pacjencie + edycja?
            print("Kliknieto: ", self.tree_view.item(item)['values'])
            self.block_new_info_window = True
            self.patient_info_window(self.patients_data.get_patient(self.tree_view.item(item)['values'][-1]))
        
        
    def patient_info_window(self, patient):
        self.form = tk.Toplevel(self.window)
        self.form.title("Dane pacjenta")
        self.form.geometry("600x700")
        
        # Zmienne
        self.name_text_value = tk.StringVar()
        self.name_text_value.set(patient.name)
        
        self.surname_text_value = tk.StringVar()
        self.surname_text_value.set(patient.surname)
        
        self.gender_text_value = tk.StringVar()
        self.gender_text_value.set(patient.gender)
        
        self.born_text_value = tk.StringVar()
        self.born_text_value.set(patient.birth_date)
        
        self.id_text_value = tk.StringVar()
        self.id_text_value.set(patient.id)
        
        # Glowna ramka
        self.form_container = ttk.Frame(self.form)
        self.form_container.pack(fill=tk.BOTH, expand=True)
        
        self.card_title = ttk.Label(self.form_container, text="Dane pacjenta")
        self.card_title.grid(row=0, column=3, sticky=tk.W, pady=(20, 0), padx=5)
        
        #self.names_label = ttk.Label(self.form_container, text="Name:")
        #self.names_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.name_text_label = ttk.Label(self.form_container, textvariable=self.name_text_value)
        self.name_text_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.surname_text_label = ttk.Label(self.form_container, textvariable=self.surname_text_value)
        self.surname_text_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.gender_label = ttk.Label(self.form_container, text="Gender:")
        self.gender_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.gender_text_label = ttk.Label(self.form_container, textvariable=self.gender_text_value)
        self.gender_text_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.born_label = ttk.Label(self.form_container, text="Born:")
        self.born_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        self.born_text_label = ttk.Label(self.form_container, textvariable=self.born_text_value)
        self.born_text_label.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)
        
        self.id_label = ttk.Label(self.form_container, text="ID:")
        self.id_label.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)
        self.id_text_label = ttk.Label(self.form_container, textvariable=self.id_text_value)
        self.id_text_label.grid(row=2, column=3, sticky=tk.W, pady=5, padx=5, columnspan=2)
        
        self.start_date_label = ttk.Label(self.form_container, text="Start date:")
        self.start_date_label.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.start_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        begin_date = datetime.datetime(1900, 1, 1)
        end_date = datetime.datetime.now()
        
        self.end_date_label = ttk.Label(self.form_container, text="End date:")
        self.end_date_label.grid(row=4, column=2, sticky=tk.W, pady=5, padx=5)
        
        self.end_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=4, column=3, sticky=tk.W, pady=5, padx=5)
        
        self.end_date_entry.set_date(end_date)
        self.start_date_entry.set_date(begin_date)
        
        self.history_filter_button = tk.Button(self.form_container, command="self.filter_history", text="Filter history", bg="yellow")
        self.history_filter_button.grid(row=4, column=4, sticky=tk.W, pady=5, padx=5)
        
        #self.drop_down_list = ttk.Combobox(self.form_container, values=patient.observations_value_names)
        #self.drop_down_list.grid(row=4, column=4, sticky=tk.W, pady=5, padx=5)
        
        self.history_tree = ttk.Treeview(self.form_container)
            
        #Definicja kolumn
        self.history_tree['columns'] = ("Date", "Type", "Info")
        
        # Defaultowa kolumna - nie potrzebujemy jej
        self.history_tree.column("#0", width=0)
        
        self.history_tree.column("Date", anchor=tk.W, width=100)
        self.history_tree.column("Type", anchor=tk.W, width = 120) 
        self.history_tree.column("Info", anchor=tk.W, width=200)
        
        
        self.history_tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.history_tree.heading("Type", text="Type", anchor=tk.CENTER)
        self.history_tree.heading("Info", text="Info", anchor=tk.CENTER)
        
        self.history_tree.insert(parent='', index='end', iid=patient.id, text="")
        
        self.history_tree.grid(row=5, column=1, rowspan=3, columnspan=7, sticky=tk.W, pady=5, padx=5)
        
        self.plot_button = tk.Button(self.form_container, command="self.plot_window", text="Show plot", bg="yellow")
        self.history_filter_button.grid(row=6, column=8, sticky=tk.W, pady=5, padx=5)
        
        #for event in patient.get_history_in_range(self.start_date_entry.get_date(), self.end_date_entry.get_date()):
        #    self.insert_history(event["id"], event["date"], event["type"], "INFO")
        
        
        self.form.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def insert_history(self, uid, date, type, info):
        # index='end' oznacza ze dodajemy na koniec tabeli
        self.tree_view.insert(parent='', index='end', iid=history.id, text="", values=(uid, date, type, info))
        
    def clear_history_tree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
    def on_closing(self):
        self.block_new_info_window = False
        self.form.destroy()
        
    def plot_window(self):
        self.plot_window = tk.Toplevel(self.form)
        self.form.title("Wykres")
        self.form.geometry("600x700")
        
        
        
        
        
        
        
        