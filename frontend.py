'''
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


from PIL import Image, ImageTk
import tkinter as tk


class FaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x300")
        self.title("Fader App")

        self.value = tk.IntVar()
        self.value.set(0)

        self.canvas = tk.Canvas(self, width=50, height=250, bg="white")
        self.canvas.pack()

        # Cargar imágenes del fader y la perilla
        fader_image = Image.open("img/fader_image.png")
        knob_image = Image.open("img/knob_image.png")

        # Escalar las imágenes para que se ajusten al tamaño del canvas
        fader_image = fader_image.resize((50, 250))
        knob_image = knob_image.resize((30, 30))

        self.fader = self.canvas.create_image(25, 125, image=self._pil_to_imageTk(fader_image))
        self.knob = self.canvas.create_image(25, 225, image=self._pil_to_imageTk(knob_image))

        self.canvas.bind("<B1-Motion>", self.move_knob)
        self.canvas.bind("<Button-1>", self.move_knob)
        
        self.label = tk.Label(self, textvariable=self.value)
        self.label.pack()

    def move_knob(self, event):
        y = event.y
        if y < 25:
            y = 25
        elif y > 225:
            y = 225
        self.canvas.coords(self.knob, 25, y)
        self.value.set(int(100 - (y-25) * 100 / 200))

    def _pil_to_imageTk(self, image):
        return ImageTk.PhotoImage(image)

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()
''' 
import tkinter as tk

class FaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x300")
        self.title("Fader App")

        self.value = tk.IntVar(value=100)
        self.value.set(0)

        self.canvas = tk.Canvas(self, width=50, height=250, bg="white")
        self.canvas.pack()

        self.fader = self.canvas.create_rectangle(20, 20, 30, 230, fill="black")
        self.knob = self.canvas.create_oval(10, 225, 40, 255, fill="red")

        self.canvas.bind("<B1-Motion>", self.move_knob)
        self.canvas.bind("<Button-1>", self.move_knob)
        
        self.label = tk.Label(self, textvariable=self.value)
        self.label.pack()

    def move_knob(self, event):
        y = event.y
        if y < 25:
            y = 25
        elif y > 225:
            y = 225
        self.canvas.coords(self.knob, 10, y-5, 40, y+5)
        self.value.set(int(100 - (y-25) * 100 / 200))

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()
