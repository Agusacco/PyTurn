#TODO:
#Crear un sistema de notificaciones para recordar los turnos de los pacientes automaticamente y manualmente.


import tkinter as tk
import os.path
import configparser
import customtkinter as ctk
from tkinter import messagebox, Listbox, Scrollbar, PhotoImage
from PIL import ImageTk, Image
from datetime import datetime, timezone
from util import access_calendar
from window import create_turn_window, create_pacient_window, create_config_window, prepare_interface
from functools import partial

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

    config_image = Image.open("assets/config.png")
    config_image2 = ctk.CTkImage(config_image)
    config_button = ctk.CTkButton(main_window, text="Configuración", image=config_image2, command=lambda: create_config_window(main_window))
    config_button.pack(pady=10, padx=10, anchor="e")

    label = ctk.CTkLabel(frame, text="PyTurn")
    label.pack(pady=5)

    turn_interface = ctk.CTkButton(frame, text="Turnos", command=lambda: create_turn_window(main_window))
    turn_interface.pack(pady=5, padx=10)

    pacient_interface = ctk.CTkButton(frame, text="Pacientes", command=lambda: create_pacient_window(main_window))
    pacient_interface.pack(pady=10, padx=10)

    main_window.mainloop()

create_main_window()