from operator import invert
from turtle import distance
# from types import NoneType
from xml.etree.ElementTree import tostring
import cv2 as cv
import numpy as np
import sys
import math
from urx import robotiq_two_finger_gripper
import time
import socket
from typing import List
import urx
#from detector import read_camera_parameters, get_delta_cam, get_centers, show_centers

# MAIN
print("------------------------------------------------------------")
print("                     BIENVENIDO                             ")
print("------------------------------------------------------------")

# Conect to robot:
HOST = "192.168.0.18" # IP del robot, puede variar.
PORT = 30002 # port: 30001, 30002 o 30003, en ambos extremos

rob = urx.Robot(HOST) #se conecta al robot 
print("Conectando a IP: ", HOST)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #se crea un socket para la comunicacion IP con el robot
print("conectando...")
s.connect((HOST, PORT)) #se conecta al robot usando el IP y puerto
time.sleep(0.5)
print("Conectado con el robot")

print("Posición cartesiana actual:",rob.get_pos()) #se obtiene la posicion del robot, esto lo usamos para saber cuales son las esquinas de la camara

