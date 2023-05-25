import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class FaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Fader App")
        self.value = tk.IntVar(value=0)

        # Cargar la imagen de fondo
        self.image = ImageTk.PhotoImage(file="Projecte_APA/DOWNSAMPLING.png")

        # Crear un widget Label y establecer la imagen de fondo
        background_label = tk.Label(self, image=self.image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=10, height=225, bg="black", highlightthickness=0)
        self.canvas.place(x=120, y=126)  # Posición deseada del fader

        self.fader = self.canvas.create_rectangle(0, 230, 280, 0, fill="white")
        self.knob = self.canvas.create_oval(-5, -5, 15, 15, fill="red")

        self.canvas.bind("<B1-Motion>", self.move_knob)
        self.canvas.bind("<Button-1>", self.move_knob)

        self.label = tk.Label(self, textvariable=self.value)
        self.label.place(x=113, y=354)  # Posición deseada de la etiqueta

        self.selected_file_label = tk.Label(self, text="Archivo seleccionado: ")
        self.selected_file_label.place(x=20, y=470)  # Posición deseada de la etiqueta de ruta seleccionada

        self.browse_button = tk.Button(self, text="Browse", command=self.open_file_dialog)
        self.browse_button.place(x=450, y=470)  # Posición deseada del botón de navegación

    def move_knob(self, event):
        y = event.y
        if y < 25:
            y = 25
        elif y > 225:
            y = 225
        self.canvas.coords(self.fader, 0, y, 300, 230)  # Ajustar coordenadas del rectángulo
        self.canvas.coords(self.knob, -5, y-5, 15, y+5)
        self.value.set(int((y-25) * 100 / 200))

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_label.config(text="Archivo seleccionado: " + file_path)

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()
