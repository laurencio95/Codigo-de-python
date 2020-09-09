import PySimpleGUI as sg
import numpy as np
from datetime import date
import urllib.request
import cv2

#Se declara la url de manera indirecta.
#url=('http://192.168.137.203/cam-lo.png')

def main():
    #Conectamos a la camara con la url directa
    camara = cv2.VideoCapture('https://192.168.8.8:8080/video')
    #camara = cv2.VideoCapture(0)

    #Elegimos un tema de PySimpleGUI
    sg.theme('DarkGreen5')
    #Definimos los elementos de la interfaz grafica
    layout = [[sg.Button('Tomar Fotografia'),sg.Button('Salir')],[sg.Image(filename='', key='-image-')]]
    #Creamos la interfaz grafica
    window = sg.Window('Camara ESP32-OV2640',
                       layout,
                       no_titlebar=False,
                       location=(0, 0),
                       resizable=True)

    image_elem = window['-image-']

    numero = 0
    #Iniciamos la lectura y actualizacion
    while camara.isOpened():
        #Obtenemos informacion de la interfaz grafica y video
        event, values = window.read(timeout=0)
        ret, frame = camara.read()
        #tecla = cv2.waitKey(5) & 0xFF
       
        #Si salimos
        #if tecla ==27:
         #   break
        if event in ('Salir','Exit', None):
            break

        #Si tomamos foto
        elif event == 'Tomar Fotografia':
            ruta = sg.popup_get_folder(title='Guardar Fotografia', message="Carpeta destino")
            cv2.imwrite(ruta + "/" + str(date.today()) + str(numero) + ".png", frame)

        if not ret:
            break

        #Mandamos el video a la GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        image_elem.update(data=imgbytes)
        numero = numero + 1
main()