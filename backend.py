import soundfile as sf
import sounddevice as sd
import numpy as np
import math
import wave as wv

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
    '''
    Esta función reduce la calidad del audio introducido como "data" en función a un porcentaje de calidad "fader". 
    El valor máximo de calidad es 100% y el valor mínimo es 1%.  
    '''
    if 101 > fader & fader>0:
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

    return downsampled_data, samplerate, info 

def escritura_wave(data, samplerate, info):
    
    out_file = "Downsampled_out.wav"
    sf.write(out_file, data, samplerate, subtype=info.subtype, format='WAV')
    

    