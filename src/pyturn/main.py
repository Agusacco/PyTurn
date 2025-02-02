#TODO:
#Crear un sistema para guardar los numeros de telefono y nombre de los pacientes.
#Interfaz para poder agregar, eliminar pacientes. Conexion con Google SpreadSheet u otro sistema de almacenamiento.
#Crear un sistema de notificaciones para recordar los turnos de los pacientes automaticamente.

import os.path
import tkinter as tk

from tkinter import messagebox, Listbox, Scrollbar
from datetime import datetime, timezone

from util import format_event_date, access_calendar
from pacient import create_pacient
#from turn import 

# If modifying these scopes, delete the file token.json.

#def show_event_details(event):
#    details = f"Título: {event.get('summary', 'Sin título')}\n" \
#              f"Inicio: {event['start'].get('dateTime', event['start'].get('date'))}\n" \
#              f"Fin: {event['end'].get('dateTime', event['end'].get('date'))}\n" \
#              f"Descripción: {event.get('description', 'Sin descripción')}"
#    messagebox.showinfo("Detalles del evento", details)

def visualize_reminders():
    events = access_calendar()
    if not events:
        messagebox.showinfo("Eventos", "No hay eventos próximos.")
        return
  
    now = datetime.now(timezone.utc)

    # Añadir eventos a la lista
    future_events = []
    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        try:
            start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            
            # Si el evento tiene un datetime sin zona horaria (naive), le asignamos zona horaria UTC
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)
            
            # Solo eventos futuros
            if start > now:
                future_events.append((start, event))
        except ValueError:
            continue  # Ignorar eventos sin hora específica (de todo el día)
      
    future_events.sort(key=lambda x: x[0])

    # Crear una ventana para listar los eventos
    event_window = tk.Toplevel()
    event_window.title("Seleccionar evento")
    event_window.geometry("400x300")

    scrollbar = Scrollbar(event_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    event_listbox = Listbox(event_window, yscrollcommand=scrollbar.set, width=50, height=15)
    event_listbox.pack(pady=20)
    scrollbar.config(command=event_listbox.yview)

    for start, event in future_events:
        formatted_start = format_event_date(event['start'].get('dateTime', event['start'].get('date')))
        event_listbox.insert(tk.END, f"{formatted_start} - {event.get('summary', 'Sin título')}")

  # Función para mostrar detalles del evento seleccionado
  #def on_event_select(event):
  #    selected_index = event_listbox.curselection()
  #    if selected_index:
  #        selected_event = events[selected_index[0]]
  #        show_event_details(selected_event)

  #event_listbox.bind("<Double-1>", on_event_select)


#Enviar recordatorio a los pacientes con un margen de 48 horas.
def send_reminders():
    pass


#Crear interfaz para los turnos.
def create_turn_interface():
    pass


#Crear interfaz para los pacientes.
def create_pacient_interface():
    pass


#Crear interfaz para las opciones de la aplicacion.
def create_login_interface():
    window = tk.Tk()
    window.title("Recordatorios Calendario")
    window.geometry("400x400")
    try:
        access_calendar()
    except Exception as error:
        messagebox.showerror("Error", f"No se pudo acceder al calendario.\n{error}")
        window.destroy()

    turn_interface = tk.Button(window, text="Turnos", command=create_turn_interface)
    turn_interface.pack(pady=5)

    pacient_interface = tk.Button(window, text="Pacientes", command=create_pacient_interface)
    pacient_interface.pack(pady=5)

    window.mainloop()

create_login_interface()