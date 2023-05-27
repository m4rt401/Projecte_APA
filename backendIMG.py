from PIL import Image
import math

def downsample_img(image_path, fader):
    # Abrir la imagen
    image = Image.open(image_path)

    # Obtener la calidad actual de la imagen
    current_quality = image.info.get('quality', 100)

    # Calcular la nueva calidad en función del fader
    new_quality = math.ceil((current_quality * (fader / 100))/10)

    # Guardar la imagen con la nueva calidad
    image.save("reduced_image.jpg", quality=new_quality)
    
    # Cargar la imagen reducida
    downsampled_image = Image.open("reduced_image.jpg")
    
    # Redimensionar la imagen al tamaño original
    downsampled_image = downsampled_image.resize(image.size)
    
    # Guardar y devolver la imagen reducida
    downsampled_image.save("downsampled_image.jpg")
    return "downsampled_image.jpg"


