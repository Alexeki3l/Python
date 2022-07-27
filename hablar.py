import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', 'spanish')
engine.setProperty('volume', 1)




# It's just a text to speech function..
def saySomething(somethingToSay):
   engine.say(somethingToSay)
   engine.runAndWait()


   while True:
       something = input("Something to say? ")
       print("Saying something with speakers..")
       saySomething(something)


   # ------------------------------------------------------------------------

# from gtts import gTTS
# import os


#    # It's just a text to speech function..
# def saySomething(somethingToSay):
#    myobj = gTTS(text=somethingToSay, lang="es", slow=False)
#    myobj.save("somethingToSay.mp3")
#    os.system("mpg321 somethingToSay.mp3")


#    while True:
#       something = input("Something to say? ")
#       print("Saying something with speakers..")
#       saySomething(something)