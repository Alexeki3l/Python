"""
Muestra todos los microfonos de la PC
"""
import speech_recognition as sr

for elementos in sr.Microphone.list_microphone_names():
    print(elementos)