import tkinter as tk
import customtkinter as ctk

index_selected = None

def btn_pacient_click(btn, frame, frame2, label, pacient, pacients):
    global index_selected 
    for widget in frame.winfo_children():
        widget.configure(state="normal", fg_color="transparent", text_color="white")

    for widget in frame2.winfo_children():
        widget.configure(state="normal")

    btn.configure(state="disabled", fg_color="#3c3c3c", text_color="black")
    label.configure(text=str(pacient[0])+"\nTel. "+str(pacient[1]))
    index_selected = pacients.index(pacient)
    return index_selected


#Crea un nuevo paciente.
def create_pacient(window, flag, input):
    window.attributes("-disabled", True)
    try:
        if flag == 0:
            input_window = ctk.CTkInputDialog(text="Nombre del paciente:", title="Pyturn - Añadir paciente")
            input = input_window.get_input()
            print(input)
            if input is None:
                window.attributes("-disabled", False)
                window.focus_force()
            elif input == "":
                raise Exception("El nombre del paciente no puede estar vacío.")
            else:
                flag = 1
        if flag == 1:
            phone_window = ctk.CTkInputDialog(text="Teléfono del paciente:", title="Pyturn - Añadir paciente")
            phone_input = phone_window.get_input()
            if phone_input is None:
                window.attributes("-disabled", False)
                window.focus_force()
            elif phone_input == "":
                raise Exception("El teléfono del paciente no puede estar vacío.")
            elif phone_input.isnumeric() == False:
                raise Exception("El teléfono del paciente debe contener solo números.")
            else:
                print("Paciente ingresado.\nNombre: "+input+"\nTeléfono: "+phone_input)
                window.attributes("-disabled", False)
                window.focus_force()
                
             
    except Exception as error:
        tk.messagebox.showerror("Error", f"{error.__class__.__name__}\n{error}")
        create_pacient(window, flag, input)

def edit_pacient():
    pass

#Borra un paciente.
def delete_pacient(pacients):
    pacient = pacients[index_selected]
    ask_delete = tk.messagebox.askyesno("askyesno", "Vas a eliminar el paciente "+str(pacient[0])+".\n¿Estás seguro?")
    if ask_delete:
        print("Paciente eliminado.\n"+str(pacient[0]))+"\nTel. "+str(pacient[1])
