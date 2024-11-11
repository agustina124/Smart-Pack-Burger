'''
Este servidor TCP/IP se ejecuta en PC preferentemente con IP fija y un puerto cualquiera.
La IP y el puerto se deben transcribir en el cliente que ejecuta en el controlador del robot.

Dentro del bucle principal while True se debe implementar el código que determina
las coordenadas x,y a informar al robot cuando consulte.
'''

import socket
import threading
import time
import numpy as np

from detector import get_centers, show_centers
import cv2 as cv

cap = cv.VideoCapture(1)
coords_virtual = []

#Coordenadas de las esquinas de la camara.Se deben actualizar cada vez que se haga uso del mismo.
COORD_A, COORD_B, COORD_C = [246.73, 64.93],[825.56, -39.24], [196.14, -345.98] 
COORD_D = [COORD_B[0]+COORD_C[0]-COORD_A[0], COORD_B[1]+COORD_C[1]-COORD_A[1]]

while True:
    ret, img = cap.read()
    if ret == False: break

    show_centers(img)
    cv.imshow('Detector', img)

    k = cv.waitKey(20)
    #Se debe presionar "s" para tomar una foto de las piezas detectadas que muestra en la pantalla.
    if k == ord('s'):
        coords_virtual = get_centers(img)
        print("Elementos guardados:", len(coords_virtual)) #Te indica cuantas piezas encontro en la mesa de trabajo.
        cap.release()
        cv.destroyAllWindows()
        break


def read_camera_parameters(filepath ='intrinsic.dat'):
    inf = open(filepath, 'r')
    cmtx, dist = [], []

    #Ignorar primera titulo (porque justamente no tiene los parametros que necesitamos)
    line = inf.readline()
    for _ in range(3):
        line = inf.readline().split()
        line = [float(en) for en in line]
        cmtx.append(line)

    #Ignorar segundo titulo (porque justamente no tiene los parametros que necesitamos)
    line = inf.readline()
    line = inf.readline().split()
    line = [float(en) for en in line]
    dist.append(line)

    return np.array(cmtx), np.array(dist)


# Convertir coordenadas virtuales a reales
def convert_coords(cmtx, dist, coords_virtual):
    puntos_imagen = np.array([[0, 0], [640, 0], [0, 480], [640, 480]], dtype=np.float32) # Coordenadas de las esquinas en la imagen (u, v)
    puntos_reales = np.array([COORD_A, COORD_B, COORD_C, COORD_D], dtype=np.float32) # Coordenadas reales correspondientes (X, Y, en el sistema del brazo robótico)
    
    # Calcular la matriz de homografía
    H, _ = cv.findHomography(puntos_imagen, puntos_reales)
    
    coords_real = []
    for coord in coords_virtual:
        # Corregir la distorsión
        coord_fixed = cv.undistortPoints(np.array([[[coord[0], coord[1]]]], dtype=np.float32), cmtx, dist, P=cmtx)
        print(coord)
        print(coord_fixed)
        # Asegurarse de que el punto esté en el formato (1, 1, 2)
        punto_imagen = np.array([[[coord_fixed[0][0][0], coord_fixed[0][0][1]]]], dtype=np.float32)
        
        # Transformar el punto a coordenadas reales
        punto_real = cv.perspectiveTransform(punto_imagen, H)
        
        # Guardar la coordenada transformada
        coords_real.append(punto_real[0][0])

    return coords_real


# Leer los parámetros de la cámara
cmtx, dist = read_camera_parameters()
cord = convert_coords(cmtx, dist, coords_virtual)
print(cord)
print([list(c) for c in cord])
cord=[list(c) for c in cord]

# IP y puerto de escucha de este servidor TCP/IP
HOST = "192.168.0.105" # Dirección IP (Ethernet) de este servidor, se saca colocando en la terminal IPconfig
PORT = 65432           # Puerto donde escucha el servidor, un número inventado que no esté usado por otro servicio

# Función que ejecuta el servidor TCP/IP en un hilo aparte
def start_server():
    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor escuchando en {HOST}:{PORT}...")

        # Bucle infinito para aceptar múltiples conexiones
        while True:
            # Usamos un timeout para evitar bloqueo completo en accept
            s.settimeout(1.0)
            try:
                # accept() bloquea hasta que recibe una consulta
                # addr contiene la ip de la máquina que realiza la consulta
                conn, addr = s.accept()
            except socket.timeout:
                # Si no hay conexión, seguimos esperando
                continue

            with conn:
                # Bucle para recibir múltiples mensajes en la misma conexión
                while True:
                    # Recibir la consulta del cliente, con un tamaño máximo de 1024 bytes
                    data = conn.recv(1024)
                    if not data:
                        # Si no hay más datos, el cliente cerró la conexión
                        print("Cliente desconectado.")
                        break
 
                    consulta = data.decode()
                    print(f"Consulta: {consulta}")
                   
                    if consulta == "GET COUNT":
                        
                        response = f"({len(cord)}, 9)\n" #aca responde longitud de la lista, cantidad de coordenadas que se le va a pasar

                    if consulta == "GET POS":
                        p=cord.pop() #.pop toma el ultimo valor de la lista, y luego de tomarlo lo elimina y sigue con el siguiente 
                    # Generar la respuesta
                        response = f"({(p[0])/1000}, {p[1]/1000})\n" #le pasamos las coordenadas que se encuentran en la lista 
                    conn.sendall(response.encode())
                    print(f"Respuesta enviada: {response}")


# Crear un hilo para el servidor
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Hacer que el hilo se cierre cuando termine el programa principal
server_thread.start()

# Programa principal continúa haciendo otras cosas
print("Servidor en ejecución en segundo plano. El programa principal puede seguir trabajando.")
print("Ctrl+c para detener el servidor y terminar el programa.")

# Bucle principal donde se determinan las coordenadas x e y
try:
    while True:
       
        w=0
except KeyboardInterrupt:
  print("Programa interrumpido por el usuario.")
