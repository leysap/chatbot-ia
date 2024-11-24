from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Obtener la clave API de Mistral desde las variables de entorno
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"  # URL del endpoint correcto

# Verificar si la clave de API está presente
if MISTRAL_API_KEY is None:
    print("ERROR: No se pudo encontrar la clave API en el archivo .env")
else:
    print("Clave API cargada correctamente")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Obtener el mensaje del usuario desde la solicitud JSON
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400  # Validar que el mensaje no esté vacío

    # Obtener los mensajes previos desde el frontend o usar un mensaje vacío por defecto
    messages = request.json.get('messages', [])

    # Construir el payload para la API de Mistral
    payload = {
        "messages": messages + [{"role": "user", "content": user_message}],
        "model": "mistral-tiny"  # Especificamos el modelo a utilizar (ajusta si es necesario)
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Realizamos la solicitud POST a la API de Mistral
        response = requests.post(MISTRAL_URL, json=payload, headers=headers)
        response.raise_for_status()  # Si hay un error, se levantará una excepción

        # Obtener la respuesta de la IA
        ai_response = response.json()
        
        # Extraemos el contenido de la respuesta (ajustado a la estructura de la API)
        answer = ai_response.get('choices', [{}])[0].get('message', {}).get('content', 'No entendí tu mensaje.')

        # Devolver la respuesta al frontend
        return jsonify({"response": answer})
    
    except requests.exceptions.RequestException as e:
        # Manejo de errores en la solicitud
        print(f"Error en la solicitud a Mistral: {e}")
        return jsonify({"error": "Error de conexión con la API de Mistral", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
