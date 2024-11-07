import cv2 as cv #para procesar imagenes
import numpy as np #para operaciones matematicas
import sys #proporciona acceso a algunas variables y funciones que interactuen con el interprete de python.


MAX_AREA = 500000 #area maxima de los contornos, se ajusta segun tamaño de piezas a utilizar 
MIN_AREA = 500 #area minima de los contornos, se ajusta segun tamaño de piezas a utilizar
threshold_value = 134 #valor del umbral INICIAL

def update_threshold(value): #actualiza el valor del umbral
    global threshold_value
    threshold_value = value

cv.namedWindow('Binary')
cv.resizeWindow('Binary', 640, 480) #tamaño de la ventana
cv.createTrackbar('Threshold', 'Binary', threshold_value, 250, update_threshold) #crea una barra de seguimiento para cambiar el valor del umbral


def get_contours(image): #obtiene los contornos de la imagen
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    ret, threshold = cv.threshold(gray_image, threshold_value, 255, cv.THRESH_BINARY_INV)

    cv.imshow('Binary', threshold)

    structuring_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (1, 1))
    morph_open = cv.morphologyEx(threshold, cv.MORPH_OPEN, structuring_element)
    denoised_image = cv.morphologyEx(morph_open, cv.MORPH_CLOSE, structuring_element) #saca ruido a la imagen

    cv.imshow('Denoised', denoised_image)

    contours, _ = cv.findContours(denoised_image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    return contours


def show_centers(img): #muestra los centros de los contornos en la imagen
    contours = get_contours(img)
    
    for contour in contours:
        area = cv.contourArea(contour)
        if area > MIN_AREA and area < MAX_AREA:
            M = cv.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv.drawContours(img, [contour], -1, (0, 255, 0), 3)
            cv.line(img, [0,0], [cX,cY], (0, 255, 0), 5)


def get_centers(img): #obtiene los centros de los contornos en la imagen 
    contours = get_contours(img)

    centers = [] #inicializo la variable de contornos filtrados
    for contour in contours:
        area = cv.contourArea(contour)
        if area > MIN_AREA and area < MAX_AREA:
            M = cv.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append([cX, cY])
    return centers


def execute(in_source): #ejecuta el programa
    cap = cv.VideoCapture(in_source)

    while True:
        ret, img = cap.read()
        if ret == False: break

        show_centers(img)
        cv.imshow('frame', img)

        k = cv.waitKey(20)
        if k == 27: break #27 = ESC key.--> es para romper el bucle

    cap.release()
    cv.destroyAllWindows()


#if __name__ == '__main__': #si el modulo es ejecutado como principal
#    input_source = 'media/test.mp4'
#    if len(sys.argv) > 1:
#        input_source = int(sys.argv[1])
#    execute(1)
