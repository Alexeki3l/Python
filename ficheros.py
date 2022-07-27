from os import remove

# Crea un fichero vacio
def crear_archivo(nombre_archivo):
    try:
        file = open(nombre_archivo,"x")
        print(f"Se ha creado un archivo de nombre {nombre_archivo}")
    except:
        print("Ya existe un archivo con ese nombre ")
        nombre = input("Entra el nombre del archivo >> ")
        crear_archivo(nombre)

# Escribe un mensaje en el fichero
def escribe_archivo(nombre_archivo):
    mensaje  = input("Escribe en el fichero >>>  ")
    with open(nombre_archivo, 'a') as fichero:
        fichero.write(mensaje + "\n")

# Leer el mensaje del fichero        
def lee_archivo(nombre_archivo):
    mensaje = ""
    with open(nombre_archivo, 'r') as fichero:
        mensaje = fichero.read()
    # Borra el contenido del fichero para dejarlo vacío
    # f = open('archivo.txt', 'w')
    fichero.close()
    return print(mensaje)

# Borra el mensaje del fichero
def vaciar_archivo(nombre_archivo):
    opcion = input(f"Desea borrar el vaciar el contenido del archivo {nombre_archivo}? SI / NO >>> ")
    opciones_si = ["SI","Si","si"]
    opciones_no = ["NO","No","no"]
    if opcion in opciones_si:
        with open(nombre_archivo,"w") as file:
            file.close()
            print("Se ha vaciado este archivo")
    elif opcion in opciones_no:  
        file = open(nombre_archivo,"r")
        file.close()  
    else:
        print("Se espera una respuesta de Si/No")
        vaciar_archivo(nombre_archivo)

# Elimina el fichero   
def eliminar_archivo(nombre_archivo):
    opcion = input("Desea borrar el archivo? SI / NO >>> ")
    opciones_si = ["SI","Si","si"]
    opciones_no = ["NO","No","no"]
    if opcion in opciones_si:
        remove(nombre_archivo)
        print("Se elimino el archivo")
    elif opcion in opciones_no:
        with open (nombre_archivo) as file:
            file.close()
    else:
        print("Se espera una opcion de SI / No")
        eliminar_archivo(nombre_archivo)
    

# crear_archivo("ejemplo.txt")
# escribe_archivo("ejemplo.txt")
# lee_archivo("ejemplo.txt")
# vaciar_archivo("ejemplo.txt")
# eliminar_archivo("ejemplo.txt")
print(dir())
  