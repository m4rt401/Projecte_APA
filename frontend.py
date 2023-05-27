import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sounddevice as sd
import backend as bk

class FaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Fader App")
        self.value = tk.IntVar(value=0)

        # Cargar la imagen de fondo
        self.image = ImageTk.PhotoImage(file="DOWNSAMPLING.png")

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
        self.selected_file_label.place(x=20, y=430)  # Posición deseada de la etiqueta de ruta seleccionada

        self.browse_button = tk.Button(self, text="Browse", command=self.open_file_dialog)
        self.browse_button.place(x=450, y=470)  # Posición deseada del botón de navegación

        self.play_button = tk.Button(self, text="Play", command=self.play_pause_file)
        self.play_button.place(x=400, y=470)  # Posición deseada del botón de reproducción
        self.is_playing = False

        self.download_button = tk.Button(self, text="Download", command=self.download_file)
        self.download_button.place(x=325, y=470) # Posición deseada del botón de descarga

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
        '''
        Función que nos permite buscar un fichero de audio por nuestro ordenador para poderlo usar más adelante.
        '''
        file_path = filedialog.askopenfilename()
        self.org_data, self.samplerate, self.info = bk.lectura_audio(file_path)

        if file_path:
            self.selected_file_label.config(text="Archivo seleccionado: " + file_path)

    def play_pause_file(self):
        '''
        Función que regula el boton de play/pause. 
        Cada vez que se da al play se consigue el valor en el que esta el fader(porcentaje de calidad) para poder reproducir la señal downsampleada.
        En el momento en el que se da Play, este mismo botón cambia a ser un botón de Pause y se se apreta lo que hace es parar de reproducir y prepararse para volver a reproducir el audio.
        '''
        if self.is_playing == False:
            fader=self.value.get()
            self.data_DWS, self.samplerate, self.info = bk.downsampler(self.org_data, self.samplerate, self.info, fader)
            
            sd.play(self.data_DWS, self.samplerate)
            self.is_playing = True
            self.play_button.config(text="Pause")
        else:
            
            sd.stop()
            self.is_playing = False
            self.play_button.config(text="Play")

    def download_file(self):
        '''
        Función que, de manera independiente a la posición del fader con la que se haya dado a reproducir, agarra el valor de fader en el que esté
        colocado y escribe un fichero wave con ese porcentaje de calidad. Para ello se usa la función "escritura_wave" definida en back end que
        agarra los datos y los codifica en formato wave. Este fichero nuevo tiene como salida la misma carpeta del proyecto.
        '''
        self.data_DWS, self.samplerate, self.info = bk.downsampler(self.org_data, self.samplerate, self.info,self.value.get())
        bk.escritura_wave(self.data_DWS, self.samplerate, self.info)

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()