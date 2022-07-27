from email.mime import image
import mediapipe as mp
import cv2

# Deteccion de rostros con mediapipe
def face_detection():
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

# Deteccion de rostros con mediapipe usando metodos externos
def face_detection_2():
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
                
                # mp.solutions.drawing_utils.draw_detection(imagen,detection)
                draw_rectangulo_detection(imagen,detection,alto,ancho)
                draw_detection(imagen,detection,alto,ancho)
                cv2.putText(imagen,"rostro_"+str(cont),(int(bbox.xmin*ancho),int(bbox.ymin*alto)-15),cv2.FONT_HERSHEY_SIMPLEX,0.7,(208,151,12),2)
                
                cont+=1
        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1)==27:break


def draw_rectangulo_detection(imagen,detection,alto,ancho):
    bbox = detection.location_data.relative_bounding_box
    

    y0=int(bbox.ymin*alto)
    y1=y0 + int(bbox.height*alto)

    x0=int(bbox.xmin*ancho)
    x1=x0 + int(bbox.width*ancho)

    cv2.rectangle(imagen,(x0,y0),(x1,y1),(208,151,12),1)
    

def draw_detection(imagen,detection,alto,ancho):
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
    


face_detection()


