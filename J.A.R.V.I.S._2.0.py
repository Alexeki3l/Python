
# ------------------------DEPENDENCIAS----------------------------
from concurrent.futures import process
from unicodedata import normalize
from urllib import request
import speech_recognition as sr
import playsound as play
import mediapipe as mp
import multiprocessing
import requests
import urllib3
import reproductor as play
import unidecode
import threading
import wikipedia
import datetime
import pyttsx3
import urllib
import json
import time
import wmi
import cv2
import os
import re

# --------------------------------------------------------------------
# -----------------------------BODY CODE------------------------------
# --------------------------------------------------------------------


def iniciar_Conf():
    # "sapi5 Para Windows"
    engine = pyttsx3.init("sapi5")    
    rate = engine.getProperty("rate")
    #Se define la velocidad en que hablara
    engine.setProperty("rate", 130)            
    voices = engine.getProperty("voices")
    engine.setProperty("voices", voices[0].id)
    return engine

def hablar(texto):
    engine=iniciar_Conf()
    engine.say(texto)
    engine.runAndWait()
    
def escuchar():

    microfono = sr.Recognizer()  
    with sr.Microphone() as fuente:
         print("Escuchando...")
        #  hablar("Escuchando")
         microfono.pause_threshold = 1
        # Eliminar ruido de ambiente
         microfono.adjust_for_ambient_noise(fuente, duration=1)
         audio =microfono.listen(fuente) 
         time.sleep(1.5)
    try:
         print("Reconociendo...")
        #  hablar("Reconociendo...")
         consulta = microfono.recognize_google(audio, language="es-ES")
         print(f"Usted dijo: {consulta}\n")
        #  hablar(f"Usted dijo {consulta}")

    except Exception as exc:
        # hablar("Por favor. Repita lo que dijo")
        print("Por favor. Repita lo que dijo")
        return "None"

    return consulta 

def aux_busqueda_Wiki(lissta):

    memoryPath=os.path.dirname(os.path.abspath(__file__))+"/BD/memory"

    print("Elija una opcion")
    hablar("Elija una opcion")
    opcion = escuchar().lower()
    time.sleep(1.5)
    lista_num = ["uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez",
                "once","doce","trece","catorce","quince","dieciseis","diecisiete",
                "dieciocho","diecinueve","veinte","veintiuno","veintidos","veintitres","veinticuatro"]
 # ""convirtiendo el str en numero y haciendolo coincidir con el listado
    """try:"""
    if opcion in lista_num:
        print(wikipedia.summary(lissta[lista_num.index(opcion)], sentences = 5))
        hablar(wikipedia.summary(lissta[lista_num.index(opcion)], sentences = 5))
    
    elif opcion in lissta:
        var=lissta[lissta.index(opcion)]
        archivo= open(memoryPath+"/"+var.lower()+".txt", "w")
        all_result=wikipedia.summary(var)
        # ---------------------------------------------------
        
        s1 = all_result.replace("ñ", "#").replace("Ñ", "%")
        s2 = normalize("NFKD", s1)\
          .encode("ascii","ignore").decode("ascii")\
          .replace("#", "ñ").replace("%", "Ñ")

        # -----------------------------------------------------
        archivo.write(s2)
        archivo.close()

        print(wikipedia.summary(var, sentences=3))
        hablar(wikipedia.summary(var, sentences=3))

    elif "Salir" in opcion:
        return lord_comander()

    else:
        hablar("Estoy esperando que elijas")
        aux_busqueda_Wiki(lissta)

def search_Wiki(subconsulta):

    memoryPath=os.path.dirname(os.path.abspath(__file__))+"/BD/memory"
    archivo=memoryPath+"/"+subconsulta+".txt"
    if not os.path.exists(archivo):
      archivo= open(memoryPath+"/"+subconsulta+".txt", "w")

  
    wikipedia.set_lang("es")
# -------------------------------------------
    resultado = wikipedia.summary(subconsulta, sentences = 3)
    
    hablar(f"Buscando sobre {subconsulta}")
    resultados = list(wikipedia.search(subconsulta))

    if len(resultados) ==1:
        resultado = wikipedia.summary(subconsulta, sentences = 3)
        print("Segun la wikipedia", resultado)
        hablar("Segun la wikipedia")
        hablar(resultado)
        all_result=wikipedia.summary(subconsulta)
        # ---------------------------------------------------
        
        s1 = all_result.replace("ñ", "#").replace("Ñ", "%")
        s2 = normalize("NFKD", s1)\
          .encode("ascii","ignore").decode("ascii")\
          .replace("#", "ñ").replace("%", "Ñ")

        # -----------------------------------------------------
        archivo.write(s2)
        archivo.close()
        
        #hablar(resultado) 
    else:
        count = 1
        hablar(f"Estoy mostrando en consola todos los contenidos encontrados relacionados con {subconsulta}")
        print(f"Estoy mostrando en consola todos los contenidos encontrados relacionados con {subconsulta}")
        lista=[]
        for resul in resultados:
                
            print(count,"-->",resul.lower())
            hablar(resul)
            lista.append(resul.lower())
            resultados.pop(resultados.index(resul))
            count += 1

        aux_busqueda_Wiki(lista)

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

def how_is(x,y,result):
    cont=1

    dataPath=os.path.dirname(os.path.abspath(__file__))+"/BD/image/faces"
    imagePaths = os.listdir(dataPath)

    if result[1]<60:
        # cv2.putText(imagen,"{}".format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
        # cv2.putText(imagen,"{}".format(imagePaths[result[0]])+"    "+f'{int(detection.score[0]*100)}%',(x0,y0-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
        return imagePaths[result[0]]

        
    else:
        # cv2.putText(imagen,"Desconocido_{}".format(cont),(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
        cont+=1
        return "Desconocido_{}".format(cont)
        
def face_recognition():

    face_recognizer= cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(os.path.dirname(os.path.abspath(__file__))+"/BD/models/modeloLBPHFace.xml")

    face_detection = mp.solutions.face_detection.FaceDetection(
        model_selection =1, min_detection_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    cont=1

    while True:
        ret,imagen = cap.read()
        if not ret:break
        imagen = cv2.flip(imagen,1)
        alto,ancho,_ = imagen.shape
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        imagen2= cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        results = face_detection.process(imagen2)
        

        if results.detections:
            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                y0=int(bbox.ymin*alto)
                y1=y0 + int(bbox.height*alto)

                x0=int(bbox.xmin*ancho)
                x1=x0 + int(bbox.width*ancho)

                rostro = auxFrame[y0:y1, x0:x1]
                rostro = cv2.resize(rostro,(200,200),interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                how_is(x0,y0,result)

                if  cont==1:

                    # hablar("Hola"+str(name))
                    
                    cont+=1

                # cv2.putText(imagen,"{}".format(result),(x0,y0-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                draw_detection(imagen,detection,alto,ancho)
        
        cv2.imshow("Face Recognition",imagen)
        if cv2.waitKey(1)==27:break
        
    cap.release()
    cv2.destroyAllWindows()

def lord_comander():
    """
    La funcion donde se encuentra todas las ordenes que va a ejecutar el 
    programa.
    """
    bandera=False
    memoryPath=os.path.dirname(os.path.abspath(__file__))+"/BD/memory"

    cont=0
    while True:

        print("A la espera de comandos....")

        consulta=escuchar().lower()

        if "Jarvis" in consulta:
            hablar("Aki estoy. Digame usted")
            bandera=True

        elif ("busca sobre la " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("busca sobre la ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)

        elif ("busca sobre el " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("busca sobre el ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)
        
        elif ("qué es la " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("qué es la ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)

        elif ("qué es el " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("qué es el ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)

        elif ("qué es un " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("qué es un ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)

        elif ("qué es una " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("qué es una ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)
        
        elif ("quién es " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("quién es ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)
        
        elif ("buscame sobre " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("buscame sobre ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)

        elif ("qué sabes de " in consulta) and (bandera==True):
            
            subconsulta=consulta.split("qué sabes de ")[1]
            print(subconsulta)
            if not os.path.exists(memoryPath):
                os.makedirs(memoryPath,exist_ok=True)
                # subconsulta=consulta.split("busca sobre la ")[1]
                search_Wiki(subconsulta)
            else:
                memorys=os.listdir(memoryPath)
                subconsulta1=subconsulta+".txt"
                if subconsulta1 in memorys:
                    archivo=memoryPath+"/"+subconsulta1
                    with open(archivo) as fichero:
                        for linea in fichero:
                            hablar(linea)
                            
                else:
                    search_Wiki(subconsulta)
      
        elif ("salir" in consulta) and (bandera==True):
            break

        elif ("cuantos suscriptores tiene" in consulta) and (bandera==True):
            name_subs=consulta.replace("cuantos suscriptores tiene","")
            data=urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name_subs+"&key="+key).read()
            subs=json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            hablar(name_subs + " tiene {:,d}".format(int(subs)))

        elif cont==(cont//2==0):
            time.sleep(3)

        elif ("quiero hablar" in consulta) and (bandera==True):
            hablar("¿De que quieres hablar?")
            time.sleep(1.5)
            hablar("No tengo ninguna configuracion para poder entablar una conversacion todavia")

        elif ("dime la hora" in consulta)  and (bandera==True):
            hora = datetime.datetime.now().strftime("%H")
            minutos = datetime.datetime.now().strftime("%M")
            hora_Int = int(hora)
            if hora_Int >=1 and hora_Int < 7:
                print(f"La hora es {hora} con {minutos} minutos de la madrugada")
                hablar(f"La hora es {hora} con {minutos} minutos de la madrugada")
                
            elif hora_Int >= 7 and hora_Int < 12:
                print(f"La hora es {hora} con {minutos} minutos de la mañana")
                hablar(f"La hora es {hora} con {minutos} minutos de la mañana")
                
            elif hora_Int >= 12 and hora_Int < 20:
                hora_Int=hora_Int-12
                print(f"La hora es {hora_Int} con {minutos} minutos de la tarde")
                hablar(f"La hora es {hora_Int} con {minutos} minutos de la tarde")
                
            elif hora_Int >= 20 and hora_Int <24:
                hora_Int=hora_Int-12
                print(f"La hora es {hora_Int} con {minutos} minutos de la noche")
                hablar(f"La hora es {hora_Int} con {minutos} minutos de la noche")        

        elif ("qué hora es" in consulta) and (bandera==True):
            hora = datetime.datetime.now().strftime("%H")
            minutos = datetime.datetime.now().strftime("%M")
            hora_Int = int(hora)
            if hora_Int >=1 and hora_Int < 7:
                print(f"La hora es {hora} con {minutos} minutos de la madrugada")
                hablar(f"La hora es {hora} con {minutos} minutos de la madrugada")
                
            elif hora_Int >= 7 and hora_Int < 12:
                print(f"La hora es {hora} con {minutos} minutos de la mañana")
                hablar(f"La hora es {hora} con {minutos} minutos de la mañana")
                
            elif hora_Int >= 12 and hora_Int < 20:
                hora_Int=hora_Int-12
                print(f"La hora es {hora_Int} con {minutos} minutos de la tarde")
                hablar(f"La hora es {hora_Int} con {minutos} minutos de la tarde")
                
            elif hora_Int >= 20 and hora_Int <24:
                hora_Int=hora_Int-12
                print(f"La hora es {hora_Int} con {minutos} minutos de la noche")
                hablar(f"La hora es {hora_Int} con {minutos} minutos de la noche") 
                
        elif ("hoy es" in consulta) and (bandera==True):
            dia = datetime.datetime.now().strftime("%d")
            print(f"hoy es dia {int(dia)}")
            hablar(f"hoy es dia {int(dia)}")
            
        elif ("qué día es hoy" in consulta) and (bandera==True):
            dia = datetime.datetime.now().strftime("%d")
            meses = ["Enero", "Febrero", "Marzo", "Abril",
              "Mayo", "Junio", "Julio", "Agosto",
               "Septiembre", "Octubre", "Noviembre",
                "Diciembre"]
            mes = meses[int(datetime.datetime.now().strftime("%m")) -1 ]
            print(f"Hoy es {dia} de {mes}") 
            hablar(f"Hoy es {dia} de {mes}")  
            
        elif ("año" in consulta) and (bandera==True):
            anno = datetime.datetime.now().strftime("%Y")
            print(f"Estamos en el año {anno}")
            hablar(f"Estamos en el año {anno}")

        elif ("hola" in consulta) and (bandera==True):
            hablar("hola")
            saludo()
        
        # elif ("pon música" in consulta) and (bandera==True):
        #     process_3=multiprocessing.Process(target= play.main)
        #     process_3.start()

        # elif ("cambia música" in consulta) and (bandera==True): 
        #     play.main()

        # elif ("detener música" in consulta) and (bandera==True):

        #     ti = 0
        #     name = 'AIMP.exe'
        #     f = wmi.WMI() 
        #     print("Cerrando.....")
        #     for process in f.Win32_Process(): 
        #         if process.name == name: 
        #             process.Terminate() 
        #             ti += 1       
        
        cont+=1

def saludo():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        hablar("Buenos dias")

    elif hour>=12 and hour<18:
        hablar("Buenas tardes")

    else:
        hablar("Buenas noches")

# def main():

#     print("Activado...")
#     lord_comander()

lord_comander()
    
        
   
# -----------------------------------------------------------------------
# -------------------------------The End---------------------------------
# -----------------------------------------------------------------------




                
    
