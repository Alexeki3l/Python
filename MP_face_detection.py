"""
   En este modulo se encuentran los metodos convencionales para detectar rostros en una imagen. Tambien,
se encuentran las funciones para dibujar rectangulos al rededor del rostro y unas funciones adicionales que 
su proposito es crear un DATASET de rostros detectados REC por la webcam usando Mediapipe, entrenar un modelo
con la DATASET creada y otra funcion que reconozca a esas personas

"""


import mediapipe as mp
import cv2
import os
from datetime import datetime
import shutil
import numpy as np
import math


def face_detection():
    """--------------------------------------------------------
    La funcion detecta rostros usando la libreria mediapipe
    -----------------------------------------------------------"""
    face_detection = mp.solutions.face_detection.FaceDetection(model_selection =1, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)
    while True:
        ret,imagen = cap.read()
        if not ret:break
        imagen = cv2.flip(imagen,1)
        imagen2= cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagen2)

        if results.detections:
            for detection in results.detections:
                mp.solutions.drawing_utils.draw_detection(imagen,detection)

        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1)==27:break

def face_detection_2():
    """--------------------------------------------------------------------------
    La funcion detecta rostros usando la libreria mediapipe y con hace uso de
     metodos externos para dibujar el marco del rostro.
    -------------------------------------------------------------------------"""
    face_detection = mp.solutions.face_detection.FaceDetection(model_selection =1, min_detection_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    while True:
        ret,imagen = cap.read()
        if not ret:break
        imagen = cv2.flip(imagen,1)
        imagen2= cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagen2)

        alto,ancho,_ = imagen.shape
        # print(imagen.shape)
        cont=1
        if results.detections: 
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                # draw_rectangulo_detection(imagen,detection,alto,ancho)
                draw_detection(imagen,detection,alto,ancho)
                
                cv2.putText(imagen,"desconocido_"+str(cont),(int(bbox.xmin*ancho),int(bbox.ymin*alto)-15),cv2.FONT_HERSHEY_SIMPLEX,0.7,(208,151,12),2)
                
                cont+=1
        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1)==27:break
                      
def draw_rectangulo_detection(imagen,detection,alto,ancho):
    """
    draw_rectangulo_detection(imagen=Imagen,detection=Deteccion de rostro,alto=Alto de la Imagen,ancho=Ancho de la Imagen)
    ------------------------------------------------------------------
    Se encarga de pintar un rectangulo alrededor del rostro detectado con 
    el uso de la funcion rectangle que ofrece cv2
    -----------------------------------------------------------------
    """
    bbox = detection.location_data.relative_bounding_box
    
    y0=int(bbox.ymin*alto)
    y1=y0 + int(bbox.height*alto)

    x0=int(bbox.xmin*ancho)
    x1=x0 + int(bbox.width*ancho)

    cv2.rectangle(imagen,(x0,y0),(x1,y1),(208,151,12),1)
    
def draw_detection(imagen,detection,alto,ancho):
    """
    draw_detection(imagen=Imagen,detection=Deteccion de rostro,alto=Alto de la Imagen,ancho=Ancho de la Imagen)
    ------------------------------------------------------------------
    Se encarga de pintar una mirilla al rededor del rostro detectado con 
    el uso de la funcion line que ofrece cv2
    -----------------------------------------------------------------
    """
    bbox = detection.location_data.relative_bounding_box

    y0=int(bbox.ymin*alto)
    y1=y0 + int(bbox.height*alto)

    x0=int(bbox.xmin*ancho)
    x1=x0 + int(bbox.width*ancho)

    h=int(bbox.height*alto*0.3) # alto
    w=int(bbox.width*ancho*0.3)  #ancho


    cv2.line(imagen, (x0,y0),(x0+w,y0),(208,151,12),4)
    cv2.line(imagen, (x0,y0),(x0,y0+h),(208,151,12),4)

    cv2.line(imagen, (x0,y1),(x0+w,y1),(208,151,12),4)
    cv2.line(imagen, (x0,y1),(x0,y1-h),(208,151,12),4)

    cv2.line(imagen, (x1,y0),(x1-w,y0),(208,151,12),4)
    cv2.line(imagen, (x1,y0),(x1,y0+h),(208,151,12),4)

    cv2.line(imagen, (x1,y1),(x1-w,y1),(208,151,12),4)
    cv2.line(imagen, (x1,y1),(x1,y1-h),(208,151,12),4)
    
def aux_scrip_BD(imagen,detection,alto,ancho,personName):
    """----------------------------------------------------------------------
     La funcion se ocupa de guardar las imagenes capturadas por mediapipe en la
    direccion del DATASET a la persona correspondiente(personName).
    -----------------------------------------------------------------------
    """

    pathBD=os.path.dirname(os.path.abspath(__file__))+"/BD"  
    pathName=pathBD+"/"+personName
    total=0
    lista=os.listdir(pathName)

    bbox = detection.location_data.relative_bounding_box

    auxImagen=imagen.copy()
    instanteInicial = datetime.now().second
    # al final de la partida
    instanteFinal = datetime.now().second
    tiempo = instanteFinal - instanteInicial # Devuelve un objeto 
    
    y0=int(bbox.ymin*alto)
    y1=y0 + int(bbox.height*alto)

    x0=int(bbox.xmin*ancho)
    x1=x0 + int(bbox.width*ancho)

    cv2.rectangle(imagen,(x0,y0),(x1,y1),(208,151,12),1)
    if tiempo ==0:
        if not os.path.exists(pathName):
            os.makedirs(pathName,exist_ok=True)
        else: 
                        
            if len(lista)>=0:
                rostro=auxImagen[y0:y1,x0:x1]
                rostro=cv2.resize(rostro,(200,200),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(pathName+"/rostro_{}.jpg".format(len(lista)),rostro)
                print(pathName+"/rostro_{}.jpg".format(len(lista)))

def scrip_BD(personName):

    """scrip_BD(personName="NAME_DATASET")
    --------------------------------------------------------------------------------------------
    Es el metodo que se encarga de crear el DATASET y almacenar los rostros que se utilizaran 
    para el reconocimiento de personas de interes.
    Al metodo se le asigna por parametro el nombre de la persona la cual su rostro sera 
    almacenado
    -------------------------------------------------------------------------------------------"""

    #retorna la direccion del archivo invocador
    # print(pathlib.Path(__file__).parent.absolute())
    #retorna la direccion de la carpeta que tiene
    # print(pathlib.Path().absolute()) 
    # retorna la direccion del archivo invocador
    # os.path.dirname(os.path.abspath(__file__))

    face_detection = mp.solutions.face_detection.FaceDetection(model_selection =1, min_detection_confidence=0.5)
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while True:
        ret,imagen = cap.read()
        if not ret:break
        imagen = cv2.flip(imagen,1)
        imagen2= cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagen2)

        alto,ancho,_ = imagen.shape
        # print(imagen.shape)
        
        if results.detections: 
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                aux_scrip_BD(imagen,detection,alto,ancho,personName)
                cv2.putText(imagen,personName,(int(bbox.xmin*ancho),int(bbox.ymin*alto)-15),cv2.FONT_HERSHEY_SIMPLEX,0.7,(208,151,12),2)
         
        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1)==27:
            print("Alexei tiene "+len(os.listdir(os.path.dirname(os.path.abspath(__file__))+"/BD/"+personName)+" imagenes almacenadas"))
            break

def normalizar_DATASET(pathDirection):

    """normalizar_DATASET(pathDirection="PATH/IMAGENES)"""
    """La funcion se encarga de normalizar las imagenes encontradas en la direccion entrada 
    por parametro a 200x200.Guardandola en la direccion pathOut de salida y eliminando la direccion
    entrada.
    --------------------------------------------------------------------
    La funcion lanza un error si las imagenes ya estan normalizadas """

    lista=os.listdir(pathDirection)
    pathOut=os.path.dirname(os.path.abspath(__file__))+"/BD/AuxNormalizada"
    if not os.path.exists(pathOut):
        os.makedirs(pathOut,exist_ok=True)
    opcion=input("¿Desea normalizar los datos? (si/no)")
    cont=1
    if "si" in opcion:
        print("Normalizando imagenes.....")
        for image_name in lista:
            
            imagen=cv2.imread(pathDirection + "/" + image_name)
            rostro = cv2.resize(imagen,(200,200),interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(pathOut+"/image_{}.jpg".format(cont),rostro)
            
            cont+=1
            if cv2.waitKey(1)==113:
                break
        print("Se normalizaron a una escala 200x200 todas las imagenes")
        op=input("¿Desea eliminar la direccion de entrada? (si/no)---> ")
        if "si" in op:
            shutil.rmtree(pathDirection)
            print("La direccion anterior fue eliminada")
        elif "no" in op:
            print(pathDirection+" se conservara")
            return
        else:
            print("Se espera una respuesta de [si/no]")
   
    elif "no" in opcion:
        return
    else:
        print("Se espera una respuesta de [si/no]")

def normalizar_NAME_DATASET(pathDirection,personName):

    """-----------------------------------------------------------------------------------------------
         normalizar_NAME_DATASET (pathDirection="PATH/IMAGENES",personName="nombre de persona en DATASET")
    La funcion se encarga de guardar con un mismo nombre (image_) las imagenes que se encuentren en pathDirection
    y guardandolas en personName que seria la carpeta de la persona en DATASET con nombres normalizados
    -------------------------------------------------------------------------------------------------"""
    # lista con las imagenes de entrada
    lista=os.listdir(pathDirection)
    pathOut=os.path.dirname(os.path.abspath(__file__))+"/BD/"+personName+"/AuxNormalizada"

    if not os.path.exists(pathOut):
        os.makedirs(pathOut,exist_ok=True)

        cont=0

        for file_name in lista:
            imagen=cv2.imread(pathDirection+"/"+file_name)
            cv2.imwrite(pathOut+"/image_{}.jpg".format(cont),imagen)

            cont+=1
    print("Se ha terminado la operacion")

def train_DATASET():

    """
    La funcion exporta un archivo XML correspondiente con el metodo de entrenamiento
    escogido en el codigo. El codigo se encuentra comentariado para dar una confianza 
    mayor de uso.
    """

    pathBD=os.path.dirname(os.path.abspath(__file__))+"/BD"  # retorna la direccion del archivo invocador
    listNames=os.listdir(pathBD)
    print("Lista de personas:", listNames)

    labels= []
    facesData = []
    label = 0  
    pathModel=os.path.dirname(os.path.abspath(__file__))+"/Modelo"
    if not os.path.exists(pathModel):
        os.makedirs(pathModel,exist_ok=True)

    for nameDir in listNames:
        personPath = pathBD +"/"+nameDir
        print("Leyendo las imagenes....")

        for fileName in os.listdir(personPath):
            print("Rostros: ",nameDir + "/" + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+"/"+fileName,0))
            image = cv2.imread(personPath+"/"+fileName,0)
        label = label + 1

    # print("Labels: ",labels)
    # print("Numero de etiquetas 0:",np.count_nonzero(np.array(labels)==0))
    # cv2.destroyAllWindows()
    
    # Crear modelo ha utilizar
    # face_recognizer = cv2.face.EigenFaceRecognizer_create()
    # face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))

    # if os.path.exists(pathModel+"/modeloLBPHFace.xml"):
    #     print("Existe en esta direccion un archivo con el mismo nombre")
    #     opcion=input(" (si/no)")
    #     if "si" in opcion:
    #         os.remove(pathModel+"/modeloLBPHFace.xml")
    #     elif "no" in opcion:
    #         return
    #     else:
    #         print("Se espera una opcion de (si/no)")

    # Almacenando el modelo
    # face_recognizer.write(pathModel+"/modeloEigenFace.xml")
    # face_recognizer.write(pathModel+"/modeloFisherFace.xml")
    face_recognizer.write(pathModel+"/modeloLBPHFace.xml")
    print("Modelo almacenado....")

def face_recognition():
    """
    face_recognition()
    La funcion se encarga de predecir un rostro apartir del archivo XML exportado 
    por la funcion train_DATASET().
    """
    dataPath=os.path.dirname(os.path.abspath(__file__))+"/BD"
    imagePaths = os.listdir(dataPath)
    print("imagePaths=",imagePaths)

    # face_recognizer= cv2.face.EigenFaceRecognizer_create()
    face_recognizer= cv2.face.LBPHFaceRecognizer_create()

    # Leyendo modelo
    # face_recognizer.read(os.path.dirname(os.path.abspath(__file__))+"/Modelo/modeloEigenFace.xml")
    face_recognizer.read(os.path.dirname(os.path.abspath(__file__))+"/Modelo/modeloLBPHFace.xml")

    cap = cv2.VideoCapture(0)

    face_detection = mp.solutions.face_detection.FaceDetection(model_selection =1, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)
    while True:
        ret,imagen = cap.read()
        if not ret:break
        imagen = cv2.flip(imagen,1)
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        imagen2= cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagen2)

        alto,ancho,_ = imagen.shape

        cont=1

        if results.detections:
            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                y0=int(bbox.ymin*alto)
                y1=y0 + int(bbox.height*alto)

                x0=int(bbox.xmin*ancho)
                x1=x0 + int(bbox.width*ancho)

                rostro = auxFrame[y0:y1,x0:x1]
                rostro = cv2.resize(rostro,(200,200),interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                cv2.putText(imagen,"{}".format(result),(x0,y0-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                draw_detection(imagen,detection,alto,ancho)
                

                # -----EigenFace
                # if result[1]<5700:
                #     cv2.putText(frame,"{}".format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                #     if cont==0:
                #         hablar(f"Se ha detectado ha {imagePaths[result[0]]}")
                #         cont=1

                # else:
                #     cv2.putText(frame,"Desconocido",(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        
                #-----Modelo LBPH
                if result[1]<60:
                    cv2.putText(imagen,"{}".format(imagePaths[result[0]]),(x0,y0-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    # cv2.putText(imagen,"{}".format(imagePaths[result[0]])+"    "+f'{int(detection.score[0]*100)}%',(x0,y0-25),2,1.1,(0,255,0),1,cv2.LINE_AA)

                    draw_detection(imagen,detection,alto,ancho)

                else:
                    cv2.putText(imagen,"Desconocido_{}".format(cont),(x0,y0-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cont+=1
                    draw_detection(imagen,detection,alto,ancho)

        cv2.imshow("Face Recognition",imagen)
        if cv2.waitKey(1)==27:break

    cap.release()
    cv2.destroyAllWindows()


face_recognition()
