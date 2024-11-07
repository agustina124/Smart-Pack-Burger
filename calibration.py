import cv2
import numpy as np
import glob

# Configuración del tamaño del patrón del tablero de ajedrez
PATTERN_SIZE = (5, 4) #base 5 , alto 4
SQUARE_SIZE = 4.0  # Tamaño de cada cuadrado en unidades físicas (puede ser en cm, mm, etc.)

def calibrateCamera():
    # Prepara los puntos 3D en el espacio del tablero de ajedrez (z=0)
    objp = np.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE

    # Arrays para almacenar puntos 3D en el mundo real y puntos 2D en las imágenes
    objpoints = []  # Puntos 3D
    imgpoints = []  # Puntos 2D

    # Directorio que contiene las imágenes de la galería
    images_folder = 'imagenes/*.png'  # Cambia la ruta y extensión según tus imágenes

    # Leer todas las imágenes en el directorio
    imagenes = glob.glob(images_folder)

    # Iterar sobre cada imagen y encontrar las esquinas del patrón
    print("Se detectaron:", len(imagenes), "imagenes")
    for fname in imagenes:
        # Leer la imagen
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Encuentra las esquinas del tablero de ajedrez y pasa a escala de grises.
        ret, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)

        # Si encuentra el patrón, guarda los puntos 3D y 2D
        print(ret)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Dibujar y mostrar las esquinas detectadas (opcional)
            cv2.drawChessboardCorners(img, PATTERN_SIZE, corners, ret)
            cv2.imshow('Esquinas del Tablero', img)
            cv2.waitKey(300)  # Mostrar cada imagen por 300 ms

    cv2.destroyAllWindows()

    # Si se han capturado suficientes imágenes, realiza la calibración
    if len(objpoints) > 0:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print("Matriz intrínseca:\n", mtx) #valor que debe ser reemplazado en el archivo intrinsic.dat
        print("Coeficientes de distorsión:\n", dist) #valor que debe ser reemplazado en el archivo intrinsic.dat

        # Calcular la escala de píxeles a unidades reales en el plano Z=0 (del tablero de ajedrez)
        # Usando la distancia entre las dos primeras esquinas del patrón
        square_size_in_pixels = np.linalg.norm(corners[0] - corners[1])
        pixel_to_real_scale = SQUARE_SIZE / square_size_in_pixels  # Factor de conversión de píxeles a unidades reales

        print("Factor de conversión:\n", pixel_to_real_scale) #valor que debe ser reemplazado en el archivo intrinsic.dat

    else:
        print("No se encontraron suficientes imágenes válidas para la calibración.") #se necesitan aporx entre 30~40 img


calibrateCamera()
