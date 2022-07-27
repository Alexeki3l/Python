
"""
Trabajando en gestos de la cara y reconocimiento de sentimiento a traves de la 
libreria de python Mediapipe-FaceMesh.
   NOTA: La sonriza es lo unico que esta validado
"""

from json import detect_encoding
import cv2
import mediapipe as mp
import math
import numpy as np

def feeling():
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # with mp_face_mesh.FaceMesh(
    #     static_image_mode=False,
    #     max_num_faces=1,
    #     min_detection_confidence=0.5) as face_mesh:

# Esta linea es mas exacta los ptos con el movimiento
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        while True:

            ret, frame = cap.read()
            if ret == False:
                break

            frame = cv2.flip(frame,1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            alto,ancho,_ = frame.shape

            
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:

                     
                     # mp_drawing.draw_landmarks(frame, face_landmarks,
                     #     mp_face_mesh.FACEMESH_CONTOURS,
                     #     mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                     #     mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1)) 
                  
                     """Pintar los puntos de la malla sin las conecciones"""
                     # for landmark in face_landmarks.landmark:
                     #     x = landmark.x
                     #     y = landmark.y

                     #     shape = frame.shape 
                     #     relative_x = int(x * shape[1])
                     #     relative_y = int(y * shape[0])

                     #     cv2.circle(frame, (relative_x, relative_y), radius=1, color=(225, 0, 100), thickness=1)

                     """Trabajar con los puntos en especificos de la cara"""
                     shape = frame.shape 
                     # --------------------Punta de la nariz-------------------------
                     x1= int(face_landmarks.landmark[1].x * shape[1])
                     y1=int(face_landmarks.landmark[1].y * shape[0])
                     z1=face_landmarks.landmark[1].z * 100
                     cv2.circle(frame, (x1,y1), 2, color=(225, 0, 100), thickness=2)
                     # print(""+str(z1))

                     # ------------------------BOCA------------------------------------
                     # Punta labio superior
                     x13= int(face_landmarks.landmark[13].x * shape[1])
                     y13=int(face_landmarks.landmark[13].y * shape[0])
                     cv2.circle(frame, (x13,y13), 2, color=(225, 0, 100), thickness=2)
                     # z13=face_landmarks.landmark[13].z * 100
                     # print("El numero es "+str(z13))
                
                     #--------------------Punta labio inferior-----------------------
                     x14= int(face_landmarks.landmark[14].x * shape[1])
                     y14=int(face_landmarks.landmark[14].y * shape[0])
                     cv2.circle(frame, (x14,y14), 2, color=(225, 0, 100), thickness=2)

                     # ---------------------------------------------------------------
                     # -------------Punta extremo izquierdo de la boca---------------
                     x61= int(face_landmarks.landmark[61].x * shape[1])
                     y61=int(face_landmarks.landmark[61].y * shape[0])
                     cv2.circle(frame, (x61,y61), 2, color=(225, 0, 100), thickness=2)
                
                     # --------------Punta extremo derecho de la boca------------------
                     x291= int(face_landmarks.landmark[291].x * shape[1])
                     y291=int(face_landmarks.landmark[291].y * shape[0])
                     cv2.circle(frame, (x291,y291), 2, color=(225, 0, 100), thickness=2)
                     # ------------------------------------------------------------------

                     # -------------------------OJO IZQUIERDO----------------------------
                     # ----------------------Extremo ojo izquierdo-----------------------
                     x143= int(face_landmarks.landmark[143].x * shape[1])
                     y143=int(face_landmarks.landmark[143].y * shape[0])
                     cv2.circle(frame, (x143,y143), 2, color=(225, 0, 100), thickness=2)
                     # ------------------------Pto en las cejas inferior----------------------
                     x52= int(face_landmarks.landmark[52].x * shape[1])
                     y52=int(face_landmarks.landmark[52].y * shape[0])
                     cv2.circle(frame, (x52,y52), 2, color=(225, 0, 100), thickness=2)
                     # --------------------Pto superior en el ojo---------------------------
                     x159= int(face_landmarks.landmark[159].x * shape[1])
                     y159=int(face_landmarks.landmark[159].y * shape[0])
                     cv2.circle(frame, (x159,y159), 2, color=(225, 0, 100), thickness=2)
                     # ----------------------------------------------------------------------

                     # -------------------------OJO DERECHO-----------------------------------
                     #  ------------------------Pto en las cejas inferior----------------------
                     x282= int(face_landmarks.landmark[282].x * shape[1])
                     y282=int(face_landmarks.landmark[282].y * shape[0])
                     cv2.circle(frame, (x282,y282), 2, color=(225, 0, 100), thickness=2)
                     #--------------------- Extremo ojo derecho-------------------------------
                     x372= int(face_landmarks.landmark[372].x * shape[1])
                     y372=int(face_landmarks.landmark[372].y * shape[0])
                     cv2.circle(frame, (x372,y372), 2, color=(225, 0, 100), thickness=2)
                     #---------------- Pto parte superior del ojo derecho----------------------
                     x386= int(face_landmarks.landmark[386].x * shape[1])
                     y386=int(face_landmarks.landmark[386].y * shape[0])
                     cv2.circle(frame, (x386,y386), 2, color=(225, 0, 100), thickness=2)
                     # -----------------------------------------------------------------------------


                     # --------------------------Midiendo longitudes---------------------------------
                     # -------------------BOCA-----------------------------
                     longitud1= math.hypot(x14-x13, y14-y13)
                     longitud2= math.hypot(x291-x61, y291-y61)
                     # ----------------BOCA A OJOS--------------------
                     longitud3= math.hypot(x372-x291, y372-y291)
                     longitud4= math.hypot(x143-x61, y143-y61)
                     # ---------------OJOS A CEJAS------------------
                     longitud5= math.hypot((x159-x52), y159-y52)
                     longitud6= math.hypot((x386-x282), y386-y282)


                     cv2.line(frame,(x13,y13),(x14,y14),(0,0,0),1)
                     # cv2.putText(frame, ""+str(longitud1),(x13,y13+110),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                     cv2.line(frame,(x61,y61),(x291,y291),(0,0,0),1)
                     # cv2.putText(frame, ""+str(longitud2),(x291,y291+35),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                     cv2.line(frame,(x291,y291),(x372,y372),(0,0,0),1)
                     # cv2.putText(frame, ""+str(longitud3),(x372,y372),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                     cv2.line(frame,(x61,y61),(x143,y143),(0,0,0),1)

                     cv2.line(frame,(x52,y52),(x159,y159),(0,0,0),1)
                     # cv2.putText(frame, ""+str(longitud5),(x159,y159+50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                     cv2.line(frame,(x386,y386),(x282,y282),(0,0,0),1)
                     # cv2.putText(frame, ""+str(longitud6),(x282,y282-50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)


                     # cv2.putText(frame, ""+str(z1),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

                     """
                     longitud1 ==> Es el alto de la boca
                     longitud2 ==> Es el ancho de la boca
                     longitud3 ==> Es la distancia del extremo derecho de boca a un pto del extremo derecho de ojo derecho
                       z1 ==> Es el pto 1 que se encuentra en la punta de la nariz

                     """
                     """---------------------------------------------------------------------------------------------------
                     -----------------------------------Validando la sonrisa-----------------------------------------------
                      ------------------------------------------------------------------------------------------------------
                    """

                     if (((longitud1 >=19 and longitud1 <=25) and (longitud2>=95 and longitud2<=117) and (longitud3<=110 and longitud3>=94) and (z1>=-9 and z1<=-7))
                         or ((longitud1 >=13) and (longitud2>=80) and (longitud3<=100) and (z1>=-8 and z1<=-6))
                         or ((longitud1 >=8) and (longitud2>=69) and (longitud3<=89) and (z1>=-7 and z1<=-5))
                         or ((longitud1 >=5 and longitud1<=25) and (longitud2>=60) and (longitud3<=78) and (z1>=-6 and z1<=-4))
                         or ((longitud1 >=5 and longitud1<=12) and (longitud2>=52 and longitud2<=60) and (longitud3<=67) and (z1>=-5 and z1<=-3))
                         or ((longitud1 >=4 and longitud1 <=15) and (longitud2>=36 and longitud2<=50) and (longitud3<=50 and longitud3 >= 44) and (z1>=-4 and z1<=-2))
                         or ((longitud1 >=3) and (longitud2>=25) and (longitud3<=31) and (z1>=-3 and z1<=-1))):
                        cv2.putText(frame, "Estas sonriendo",(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                        
                     """-------------------------------------------------------------------------------------------------------------------------"""
        

            cv2.imshow("Vision Humana", frame)
            # cv2.imshow("Vision Machine", imBlack)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        
    cap.release()
    cv2.destroyAllWindows()

feeling()

