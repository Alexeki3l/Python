import os
import cv2
import pyttsx3


engine = pyttsx3.init("sapi5")             # "sapi5"
rate = engine.getProperty("rate")
engine.setProperty("rate", 155)            #Se define la velocidad en que hablara
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

dataPath = "D:\Alexei-Todo\Python\prueba\Reconocimiento de rostros\Archivos"
imagePaths = os.listdir(dataPath)
print("imagePaths=",imagePaths)

# face_recognizer= cv2.face.EigenFaceRecognizer_create()
face_recognizer= cv2.face.LBPHFaceRecognizer_create()

# Leyendo modelo
# face_recognizer.read("modeloEigenFace.xml")
face_recognizer.read("modeloLBPHFace.xml")

cap = cv2.VideoCapture(0)

faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    if ret ==False:break
    frame=cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    faces = faceClassifier.detectMultiScale(gray,1.3,5)
    cont=0

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x, y),(w+x, y+h),(0, 255, 0), 2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        cv2.putText(frame,"{}".format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
        
        # EigenFace
        # if result[1]<5700:
        #     cv2.putText(frame,"{}".format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #     if cont==0:
        #         hablar(f"Se ha detectado ha {imagePaths[result[0]]}")
        #         cont=1

        # else:
        #     cv2.putText(frame,"Desconocido",(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        
        #Modelo LBPH
        if result[1]<60:
            cv2.putText(frame,"{}".format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        else:
            cont+=1
            cv2.putText(frame,"Desconocido_{}".format(cont),(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    cv2.imshow("frame",frame)
    k=cv2.waitKey(1)
    if k==27:break

cap.release()
cv2.destroyAllWindows()