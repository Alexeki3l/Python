from random import *
import time

# Crear una variable que guardara el pass
user_pass = input ("Entre su contraseña >>>  ")

# almacenar letras del alfabeto para usarlas para descifrar contraseñas
password = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
 "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
# una variable string vacia
guess = ""
# usar un "while" para generar muchos password y comprararlo con que se entro
tiempo = time.sleep(0.1)
while (guess != user_pass):
    guess = ""
    
    # generando una contraseña random usando el "for"
    for letter in range(len(user_pass)):
        guess_letter = password[randint(0, 35)]
        guess = str(guess_letter) +str(guess)
    # Imprimiendo el pass adivinado
    print(guess)

# imprimiendo el pass 
print("Tu password es ",guess)