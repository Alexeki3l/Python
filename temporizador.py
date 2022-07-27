import time

def contador(t):
    t = int(t)
    while t:
        min,seg=divmod(t,60)
        timer="{:02d}:{:02d}".format(min,seg)
        print(timer,end="\r")
        time.sleep(1)
        t-=1
    print("El tiempo se ha acabado")

t = input("Entre el tiempo en segundos:  ")
contador(t)