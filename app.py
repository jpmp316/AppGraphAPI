import requests
import datetime
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')



@app.route('/api/posts', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    message = data.get('message')
    image_url = data.get('image_url')
    fecha = data.get('datetime')
    page_id = "115199898165986"
    access_token = 'EAALCMus5D6gBO9GKZCtoZA7wC7SwaQZBI5FTh3ZCjC0TDmNJr1KfF4WW5K6r2eFrZBFxguNmfJIJE2NT9qF2SsOyoDHDmZC2dbxuIWAY9TYaENZBYAzlCZCZAyNIEvTbS5VC98Lhyxcexqq4EenJDWdG3MLxjr1K5ajpZBoOqA4H7BZA8vayjCSCDeOlnkJSf7f8pkZD'

    if fecha:
        # Convertir la fecha a un timestamp
        scheduled_time = int(datetime.datetime.strptime(fecha, "%Y-%m-%dT%H:%M").timestamp())

        if image_url:
            # Subir la imagen a Facebook sin publicarla de inmediato
            photo_payload = {
                'url': image_url,
                'published': 'false',
                'access_token': access_token,
            }
            photo_response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/photos", data=photo_payload)

            if photo_response.status_code != 200:
                return jsonify({"error": f"Error al subir la imagen: {photo_response.status_code}", "details": photo_response.json()}), photo_response.status_code

            # Obtener el ID de la imagen subida
            photo_id = photo_response.json().get('id')

            # Programar la publicación con la imagen
            post_payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
                'published': 'false',
                'attached_media': json.dumps([{'media_fbid': photo_id}]),
                'scheduled_publish_time': scheduled_time,
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/feed", data=post_payload)
        else:
            # Programar la publicación solo con el mensaje y título
            post_payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
                'scheduled_publish_time': scheduled_time,
                'published': 'false',
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/feed", data=post_payload)

        if response.status_code == 200:
            return jsonify({"message": "Post programado con éxito!"})
        else:
            return jsonify({"error": f"Error al programar post: {response.status_code}", "details": response.json()}), response.status_code

    else:
        if image_url:
            # Publicar inmediatamente con imagen
            payload = {
                'url': image_url,
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/photos", data=payload)
        else:
            # Publicar inmediatamente sin imagen
            payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/feed", data=payload)

        if response.status_code == 200:
            return jsonify({"message": "Post realizado correctamente"})
        else:
            return jsonify({"error": f"Failed to post: {response.status_code}", "details": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
