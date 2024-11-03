# Dataset de Papas 

Este repositorio contiene un dataset de papas, así como scripts para la extracción de características y edición de fondo de imágenes de papas.

# 🚨 **NOTA IMPORTANTE** 🚨

**EL DATASET DE PAPAS SE ENCUENTRA EN EL SIGUIENTE LINK:**

🔗 [Dataset de Papas en Google Drive](https://drive.google.com/drive/folders/1PuvkgxYiRefR9HbTCAOre0PZ17jWGLEj?usp=sharing)

*debido a su tamaño (8 GB), no se puede almacenar en GitHub.*

---

## Autores

- Callapina Castilla Ciro Gabriel
- Condorcahua Ayllone Ferdinan Junior
- Cordova Ccopa Emerson
- Mamani Crispin Isai Isaac

## Estructura del Proyecto

- `caracteristicas_papas/`: Contiene el archivo CSV con las características del dataset de papas.
- `dataset_papas/`: Contiene las imágenes con fondo blanco del dataset de papas organizadas en carpetas numeradas.
- `script/`: Contiene los scripts para la extracción de características y edición de fondo de las imágenes de papas.

## Características Extraídas

1. **Identificador de Especie**:
   - Un identificador único para la especie de papa, formateado con ceros a la izquierda para tener al menos dos dígitos.

2. **Área**:
   - El área del contorno más grande de la papa en centímetros cuadrados. Esta medida se obtiene a partir del área en píxeles y se convierte utilizando un factor de escala.

3. **Circularidad**:
   - Una medida de cuán circular es el contorno de la papa. Se calcula como `(4 * pi * Area) / (Perimetro^2)`. Un valor cercano a 1 indica una forma casi circular.

4. **Relación de Aspecto**:
   - La proporción entre el ancho y la altura del rectángulo delimitador del contorno de la papa. Un valor cercano a 1 indica una forma casi cuadrada.

5. **Color Promedio en Espacio HSV**:
   - Los valores promedio de los canales H (Hue), S (Saturation) y V (Value) de la imagen en el espacio de color HSV. Estos valores representan el color promedio de la papa.

6. **Contraste**:
   - Una medida de la intensidad de las variaciones entre los píxeles adyacentes en la imagen en escala de grises. Se calcula a partir de la Matriz de Co-ocurrencia de Niveles de Gris (GLCM).

7. **Entropía**:
   - Una medida de la cantidad de desorden o aleatoriedad en la textura de la imagen en escala de grises. Se calcula a partir de la GLCM.

8. **Homogeneidad**:
   - Una medida de la proximidad de los elementos de la GLCM a la diagonal principal. Valores altos indican una textura más uniforme.

9. **Brillo Promedio**:
   - El valor promedio del canal V (Value) de la imagen en el espacio de color HSV, que representa el brillo promedio de la papa.

