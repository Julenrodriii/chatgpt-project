# Líneas 1-7: Importamos todas las herramientas que necesitamos
import os
import sys
import time
import threading
from dotenv import load_dotenv
import openai
from datetime import datetime

# Línea 10: Cargamos la clave secreta del archivo .env
load_dotenv()

# Líneas 13-14: Obtenemos la clave secreta
api_key = os.getenv("OPENAI_API_KEY")

# Líneas 16-18: Comprobamos si tenemos la clave secreta
if not api_key:
    print("Error: No se encontró la API key en el archivo .env")
    sys.exit(1)

# Línea 20: Le damos la clave secreta a la herramienta de OpenAI
openai.api_key = api_key

# Línea 22: Creamos una variable para controlar la animación de "pensando"
thinking = False

# Líneas 24-31: Función para hacer la animación de "pensando"
def animate_thinking():
    global thinking
    animation = "|/-\\"
    idx = 0
    while thinking:
        print(f"\rPensando {animation[idx % len(animation)]}", end="", flush=True)
        idx += 1
        time.sleep(0.1)

# Líneas 33-55: Función para hablar con ChatGPT
def get_chatgpt_response(prompt):
    global thinking
    thinking = True
    animation_thread = threading.Thread(target=animate_thinking)
    animation_thread.start()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        result = "Error de autenticación: La API key no es válida."
    except Exception as e:
        result = f"An error occurred: {str(e)}"
    finally:
        thinking = False
        animation_thread.join()
        print("\r", end="", flush=True)  # Clear the thinking animation
    
    return result

# Líneas 57-58: Función para obtener la fecha y hora actual
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Línea 60: Mensaje de bienvenida
print("Bienvenido al chat con GPT. Escribe 'salir' para terminar.")

# Líneas 62-70: Bucle principal del chat
while True:
    user_input = input(f"\n[{get_timestamp()}] Tú: ")
    if user_input.lower() == 'salir':
        print("¡Hasta luego!")
        break
    
    response = get_chatgpt_response(user_input)
    print(f"\n[{get_timestamp()}] GPT: {response}")