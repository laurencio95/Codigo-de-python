import numpy as np
import cv2              #
import urllib.request   #Libreria para hacer funcionar la url
from io import BytesIO
import os, sys
import datetime
from PIL import Image

url=('http://192.168.137.161/cam-lo.png')

winName = 'CAMARA 1'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
scale_percent = 80

while(True):
    imgResponse = urllib.request.urlopen (url)
    imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
    img = cv2.imdecode (imgNp, -1)
    cv2.imshow(winName, img)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
   
cv2.destroyAllWindows()