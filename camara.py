import PySimpleGUI as sg
import numpy as np
from datetime import date
import urllib.request
import cv2

#Se declara la url de manera indirecta.
#url=('http://192.168.137.203/cam-lo.png')

def main():
    #Conectamos a la camara con la url directa
    stream = urllib.request.urlopen('http://192.168.1.78:8080/video')
    bytes = b''
    #camara = cv2.VideoCapture('https://192.168.1.126:8080/video')
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
    img=None
    #Iniciamos la lectura y actualizacion
    while True:
        #Obtenemos informacion de la interfaz grafica y video
        event, values = window.read(timeout=0)
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1 and bytes != b'':
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            #Si tomamos foto
            
            if event == 'Tomar Fotografia':
                ruta = sg.popup_get_folder(title='Guardar Fotografia', message="Carpeta destino")
                cv2.imwrite(ruta + "/" + str(date.today()) + str(numero) + ".png", jpg)
            try:
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                #Mandamos el video a la GUI
                #cv2.imshow('Video', img)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()  # ditto
                image_elem.update(data=imgbytes)
                numero = numero + 1
            except Exception as e:
                print(e)
                pass
            if cv2.waitKey(1) == 27:
                exit(0)
        else:
            pass
            #print("else")
        #tecla = cv2.waitKey(5) & 0xFF
       
        #Si salimos
        #if tecla ==27:
         #   break
        if event in ('Salir','Exit', None):
            break
        elif event == 'Tomar Fotografia' and img is not None:
            ruta = sg.popup_get_folder(title='Guardar Fotografia', message="Carpeta destino")
            cv2.imwrite(ruta + "/" + str(date.today()) + str(numero) + ".png", img)

        
main()