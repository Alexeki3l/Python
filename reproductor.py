from random import random
import playsound as play
import os
from random import randint

lista_reproduction=[]

def direction(path):
    return os.listdir(path)

def add(path):
    lista=os.listdir(path)
    for file in lista:
        if ".mp3" in file:
            lista_reproduction.append(path+"/"+file)
        if not "." in file:
            add(path+"/"+file)
        else:continue
    
def reproducir():
    # add("D:\Alexei-Todo\Musica")
    var=randint(0,len(lista_reproduction))
    os.startfile(lista_reproduction[var])

def main():
    add("D:\Alexei-Todo\Musica")
    reproducir()

main()


    
