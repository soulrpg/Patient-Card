import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os
from main import Patient, PatientsData, Plot
import copy
from tkcalendar import Calendar, DateEntry
import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure


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
        
        self.table_name = ttk.Label(self.container, text="Surname search")
        self.table_name.pack(side=tk.TOP, pady=(20, 0))
        
        #self.surname_filter_label = ttk.Label(self.container, text="Filtr nazwiska:")
        #self.surname_filter_label.pack(side=tk.TOP)
        
        vcmd = (self.window.register(self.filter_applied),
                '%P')
        self.surname_filter_entry_text = tk.StringVar()
        self.surname_filter_entry_text.set('')

        self.surname_filter_entry = ttk.Entry(self.container, validate="key", validatecommand=vcmd, width = 30, textvariable=self.surname_filter_entry_text)
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
        self.tree_view.column("ID", anchor=tk.W, width=280)
        
        # Nazwy kolumn
        self.tree_view.heading("Imie", text="Name", anchor=tk.CENTER)
        self.tree_view.heading("Nazwisko", text="Surname", anchor=tk.CENTER)
        self.tree_view.heading("Data urodzenia", text="Birth date", anchor=tk.CENTER)
        self.tree_view.heading("ID", text="Identifier", anchor=tk.CENTER)
        
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
        self.form.geometry("1000x700")
        
        self.local_patient = patient
        
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

        self.identifier_text_value = tk.StringVar()
        self.identifier_text_value.set(patient.identifier)

        
        # Glowna ramka
        self.form_container = ttk.Frame(self.form)
        self.form_container.pack(fill=tk.BOTH, expand=True)
        
        self.card_title = ttk.Label(self.form_container, text="Patient data")
        self.card_title.grid(row=0, column=3, sticky=tk.W, pady=(20, 0), padx=5)
        
        #self.names_label = ttk.Label(self.form_container, text="Name:")
        #self.names_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)

        self.margin_label = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.margin_label2 = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label2.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)

        self.name_text_label = ttk.Label(self.form_container, textvariable=self.name_text_value, background="#fefefe")
        self.name_text_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.surname_text_label = ttk.Label(self.form_container, textvariable=self.surname_text_value, background="#fefefe")
        self.surname_text_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        
        self.gender_label = ttk.Label(self.form_container, text="Gender:")
        self.gender_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.gender_text_label = ttk.Label(self.form_container, textvariable=self.gender_text_value, background="#fefefe")
        self.gender_text_label.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)

        self.id_label = ttk.Label(self.form_container, text="Identifier:" )
        self.id_label.grid( row=1, column=3, sticky=tk.W, pady=5, padx=5)
        self.id_text_label = ttk.Label(self.form_container, textvariable=self.identifier_text_value, background="#fefefe")
        self.id_text_label.grid(row=1, column=4, sticky=tk.W, pady=5, padx=5)

        self.edit_surname_button = tk.Button(self.form_container, command=self.show_edit_surname_window, text="Edit surname",bg="#8899dd")
        self.edit_surname_button.grid(row=1, column=5, sticky=tk.W, pady=5, padx=5)

        self.born_label = ttk.Label(self.form_container, text="Born:")
        self.born_label.grid(row=2, column=3, sticky=tk.W, pady=5, padx=5)
        self.born_text_label = ttk.Label(self.form_container, textvariable=self.born_text_value, background="#fefefe")
        self.born_text_label.grid(row=2, column=4, sticky=tk.W, pady=5, padx=5, columnspan=2)



        # self.born_label = ttk.Label(self.form_container, text="Born:")
        # self.born_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        # self.born_text_label = ttk.Label(self.form_container, textvariable=self.born_text_value)
        # self.born_text_label.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)
        #
        # self.id_label = ttk.Label(self.form_container, text="ID:")
        # self.id_label.grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)
        # self.id_text_label = ttk.Label(self.form_container, textvariable=self.id_text_value)
        # self.id_text_label.grid(row=2, column=3, sticky=tk.W, pady=5, padx=5, columnspan=2)

        self.margin_label3 = ttk.Label(self.form_container, textvariable='        ')
        self.margin_label3.grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)


        self.start_date_label = ttk.Label(self.form_container, text="Start date:")
        self.start_date_label.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.start_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=4, column=2, sticky=tk.W, pady=5, padx=5)
        
        begin_date = datetime.datetime(1980, 1, 1)
        end_date = datetime.datetime.now()
        
        self.end_date_label = ttk.Label(self.form_container, text="End date:")
        self.end_date_label.grid(row=4, column=3, sticky=tk.W, pady=5, padx=5)
        
        self.end_date_entry = DateEntry(self.form_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=4, column=4, sticky=tk.W, pady=5, padx=5)
        
        self.end_date_entry.set_date(end_date)
        self.start_date_entry.set_date(begin_date)
        
        self.history_filter_button = tk.Button(self.form_container, command=self.filter_history, text="Filter history", bg="yellow")
        self.history_filter_button.grid(row=4, column=5, sticky=tk.W, pady=5, padx=5)
        
        #self.drop_down_list = ttk.Combobox(self.form_container, values=patient.observations_value_names)
        #self.drop_down_list.grid(row=4, column=4, sticky=tk.W, pady=5, padx=5)

        style = ttk.Style()

        style.configure('myStyle1.Treeview', rowheight=48)

        self.history_tree = ttk.Treeview(self.form_container,style='myStyle1.Treeview')


        #Definicja kolumn
        self.history_tree['columns'] = ("Date", "Type", "Info")
        
        # Defaultowa kolumna - nie potrzebujemy jej
        self.history_tree.column("#0", anchor=tk.W, width=80)

        self.med_img = tk.PhotoImage(file='med.png')
        self.obs_img = tk.PhotoImage(file='obs.png')

        self.history_tree.column("Date", anchor=tk.W, width=100)
        self.history_tree.column("Type", anchor=tk.W, width = 80)
        self.history_tree.column("Info", anchor=tk.W, width=600)

        self.history_tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.history_tree.heading("Type", text="Type", anchor=tk.CENTER)
        self.history_tree.heading("Info", text="Info", anchor=tk.CENTER)
        
        self.history_tree.insert(parent='', index='end', iid=patient.id, text="")
        
        self.history_tree.grid(row=5, column=1, rowspan=3, columnspan=7, sticky=tk.W, pady=5, padx=5)
        
        self.plot_button = tk.Button(self.form_container, command=lambda arg=self.local_patient: self.show_plot_window(), text="Show plot", bg="yellow")
        self.plot_button.grid(row=6, column=8, sticky=tk.W, pady=5, padx=5)
        

        for i,event in enumerate(self.local_patient.get_history_in_range(str(self.start_date_entry.get_date()),str( self.end_date_entry.get_date()))):
           self.insert_history(event,i)

        self.history_tree.tag_configure('odd', background='lightblue')
        self.history_tree.tag_configure('even', background='lightgrey')



        self.form.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def insert_history(self, event, i):
        # index='end' oznacza ze dodajemy na koniec tabeli
        if event["type"] != 'medication':
           event_type = 'Observation'
           info = event['name']
           img = self.obs_img
           if event['type']=='value':
               info +=  '\n'+str(event['value'])+' '+event['unit']
           elif event['type'] == 'values':
               info += '\n'+ event['specific_name'][0] +': ' +str(event['value'][0]) + ' ' + event['unit'][0] + '\n'
               info += event['specific_name'][1] +': ' +str(event['value'][1]) + ' ' + event['unit'][1]
        else:
           event_type = 'Medication'
           info = event['name']
           img = self.med_img

        if i%2==1:
            self.history_tree.insert(parent='', index='end', iid=event["id"], text="", image =img ,values=(event["date"][:16].replace('T','  '), event_type, info), tags=('odd',))
        else:
            self.history_tree.insert(parent='', index='end', iid=event["id"], text="",image=img, values=(event["date"][:16].replace('T','  '), event_type, info), tags=('even',))

    def clear_history_tree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
    def on_closing(self):
        self.block_new_info_window = False
        self.form.destroy()
        
    # Okno do wyswietlania wykresu
    def show_plot_window(self):
        self.edit_surname_button["state"] = "disabled"
        self.plot_button["state"] = "disabled"
        self.history_filter_button["state"] = "disabled"
        self.plot_window = tk.Toplevel(self.form)
        self.plot_window.title("Wykres")
        self.plot_window.geometry("800x500")
        
        self.radio_button_chosen = tk.IntVar()
        
        
        self.plot_container = ttk.Frame(self.plot_window)
        self.plot_container.pack(fill=tk.BOTH, expand=True)
        
        self.list_label = tk.Label(self.plot_container, text="Choose value:")
        self.list_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.drop_down_list = ttk.Combobox(self.plot_container, 
                            values=self.local_patient.observations_values_names)
        self.drop_down_list.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.drop_down_list.current(0)
        
        #self.drop_down_list.bind("<<ComboboxSelected>>", self.update_plot_canvas)
        
        self.start_date_label_2 = tk.Label(self.plot_container, text="Choose start date:")
        self.start_date_label_2.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        
        self.start_date_entry_2 = DateEntry(self.plot_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry_2.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
        
        self.update_plot_button = tk.Button(self.plot_container, command=self.update_plot_canvas, text="Make plot", bg="yellow")
        self.update_plot_button.grid(row=0, column=4, sticky=tk.W, pady=5, padx=5)
        
        begin_date = datetime.datetime(1980, 1, 1)
        
        self.start_date_entry_2.set_date(begin_date)
        
        # Rysowanie wykresu
        self.plot = Plot()
        self.plot.create_plot(self.local_patient,self.drop_down_list.get(), str(self.start_date_entry_2.get_date()),40000)
        self.canvas = FigureCanvasTkAgg(self.plot.fig, self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=7, columnspan=5)
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
        #self.toolbar.update()
        self.canvas._tkcanvas.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=7, columnspan=5)
        
        self.radio_label = tk.Label(self.plot_container, text="Duration:")
        self.radio_label.grid(row=0, column=5, sticky=tk.W, pady=0, padx=5)
        
        self.radio_button_1 = tk.Radiobutton(self.plot_container, text="2 days", variable=self.radio_button_chosen, value=1)
        self.radio_button_1.grid(row=1, column=5, sticky=tk.W, pady=0, padx=5)
        
        self.radio_button_2 = tk.Radiobutton(self.plot_container, text="week", variable=self.radio_button_chosen, value=2)
        self.radio_button_2.grid(row=2, column=5, sticky=tk.W, pady=0, padx=5)
        
        self.radio_button_3 = tk.Radiobutton(self.plot_container, text="month", variable=self.radio_button_chosen, value=3)
        self.radio_button_3.grid(row=3, column=5, sticky=tk.W, pady=0, padx=5)
        
        self.radio_button_4 = tk.Radiobutton(self.plot_container, text="year", variable=self.radio_button_chosen, value=4)
        self.radio_button_4.grid(row=4, column=5, sticky=tk.W, pady=0, padx=5)
        
        self.radio_button_5 = tk.Radiobutton(self.plot_container, text="all", variable=self.radio_button_chosen, value=5)
        self.radio_button_5.grid(row=5, column=5, sticky=tk.W, pady=0, padx=5)
        # Default option - all
        self.radio_button_5.select()
        
        self.plot_window.protocol("WM_DELETE_WINDOW", self.on_closing_plot)
        
    def on_closing_plot(self):
        self.edit_surname_button["state"] = "normal"
        self.plot_button["state"] = "normal"
        self.history_filter_button["state"] = "normal"
        self.plot_window.destroy()
        
    def filter_history(self):
        print("FILTER HISTORY")
        self.clear_history_tree()
        for i,event in enumerate(self.local_patient.get_history_in_range(str(self.start_date_entry.get_date()),str( self.end_date_entry.get_date()))):
           self.insert_history(event,i)
        
        
    def update_plot_canvas(self):
        print("Combobox updated!")
        duration = 0
        val = self.radio_button_chosen.get()
        if val == 1:
            duration = 2
        elif val == 2:
            duration = 7
        elif val == 3:
            duration = 31
        elif val == 4:
            duration = 365
        elif val == 5:
            duration = 40000
        
        
        self.plot.create_plot(self.local_patient, self.drop_down_list.get(), str(self.start_date_entry_2.get_date()), duration) 
        
        self.plot_container.update()
        
        self.canvas.draw()
        
        #self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) # XD
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=5, columnspan=5)

        
        #self.toolbar.update()

        
        #self.plot_window.update_idletasks()
        #self.plot_window.update()
        #self.canvas.draw_idle()
        #self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5, rowspan=5, columnspan=5)

        
    def show_edit_surname_window(self):
        self.edit_surname_button["state"] = "disabled"
        self.plot_button["state"] = "disabled"
        self.history_filter_button["state"] = "disabled"

        self.edit_surname_window = tk.Toplevel(self.form)
        self.edit_surname_window.title("Edit surname")
        self.edit_surname_window.geometry("300x100")


        self.edit_surname_container = ttk.Frame(self.edit_surname_window)
        self.edit_surname_container.pack(fill=tk.BOTH, expand=True)

        self.new_surname_label = tk.Label(self.edit_surname_container, text="New surname:")
        self.new_surname_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)

        self.surname_edit_entry = ttk.Entry(self.edit_surname_container, validate="key", width=30)
        self.surname_edit_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        self.save_surname_button = tk.Button(self.edit_surname_container, command=self.on_save_surname, text="Save",bg="yellow")
        self.save_surname_button.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        self.edit_surname_window.protocol("WM_DELETE_WINDOW", self.on_close_edit_surname)


    def on_close_edit_surname(self):
        self.edit_surname_button["state"] = "normal"
        self.plot_button["state"] = "normal"
        self.history_filter_button["state"] = "normal"
        self.edit_surname_window.destroy()

    def on_save_surname(self):
        new_surname = self.surname_edit_entry.get()
        print(new_surname)

        self.local_patient.set_surname(new_surname)
        self.surname_text_value.set(new_surname)

        self.patients_data.update_patient_surname(new_surname,self.local_patient.id)
        self.filter_applied('')
        self.surname_filter_entry_text.set('')

        self.on_close_edit_surname()
        

        
        
        
        