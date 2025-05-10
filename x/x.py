import cv2
import requests
import json

def capturar_foto():
    """Captura una foto desde la cámara web."""
    cap = cv2.VideoCapture(0)  # 0 suele ser la cámara predeterminada

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return None

    ret, frame = cap.read()

    if not ret:
        print("No se pudo capturar la imagen.")
        cap.release()
        return None

    cap.release()
    return frame

def enviar_a_faceplusplus(imagen_path, api_url, api_key, api_secret):
    """Envía la imagen a la API de Face++."""
    try:
        with open(imagen_path, 'rb') as imagen_file:
            files = {'image_file': imagen_file}
            data = {
                'api_key': api_key,
                'api_secret': api_secret
            }

            response = requests.post(api_url, data=data, files=files)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con la API: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {imagen_path}")
        return None

def procesar_respuesta(response_json):
    """Procesa la respuesta JSON de Face++ para detectar rostros."""
    if response_json and 'faces' in response_json:
        if len(response_json['faces']) > 0:
            print(f"¡Se detectó {len(response_json['faces'])} rostro(s) en la imagen!")
            return True
        else:
            print("No se detectaron rostros.")
            return False
    else:
        print("La respuesta de la API no tiene el formato esperado.")
        return False

if __name__ == "__main__":
    nombre_archivo = "foto.jpg"
    frame = capturar_foto()

    if frame is not None:
        cv2.imwrite(nombre_archivo, frame)
        print(f"Foto guardada como {nombre_archivo}")

        # Configura la URL y tus credenciales de Face++
        api_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
        api_key = "tZYtBaz06WTwv97ujkCYNHPFxE8KC-7d"
        api_secret = "F7njkd71cwuqpa1AmBH8wWaxKHGrITHL"

        resultado_api = enviar_a_faceplusplus(nombre_archivo, api_url, api_key, api_secret)

        if resultado_api:
            procesar_respuesta(resultado_api)
    else:
        print("No se pudo continuar.")