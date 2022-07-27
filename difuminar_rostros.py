# DIfuminar rostros
import cv2
import mediapipe as mp


def face_detection():
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

        if results.detections:
            for detection in results.detections:
                # mp.solutions.drawing_utils.draw_detection(imagen,detection)
                difuminar(imagen,detection,alto,ancho)

        cv2.imshow("imagen",imagen)
        if cv2.waitKey(1)==27:break

def difuminar(imagen,detection,alto,ancho):
    bbox = detection.location_data.relative_bounding_box

    y0=int(bbox.ymin*alto)
    y1=y0 + int(bbox.height*alto)

    x0=int(bbox.xmin*ancho)
    x1=x0 + int(bbox.width*ancho)

    # difuminar
    imagen[y0:y1,x0:x1]=cv2.blur(imagen[y0:y1,x0:x1],(100,150))

    # difuminar
    # imagen[y0:y1,x0:x1]=cv2.GaussianBlur(imagen[y0:y1,x0:x1],(191,191),0)
    
face_detection()