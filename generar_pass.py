# import numbers
import random

def generar_pass(len:int):
    lower = "abcdefghijkmnñopqrstvwxyz"
    upper = "ABCDEFGHIJKLMNÑOPQRSTVWXYZ"
    numbers = "0123456789"
    symbols = "[]}{()!$%&/=?¿¡._-:,;"

    all = lower + upper + numbers + symbols
    len = 20
    password = "".join(random.sample(all,len))
    
    print (password)

generar_pass(8)
