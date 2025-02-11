#TODO:
#Crear un sistema para guardar los numeros de telefono y nombre de los pacientes.
#Interfaz para poder agregar, eliminar pacientes. Conexion con Google SpreadSheet u otro sistema de almacenamiento.
#Crear un sistema de notificaciones para recordar los turnos de los pacientes automaticamente.
#Mejorar interfaz con CustomTkinter.

import tkinter as tk
import traceback
import sys
import os.path
import configparser
import customtkinter as ctk
from tkinter import messagebox, Listbox, Scrollbar, PhotoImage
from PIL import ImageTk, Image
from datetime import datetime, timezone
from util import access_calendar, access_sheet
from pacient import create_pacient, edit_pacient, delete_pacient, btn_pacient_click, index_selected
#from turn import 
from functools import partial


#-------------------Window Preparation/Events-------------------#

#Centrar y redimensionar la ventana.
def center_and_resize_window(window):

    if window.title() == "PyTurn":
        width_ratio = 0.2
        height_ratio = 0.2
    elif window.title() == "PyTurn - Turnos":
        width_ratio = 0.2
        height_ratio = 0.2
    elif window.title() == "PyTurn - Pacientes":
        width_ratio = 0.2
        height_ratio = 0.251
    elif window.title() == "PyTurn - Configuración":
        width_ratio = 0.3
        height_ratio = 0.124

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    #screen_width = 1920
    #screen_height = 1080

    # Calcular tamaño de la ventana en base a la resolución de la pantalla
    width = int(screen_width * width_ratio)
    height = int(screen_height * height_ratio)

    # Calcular posición para centrar la ventana
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    # Aplicar tamaño y posición
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")

def prepare_interface(window_type):

    if window_type == "main":
        window = ctk.CTk()
    else:
        window = ctk.CTkToplevel()

    if window_type == "turn":
        window.title("PyTurn - Turnos")
    elif window_type == "pacient":
        window.title("PyTurn - Pacientes")
    elif window_type == "config":
        window.title("PyTurn - Configuración")
    else:
        window.title("PyTurn")

    center_and_resize_window(window)
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", disable_event)
    #window.report_callback_exception = show_error

    return window

def return_to_menu(current_window):
    current_window.destroy()
    main_window.deiconify()

def disable_event():
    if main_window.state() == "normal":
        main_window.destroy()

def show_error(*args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)
    sys.exit()

#----------------------------------------------------#


#-------------------Window Creation-------------------#

#Crear interfaz para los turnos.
def create_turn_window():
    main_window.withdraw()
    window = prepare_interface("turn")

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window))
    back_button.pack(pady=5)

    window.mainloop()
    
#Crear interfaz para los pacientes.
def create_pacient_window():
    main_window.withdraw()
    window = prepare_interface("pacient")
    window.columnconfigure(0, weight=1)
    
    try:
        pacients = access_sheet()
        array_pacients = []
        for pacient in pacients[1:]:
            array_pacients.append(pacient)

    except Exception as error:
        if error.__class__.__name__ == "RefreshError":
            os.remove("token.json")
            access_sheet()
        else:
            messagebox.showerror("Error", f"No se pudo acceder a la hoja de calculo.\n{error}")

    frame = ctk.CTkScrollableFrame(window)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

    frame2 = ctk.CTkFrame(window)
    frame2.grid(row=0, column=1, pady=10, padx=10, sticky="nw")
    frame2.configure(fg_color="transparent")

    label_info= ctk.CTkLabel(window, text="")
    label_info.grid(row=0, column=1, pady=10, padx=10, sticky="sw")
    label_info.configure(justify="left")

    create_button = ctk.CTkButton(frame2, text="Añadir", command=lambda: create_pacient(window, 0, ""))
    create_button.grid(row=0, column=1, pady=5, padx=5)

    edit_button = ctk.CTkButton(frame2, text="Editar", state="disabled", command=lambda: edit_pacient(window))
    edit_button.grid(row=1, column=1, pady=5, padx=5)

    delete_button = ctk.CTkButton(frame2, text="Eliminar", state="disabled", command=lambda: delete_pacient(pacients))
    delete_button.grid(row=2, column=1, pady=5, padx=5)

    for pacient in pacients[1:]:
        btn_pacient = ctk.CTkButton(frame, text=str(pacient[0]), fg_color="transparent")
        btn_pacient.grid(row=pacients.index(pacient), column=0, padx=5, sticky="w")
        btn_pacient.configure(command=lambda btn=btn_pacient, pacient=pacient: btn_pacient_click(btn, frame, frame2, label_info, pacient, pacients))

    #save_image = Image.open("src/pyturn/assets/save.png")
    #save_image2 = ctk.CTkImage(save_image)
    #save_button = ctk.CTkButton(window, text="Guardar", image=save_image2, command=lambda: save_pacients(window))
    #save_button.grid(row=1, column=1, padx=10, sticky="e")

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window))
    back_button.grid(row=1, column=0, padx=10, sticky="w")

    window.mainloop()

def create_config_window():
    main_window.withdraw()
    window = prepare_interface("config")
    config = configparser.ConfigParser()
    config.read('.config')
    window.columnconfigure(0, weight=1)

    screen_width = window.winfo_screenwidth()
    width_ratio = 0.3

    frame = ctk.CTkFrame(window)
    frame.grid(row=0, column=0, pady=10, padx=10)

    label_excel_url = ctk.CTkLabel(frame, text="Excel URL:")
    label_excel_url.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_excel_url = ctk.CTkEntry(frame)
    entry_excel_url.insert(0, config.get("CONFIG", "GOOGLE_SHEET_URL"))
    entry_excel_url.grid(row=0, column=1, padx=10, pady=5, ipadx=(screen_width-width_ratio)/15, sticky="w")

    label_whatsapp_number = ctk.CTkLabel(frame, text="Número de WhatsApp:")
    label_whatsapp_number.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_whatsapp_number = ctk.CTkEntry(frame)
    entry_whatsapp_number.insert(0, config.get("CONFIG", "WHATSAPP_NUMBER"))
    entry_whatsapp_number.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    save_image = Image.open("src/pyturn/assets/save.png")
    save_image2 = ctk.CTkImage(save_image)
    save_button = ctk.CTkButton(window, text="Guardar", image=save_image2, command=lambda: save_config(entry_excel_url, entry_whatsapp_number, window))
    save_button.grid(row=1, column=0, padx=10, sticky="e")

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window))
    back_button.grid(row=1, column=0, padx=10, sticky="w")

    window.mainloop()

#----------------------------------------------------#


#-------------------Functions-------------------#

#Edit the .config file to save the configuration.
def save_config(entry_excel_url, entry_whatsapp_number, window):
    config = configparser.ConfigParser()
    config.read('.config')
    config.set("CONFIG", "GOOGLE_SHEET_URL", entry_excel_url.get())
    config.set("CONFIG", "GOOGLE_SHEET_ID", entry_excel_url.get().split("/")[5])
    config.set("CONFIG", "WHATSAPP_NUMBER", entry_whatsapp_number.get())
    with open('.config', 'w') as configfile:
        config.write(configfile)

    return_to_menu(window)

def save_pacients():
    pass

#Enviar recordatorio a los pacientes con un margen de 48 horas.
def send_reminders():
    pass

#----------------------------------------------------#


#-------------------Main-------------------#

#Crear interfaz para las opciones de la aplicacion.
def create_main_window():
    global main_window
    main_window = prepare_interface("main")

    try:
        access_calendar()
    except Exception as error:
        if error.__class__.__name__ == "RefreshError":
            os.remove("token.json")
            access_calendar()
        else:
            messagebox.showerror("Error", f"No se pudo acceder al calendario.\n{error}")
            main_window.destroy()

    frame = ctk.CTkFrame(main_window)
    frame.pack(expand=True)

    config_image = Image.open("src/pyturn/assets/config.png")
    config_image2 = ctk.CTkImage(config_image)
    config_button = ctk.CTkButton(main_window, text="Configuración", command=create_config_window, image=config_image2)
    config_button.pack(pady=10, padx=10, anchor="e")

    label = ctk.CTkLabel(frame, text="PyTurn")
    label.pack(pady=5)

    turn_interface = ctk.CTkButton(frame, text="Turnos", command=create_turn_window)
    turn_interface.pack(pady=5, padx=10)

    pacient_interface = ctk.CTkButton(frame, text="Pacientes", command=create_pacient_window)
    pacient_interface.pack(pady=10, padx=10)

    main_window.mainloop()


create_main_window()

#----------------------------------------------------#