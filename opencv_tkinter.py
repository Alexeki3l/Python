# Este script muestra con una seleccion de radio buton que entrada de video tendremos.
# Opcion de buscar el video que queremos mostrar o de mostrar por camara
# -------Imporyat la librearia------------
from tkinter import Button, IntVar, Label, Radiobutton, Tk, Variable, filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
from numpy import size

def video_de_entrada():
    global cap
    if seleccion.get() ==1:
        path_video = filedialog.askopenfilename(filetypes=[
                     ("all video format", ".mp4"),
                     ("all video format", ".avi")])
        if len(path_video)>0:
            botonEnd.config(state="active")
            radio1.config(state="disabled")
            radio2.config(state="disabled")

            # Mostrar ultimos 20 caracteres del video cargado
            pathInputVideo = "...." + path_video[ -23:]
            LblInfoVideoPath.configure(text=pathInputVideo)
            # Iniciar captura de video
            cap = cv2.VideoCapture(path_video)
            visualizar()
    if seleccion.get() ==2:
        botonEnd.config(state="active")
        radio1.config(state="disabled")
        radio2.config(state="disabled")
        LblInfoVideoPath.configure(text="")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        visualizar()

def visualizar():
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame=cv2.flip(frame,1)
        frame = imutils.resize(frame, width =640)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image = im)

        LblVideo.configure(image= image)
        LblVideo.image = image
        LblVideo.after(10,visualizar)
    else:
        LblVideo.image = ""
        LblInfoVideoPath.configure(text="")
        radio1.configure(state="active")        
        radio2.configure(state="active")
        seleccion.set(0)
        botonEnd.configure(state="disabled")
        cap.release()

def finalizar_limpiar():
    LblVideo.image = ""
    LblInfoVideoPath.configure(text="")
    radio1.configure(state="active")
    radio2.configure(state="active")
    seleccion.set(0)
    cap.release()


cap=None
# -------Crear interfaz-----------
root = Tk()
root.geometry("640x650")
LblInfo = Label(root, text="Video de Entrada", font="bold")
LblInfo.grid(column=0, row=0, columnspan=2)
# LblInfo.pack()

# -------Crear los radios button-----------------
# ---Cada vez que se precione el radio button la variable seleccion va tomar los valores de 1 o 2
seleccion = IntVar()
radio1 = Radiobutton(root, text = "Elegir Video", width=40, value=1, variable=seleccion, command=video_de_entrada)
radio2 = Radiobutton(root, text = "Elegir Video", width=40, value=2, variable=seleccion, command=video_de_entrada)
radio1.grid(column=0, row=1)
radio2.grid(column=1, row=1)

# ----Creamos el Label para dejar un espacio.entre los radio button y tambien
# -----------------mostrara el path de los videos leidos-----
LblInfoVideoPath = Label(root, text ="", width = 20)
LblInfoVideoPath.grid(column=0, row=2)
# ----Creamos el Label dnd se mostrara el video-----
LblVideo = Label(root)
LblVideo.grid(column=0, row=3, columnspan=2)

# ----Boton para finalizar el video
botonEnd = Button(root, text="Finalizar video", state= "disabled", command=finalizar_limpiar)
botonEnd.grid(column=0, row=4, columnspan=2, pady=10)
root.mainloop()
