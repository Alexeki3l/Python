"""
Ordena todos los archivos que estan en mis Descargas
"""

from pickletools import optimize
from pydoc import doc
from PIL import Image
import shutil

import os
# os. mkdir()
# os.path.join
carpeta_descarga = "C:/Users/Keidy/Downloads/"

if __name__ == "__main__":

    print("Ordenando archivos...")

    for filename in os.listdir(carpeta_descarga):
        name, extension = os.path.splitext(carpeta_descarga + filename)
        
        imagen      = carpeta_descarga + "Imagenes"
        video       = carpeta_descarga + "Video"
        docs        = carpeta_descarga + "Documentos"
        music       = carpeta_descarga + "Musica"
        instalador  = carpeta_descarga + "Instaladores"
        rar         = carpeta_descarga + "Comprimidos"

        # Ordenar Imagenes
        if extension in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            if not os.path.exists(imagen):
                os.mkdir(imagen)
            try:
                shutil.move(carpeta_descarga + filename, imagen)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break

        # Ordenar Videos
        if extension in [".mp4",".avi",".webm"]:
            if not os.path.exists(video):
                os.mkdir(video)
            try:
                shutil.move(carpeta_descarga + filename, video)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break
        
        # Ordenar Musica
        if extension in [".mp3"]:
            if not os.path.exists(music):
                os.mkdir(music)
            try:
                shutil.move(carpeta_descarga + filename, music)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break
        
        # Ordenar Documentos
        if extension in [".doc",".docx",".pdf",".xls",".ppt",".txt",".rtf",".odt",".xlsx",".ods",".DOC",".pptx",".PDF"]:
            if not os.path.exists(docs):
                os.mkdir(docs)
            try:
                shutil.move(carpeta_descarga + filename, docs)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break
        
        # Ordenar Ejecutables
        if extension in [".exe",".whl",".msi",".iso",".apk",".dll",".run"]:
            if not os.path.exists(instalador):
                os.mkdir(instalador)
            try:
                shutil.move(carpeta_descarga + filename, instalador)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break

        if extension in [".rar",".zip",".tar",".win64",".gz"]:
            if not os.path.exists(rar):
                os.mkdir(rar)
            try:
                shutil.move(carpeta_descarga + filename, rar)
                print(carpeta_descarga + filename)
            except:
                print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                break
    
    if len(os.listdir(carpeta_descarga)) > 6:

        more = carpeta_descarga + "More"

        if not os.path.exists(more):
            os.mkdir(more)

        for filename in os.listdir(carpeta_descarga):

                try:
                    if not filename in ["Comprimidos","Documentos","Instaladores","Video","Musica","Imagenes","More"]:
                        print("Ordenando carpetas sueltas y archivos extraño...")
                        shutil.move(carpeta_descarga + filename, more)
                 
                except:
                    print("Ha ocurrido un error. Asegurese que no esta siendo utilizado el archivo con nombre: {}".format(filename))
                    break
        
        

      
        