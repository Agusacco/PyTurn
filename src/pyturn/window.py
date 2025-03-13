import customtkinter as ctk
import configparser
import os
import traceback
import sys
from PIL import Image
from pacient import create_pacient, edit_pacient, delete_pacient, btn_pacient_click
from config import save_config
from util import access_sheet
from tkinter import messagebox

def create_turn_window(main_window):
    main_window.withdraw()
    window = prepare_interface("turn")

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window, main_window))
    back_button.pack(pady=5)

    window.mainloop()

def create_pacient_window(main_window):
    main_window.withdraw()
    window = prepare_interface("pacient")
    window.columnconfigure(0, weight=1)

    try:
        pacients = access_sheet("access_pacients", "A1:B500")
        array_pacients = [pacient for pacient in pacients[1:]]
    except Exception as error:
        if error.__class__.__name__ == "RefreshError":
            os.remove("token.json")
            access_sheet()
        else:
            messagebox.showerror("Error", f"No se pudo acceder a la hoja de cálculo.\n{error}")

    frame = ctk.CTkScrollableFrame(window)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

    frame2 = ctk.CTkFrame(window)
    frame2.grid(row=0, column=1, pady=10, padx=10, sticky="nw")
    frame2.configure(fg_color="transparent")

    label_info = ctk.CTkLabel(window, text="")
    label_info.grid(row=0, column=1, pady=10, padx=10, sticky="sw")
    label_info.configure(justify="left")

    create_button = ctk.CTkButton(frame2, text="Añadir", command=lambda: create_pacient(window, 0, ""))
    create_button.grid(row=0, column=1, pady=5, padx=5)

    edit_button = ctk.CTkButton(frame2, text="Editar", state="disabled", command=lambda: edit_pacient(window))
    edit_button.grid(row=1, column=1, pady=5, padx=5)

    delete_button = ctk.CTkButton(frame2, text="Eliminar", state="disabled", command=lambda: delete_pacient(pacients, window, main_window))
    delete_button.grid(row=2, column=1, pady=5, padx=5)

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window, main_window))
    back_button.grid(row=1, column=0, padx=10, sticky="w")

    for pacient in pacients[1:]:
        btn_pacient = ctk.CTkButton(frame, text=str(pacient[0]), fg_color="transparent")
        btn_pacient.grid(row=pacients.index(pacient), column=0, padx=5, sticky="w")
        btn_pacient.configure(command=lambda btn=btn_pacient, pacient=pacient: btn_pacient_click(btn, frame, frame2, label_info, pacient, pacients))

    window.mainloop()

def create_config_window(main_window):
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

    save_image = Image.open("assets/save.png")
    save_image2 = ctk.CTkImage(save_image)
    save_button = ctk.CTkButton(window, text="Guardar", image=save_image2, command=lambda: save_config(entry_excel_url, entry_whatsapp_number, window, main_window))
    save_button.grid(row=1, column=0, padx=10, sticky="e")

    back_button = ctk.CTkButton(window, text="Volver", command=lambda: return_to_menu(window, main_window))
    back_button.grid(row=1, column=0, padx=10, sticky="w")

    window.mainloop()

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
        window.protocol("WM_DELETE_WINDOW", disable_event)

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
    #window.report_callback_exception = show_error
    return window

def return_to_menu(current_window, main_window):
    current_window.destroy()
    main_window.deiconify()

def show_error(*args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)
    sys.exit()

def disable_event():
    pass