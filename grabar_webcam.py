import cv2
import os

captura = cv2.VideoCapture(0)

salida = cv2.VideoWriter("Sal.avi",cv2.VideoWriter_fourcc(*'XVID'),30.0,(640,480))

while (captura.isOpened()):
  ret, imagen = captura.read()
  if ret == True:
    imagen = cv2.flip(imagen,1)
    cv2.imshow('video', imagen)
    salida.write(imagen)
    if cv2.waitKey(1)==27:
      break
  else: break
salida.release()
captura.release()

cv2.destroyAllWindows()

