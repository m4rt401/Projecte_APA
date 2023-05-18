import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    selected_file_label.config(text="Archivo seleccionado: " + file_path)
    # Realizar el procesamiento adicional aquí

root = tk.Tk()
root.title("Front-end")

def create_widgets():
    browse_button = tk.Button(root, text="Browse", command=open_file_dialog)
    browse_button.pack(pady=10)

    global selected_file_label
    selected_file_label = tk.Label(root, text="Archivo seleccionado: ")
    selected_file_label.pack()

create_widgets()

root.mainloop()
