import random
import requests
import json
import qrcode
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')


def obtener_palabra():
    palabras = ["python", "programacion", "computadora", "juego", "ahorcado"]
    return random.choice(palabras)


def dibujar_ahorcado(intentos):
    if intentos == 6:
        print(" _____")
        print("|     |")
        print("|")
        print("|")
        print("|")
        print("|")
    elif intentos == 5:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|")
        print("|")
        print("|")
    elif intentos == 4:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|     |")
        print("|")
        print("|")
    elif intentos == 3:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|    /|")
        print("|")
        print("|")
    elif intentos == 2:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|    /|\\")
        print("|")
        print("|")
    elif intentos == 1:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|    /|\\")
        print("|    /")
        print("|")
    else:
        print(" _____")
        print("|     |")
        print("|     O")
        print("|    /|\\")
        print("|    / \\")
        print("|")


def jugar():
    palabra = obtener_palabra()
    palabra_secreta = ["_"] * len(palabra)
    intentos = 6
    letras_usadas = []

    print("Bienvenido al juego del ahorcado!")
    while True:
        print(" ".join(palabra_secreta))
        print("Intentos restantes: ", intentos)
        letra = input("Ingrese una letra: ").lower()

        if letra in letras_usadas:
            print("Ya has usado esa letra. Intenta otra.")
        else:
            letras_usadas.append(letra)

            if letra in palabra:
                print("¡Correcto!")
                for i in range(len(palabra)):
                    if palabra[i] == letra:
                        palabra_secreta[i] = letra

                if "_" not in palabra_secreta:
                    print("¡Ganaste! La palabra era", palabra)
                    generar_lnurl()
                    break
            else:
                print("Incorrecto.")
                intentos -= 1
                dibujar_ahorcado(intentos)

                if intentos == 0:
                    print("¡Perdiste! La palabra era", palabra)
                    break


def generar_lnurl():
    endpoint = "https://legend.lnbits.com/withdraw/api/v1/links"
    api_key = API_KEY
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

    data = {
        "title": "Premio del Juego del Ahorcado",
        "min_withdrawable": 20,
        "max_withdrawable": 20,
        "uses": 1,
        "wait_time": 1,
        "is_unique": True,
        "webhook_url": ""
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        result = json.loads(response.text)
        lnurl = result["lnurl"]
        print("¡Felicidades, ganaste! Aquí está tu premio de 20 sats:")
        print(lnurl)
        mostrar_premio_en_qr(lnurl)
    else:
        print("Lo siento, hubo un error al generar el link del premio.")
        print("El error devuelto fue: ", response.text)


def mostrar_premio_en_qr(lnurl):
    # crea el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(lnurl)
    qr.make(fit=True)

    # convierte el código QR en imagen
    img = qr.make_image(fill_color="black", back_color="white")

    # muestra la imagen del código QR
    img.show()


jugar()
