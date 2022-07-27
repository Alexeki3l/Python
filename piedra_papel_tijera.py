from random import *

def piepati():
   puntos = 0
   vidas = 0
   while vidas != 3:  
     opcion = input("Elija su opcion (piedra, papel o tijrera) >>>  ")
     opcion_generada = choice(["piedra","papel","tijera"])
     if  opcion == "piedra":
        if opcion_generada == "tijera":
            vidas += 1
            print("Usted ha ganado")
            puntos += 1  
        elif opcion_generada == "papel":
            vidas += 1
            print("Usted ha perdido")     
        else: 
            # vidas += 1
            print("Ha ocurrido un empate")

     if  opcion == "tijera":
        if opcion_generada == "papel":
            vidas += 1
            print("Usted ha ganado")
            puntos += 1
        elif opcion_generada == "piedra":
            vidas += 1
            print("Usted ha perdido")
        else: 
            # vidas += 1
            print("Ha ocurrido un empate") 

     if  opcion == "papel":
        if opcion_generada == "piedra":
            vidas += 1
            print("Usted ha ganado")
            puntos += 1  
        elif opcion_generada == "tijera":
            vidas += 1
            print("Usted ha perdido")
        else: 
            # vidas += 1
            print("Ha ocurrido un empate")  

   if  puntos >= 2:
    print(f"Se acabo la ronda. Usted ha ganado con {puntos} puntos")
    opcion = input("Desea empezar de nuevo?:  ")
    if opcion == "si":
        piepati()  
   else:
    print(f"Se acabo la ronda. Usted perdio con {puntos} puntos")
    opcion = input("Desea empezar de nuevo?:  ")
    if opcion == "si":
        piepati()  


piepati()