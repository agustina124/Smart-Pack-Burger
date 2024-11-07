# Smart-Pack-Burger
#Set up del ambiente
-Colocar la webcam en el soporte, a una altura de 79 cm respecto a la mesa de trabajo.
-Encender la lámpara del soporte.
-Ubicar el tablero de ajedrez sobre la mesa de trabajo. Asegurar que la superficie donde esté sea plana.
-Una vez capturadas las imágenes utilizando el código calibration_v2.py (se recomienda capturar como mínimo entre 30 a 40       imágenes), retirar el tablero de la escena.
-Ajustar los parámetros de la cámara (matriz intrínseca, coeficiente de distorsión y factor de conversión) en el código -       intrinsic.dat, utilizando los datos arrojados en el código calibration.py.
-Tomar las coordenadas de tres esquinas de la cámara con el comando rob.get_pos(). Una vez encontradas dichas coordenadas,       reemplazar las mismas en el código Servidor.py, línea 20. (Recordar multiplicar por 1000 dichas coordenadas).
-Por último, correr el código Servidor.py y ajustar la ventana del umbral según se requiera.
-Una vez seteado el umbral, se debe colocar dicho valor de umbral en el código detector.py.
-Ubicar la bandeja en la posición deseada.


#Ejecución
Una vez que se haya finalizado el set-up, se deben correr los siguientes archivos con Python:
-calibration_v2.py: Se utiliza para capturar las imágenes del tablero de ajedrez para posteriormente almacenarlas en la -carpeta “imagenes”. Para luego, utilizarlas en el código “calibration”.
-calibration.py: Lee todas las imagenes de la galeria e itera sobre las mismas para encontrar las esquinas del patrón. Si se han capturado suficientes imágenes, realiza la calibración.
-prueba movimiento.py: Se utiliza para conocer la posición de las esquinas de la cámara.
-intrinsic.dat: Este archivo posee la matriz intrínseca, coeficiente de distorsión y factor de conversión de la cámara.
-detector.py : Muestra los contornos de las piezas y dibuja una recta desde el origen hasta el centro de cada uno de estos contornos.
-Servidor: Establece la conexión con el teach pendant para recibir la consulta y pasarle las coordenadas donde se encuentran las piezas para luego hacer la recolección de las mismas. Además,  sirve para revisar que las piezas estén siendo detectadas correctamente.
-Movimientos de Picking-Teach Pendant: Establece una conexión mediante un socket para solicitar a la computadora la coordenada de la pieza. Luego, el robot transporta la pieza a la bandeja y repite el proceso de consulta para cada pieza sucesiva.En caso de querer parar al robot en cualquier momento de la ejecución presionar el botón rojo que se encuentra en la  tableta de control del robot.
