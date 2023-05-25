import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import soundfile as sf
import sounddevice as sd
import numpy as np
import math
import wave as wv

# back
def lectura_audio(Ficheroaudio):
    '''
    Lee el fichero de audio introducido y retorna los datos, el sample rate y la información de la cabecera del archivo sea del tipo que sea.
    En el caso de que sea un archivo no valido saltará una excepción que nos llevarà a una ventana de alerta.
    '''
    try:
        data, samplerate = sf.read(Ficheroaudio)
        info = sf.info(Ficheroaudio)
        # saca la información de la cabecera con la libreria SF para después 
        # codificar el archivo de salida con la misma información con la que 
        # entra sea cual sea el tipo de archivo de entrada
    except (TypeError, sf.SoundFileError) as e:
        # mensaje de alerta por introducir un fichero incorrecto
        print("Error al leer el archivo:", str(e))
    
    return data,samplerate,info

def downsampler(data, samplerate, info, fader):
    if 100 > fader & fader>0:
        factor_degradacion = (fader/100)
    elif fader == 0:
        factor_degradacion = 1
    else: 
        raise Exception("Valor fuera de valores permitidos") from None 
    
    print(factor_degradacion)
    samplerate_nuevo = int(samplerate*factor_degradacion/2)
    factor_downsampling = math.ceil(samplerate/samplerate_nuevo)
    print(factor_downsampling)
    downsampled_data = np.zeros_like(data)
    downsampled_data[::factor_downsampling] = data[::factor_downsampling]

    temp_file = "temp_audio.wav"
    sf.write(temp_file, downsampled_data, samplerate, subtype=info.subtype, format='WAV')
    data, _ = sf.read(temp_file, dtype='float32')
    sd.play(data)

    return downsampled_data, samplerate, info

def escritura_wave(data, samplerate, info):
    # Crear el objeto SoundFile como un archivo wav con la misma cabecera que info
    out_file = "Downsampled_out.wav"
    sf.write(out_file, data, samplerate, subtype=info.subtype, format='WAV')
    

# front
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

        self.play_button = tk.Button(self, text="Play", command=self.play_pause_file)
        self.play_button.place(x=400, y=470)  # Posición deseada del botón de reproducción

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

    def play_pause_file(self):
        file_path = self.selected_file_label.cget("Projecte_APA/temp_audio.txt")[21:]  # Obtener la ruta del archivo desde el label
        
        if not self.is_playing:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(text="Pause")
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="Play")

if __name__ == "__main__":
    app = FaderApp()
    app.mainloop()