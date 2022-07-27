"""Un chatBot Basico"""

from nltk.chat.util import Chat,reflections

mis_reflexiones= {
    "ir":"fui",
    "hola":"hey"
}

pares= [
    [
        r"mi nombre es (.*)",
        ["Hola %1, como estas?"]
    ],
    [
        r"Cual es tu nombre?",
        ["Mi nombre es chatBot"]
    ],
    [
        r"Quien eres?",
        ["Soy tu padre"]
    ],
    [
        r"Que haces?",
        ["Nada...solo procesando unos datos"]
    ]
]

def chatear():
    print("Hola")
    chat=Chat(pares,mis_reflexiones)
    chat.converse()

if __name__=="__main__":
    chatear()

