import cv2
import numpy as np

# Configuración del tamaño del patrón del tablero de ajedrez (6x5)
pattern_size = (5, 4)
#Tamaño de cada cuadrado del tablero
square_size = 4.0

# Prepara los puntos 3D en el espacio del tablero de ajedrez (z=0)
objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays para almacenar puntos 3D en el mundo real y puntos 2D en las imágenes
objpoints = []
imgpoints = []

# Captura de la cámara
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara")
    exit()

print("Presiona 's' para capturar una imagen para la calibración, o 'q' para salir")

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame de la cámara")
        break
    #Cada vez que lee cada imagen, la convierte en escala de grises para facilitar la deteccion.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None) #se encuentran las esquinas del patron

    copy = img.copy()

    if ret:
        cv2.drawChessboardCorners(img, pattern_size, corners, ret) #Dibuja las esquinas detectadas sobre la imagen 

    cv2.imshow('Calibracion de Camara', img)
  
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite('Backup'+str(len(imgpoints))+".png", copy)
        print("Patrón de ajedrez detectado, guardando puntos...")
        objpoints.append(objp)
        imgpoints.append(corners)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print("Matriz intrínseca:\n", mtx)
print("Coeficientes de distorsión:\n", dist)

if len(objpoints) < 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Matriz intrínseca:\n", mtx)
    print("Coeficientes de distorsión:\n", dist)

    #HASTA ACA ES EL TEMA DE CALIBRACION. El resto del codigo era un extra.
    
    # Captura nuevamente para medir una circunferencia
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=50, param2=30, minRadius=10, maxRadius=200)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # Dibuja el círculo y su centro
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

               # Desproyecta el punto de 2D a 3D
                point_2d = np.array([[x, y]], dtype=np.float32)
                undistorted = cv2.undistortPoints(np.expand_dims(point_2d, axis=1), mtx, dist, P=mtx)

                # El radio en píxeles se convierte a distancia en el mundo real (en el plano Z=0)
                # Calcular la distancia focal promedio de la cámara
                focal_length = (mtx[0, 0] + mtx[1, 1]) / 2.0

                # El radio en píxeles se convierte a distancia real:
                real_radius = (r * 77)/focal_length  #76 es la altura de la pieza a la camara.
                # Mostrar el radio calculado en la imagen
                cv2.putText(frame, f"Radio real: {real_radius:.2f} unidades", (int(x) - 50, int(y) - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),2)
                print(f"Radio real estimado de la circunferencia: {real_radius} unidades físicas")
                print(point_2d, r)
        cv2.imshow('Detección de Circunferencia', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("No se capturaron suficientes imágenes para la calibración.")
