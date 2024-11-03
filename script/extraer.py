import os
import cv2
import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops

BASE_DIR = "../dataset_papas"
FORMATOS_VALIDOS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
FACTOR_ESCALA = 0.005999880002399953 # del script/factor_escala.ipynb

COLUMNAS = [
    "Especie", "Area_cm2", "Circularidad", "Relacion_Aspecto",
    "Color_H", "Color_S", "Color_V", "Contraste", "Entropia", 
    "Homogeneidad", "Brillo"
]

def extraer_caracteristicas(imagen_path, especie):
    try:
        if os.path.splitext(imagen_path)[1].lower() not in FORMATOS_VALIDOS:
            return None

        # Carga de imagen
        imagen = cv2.imread(imagen_path)
        if imagen is None:
            print(f"Advertencia: La imagen '{imagen_path}' no se pudo cargar.")
            return None

        # Conversion a escala de grises y espacio HSV
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Segmentacion para encontrar contornos
        _, umbral = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contornos:
            return None

        # Seleccion del contorno mas grande
        contorno = max(contornos, key=cv2.contourArea)
        area_px = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)

        # Conversion de area (aproximada) a cm^2 
        escala_cm2 = (FACTOR_ESCALA) ** 2
        area_cm2 = area_px * escala_cm2
        circularidad = (4 * np.pi * area_px) / (perimetro ** 2)

        # Relacion de aspecto
        x, y, w, h = cv2.boundingRect(contorno)
        relacion_aspecto = float(w) / h

        # Color promedio en espacio HSV
        color_promedio = cv2.mean(hsv)[:3]

        # Calculo de GLCM y propiedades
        glcm = graycomatrix(gris, [1], [0, np.pi / 2], symmetric=True, normed=True, levels=256)
        contraste = graycoprops(glcm, 'contrast').mean()
        homogeneidad = graycoprops(glcm, 'homogeneity').mean()
        entropia = -np.sum(glcm * np.log2(glcm + (glcm == 0)))
        brillo_promedio = color_promedio[2]

        return [
            f"V{str(especie).zfill(2)}", area_cm2, circularidad, 
            relacion_aspecto, *color_promedio, contraste, entropia, 
            homogeneidad, brillo_promedio
        ]

    except Exception as e:
        print(f"Error procesando '{imagen_path}': {e}")
        return None
    

def guardar_lote_csv(datos, archivo):
    df = pd.DataFrame(datos, columns=COLUMNAS)
    df.to_csv(archivo, mode='a', header=False, index=False)


def procesar_imagenes_por_lotes(lote_tamano=10):
    archivo_csv = "dataset-21-42.csv"

    with open(archivo_csv, 'w') as f:
        f.write(','.join(COLUMNAS) + '\n')

    # Procesar imagenes por especie y en lotes
    lote = []
    for especie in range(21, 43):
        especie_dir = os.path.join(BASE_DIR, str(especie))

        if not os.path.exists(especie_dir):
            print(f"Advertencia: Directorio no encontrado '{especie_dir}'.")
            continue

        for imagen_nombre in os.listdir(especie_dir):
            imagen_path = os.path.join(especie_dir, imagen_nombre)
            vector = extraer_caracteristicas(imagen_path, especie)

            if vector:
                lote.append(vector)

            if len(lote) >= lote_tamano:
                guardar_lote_csv(lote, archivo_csv)
                lote.clear() 

    if lote:
        guardar_lote_csv(lote, archivo_csv)

    print(f"Procesamiento completado. Datos guardados en '{archivo_csv}'.")


if __name__ == "__main__":
    procesar_imagenes_por_lotes()
