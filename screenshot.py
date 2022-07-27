# Captura de pantalla

import pyautogui
import numpy as np
import cv2

image= pyautogui.screenshot()
image=cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
cv2.imwrite("image.png",image)