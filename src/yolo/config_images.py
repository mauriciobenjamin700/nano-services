# redimensionar_imagem.py
from glob import glob
from os import mkdir
from os.path import (
    basename, 
    exists,
    join, 
    splitext

)

from PIL import Image


ROTATES = [45,90,135,180,225, 270,315,360]


def get_image_paths(folder: str) -> list[str]:
    # Obter caminhos das imagens no diretório
    return glob(f"{folder}/*")

def get_image(image_path: str) -> Image.Image:
    return Image.open(image_path)

def resize_image_to_yolo(image: Image.Image) -> Image.Image:
    return image.resize((640, 640))

# Salvar a imagem redimensionada
#imagem_redimensionada.save(caminho_saida)

def rotate_image(image: Image.Image, rotates: list[int] = ROTATES) -> list[Image.Image]:
    # Abrir a imagem
    # Definir os ângulos de rotação    # Gerar e salvar as variantes rotacionadas

    result = []

    if not rotates:
        rotates = ROTATES


    for rotate in rotates:
        rotate_image = image.rotate(rotate)
        result.append(rotate_image)

    return result



def save_image(image: Image.Image, output_folder: str, filename: str, label: str = ""):
    # Salvar a imagem redimensionada
    if len(label) > 0:
        name, _ = splitext(basename(filename))
        filename = f"{name}_{label}.jpg"
    if not exists(output_folder):
        mkdir(output_folder)
    image.save(join(output_folder, basename(filename)))

def generate_image_dataset(folder: str, output: str, rotates: list[int] = ROTATES):
    
    image_paths = get_image_paths(folder)

    for image_path in image_paths:
        image = get_image(image_path)
        resized_image = resize_image_to_yolo(image)
        rotated_images = rotate_image(resized_image)
        for idx in range(len(rotated_images)):
            # Salvar a imagem rotacionada
            save_image(rotated_images[idx], output, image_path, str(rotates[idx]))

