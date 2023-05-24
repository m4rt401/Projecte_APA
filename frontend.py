import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class FaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Fader App")
        self.value = tk.IntVar(value=100)
        self.value.set(0)

        # Cargar la imagen de fondo
        self.image = ImageTk.PhotoImage(file="DOWNSAMPLING.png")

        # Crear un widget Label y establecer la imagen de fondo
        background_label = tk.Label(self, image=self.image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=10, height=230, bg="black", highlightthickness=0)
        self.canvas.place(x=127.5, y=142)  # Posición deseada del fader

        self.fader = self.canvas.create_rectangle(0, 0, 20, 230, fill="white")
        self.knob = self.canvas.create_oval(-5, -5, 15, 15, fill="red")

        self.canvas.bind("<B1-Motion>", self.move_knob)
        self.canvas.bind("<Button-1>", self.move_knob)

        self.label = tk.Label(self, textvariable=self.value)
        self.label.place(x=240, y=400)  # Posición deseada de la etiqueta

    def move_knob(self, event):
        y = event.y
        if y < 25:
            y = 25
        elif y > 225:
            y = 225
        self.canvas.coords(self.fader, 0, 0, 20, 230)  # Ajustar coordenadas del rectángulo
        self.canvas.coords(self.knob, -5, y-5, 15, y+5)
        self.value.set(int(100 - (y-25) * 100 / 200))

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()
