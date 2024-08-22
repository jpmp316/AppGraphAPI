import requests
import datetime
import json
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola, Mundo!'

@app.route('/about')
def about():
    return 'Acerca de mí'

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/api/posts', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    image = request.files['image']
    fecha = request.form['datetime']
    page_id = "115199898165986"
    access_token = 'EAALCMus5D6gBO9GKZCtoZA7wC7SwaQZBI5FTh3ZCjC0TDmNJr1KfF4WW5K6r2eFrZBFxguNmfJIJE2NT9qF2SsOyoDHDmZC2dbxuIWAY9TYaENZBYAzlCZCZAyNIEvTbS5VC98Lhyxcexqq4EenJDWdG3MLxjr1K5ajpZBoOqA4H7BZA8vayjCSCDeOlnkJSf7f8pkZD'
    
    if fecha:
        # Convertir la fecha a un timestamp
        scheduled_time = int(datetime.datetime.strptime(fecha, "%Y-%m-%dT%H:%M").timestamp())

        if image:
            # Subir la imagen a Facebook sin publicarla de inmediato
            image_filename = image.filename
            image.save(image_filename)
            img_file = open(image_filename, 'rb')
            photo_payload = {
                'published': 'false',
                'access_token': access_token,
            }
            files = {
                'source': (image_filename, img_file)
            }
            photo_response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/photos", data=photo_payload, files=files)
            img_file.close()

            if photo_response.status_code != 200:
                return f"Error al subir la imagen: {photo_response.status_code}\n{photo_response.json()}"

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
            # Programar la publicación solo con el mensaje y titulo
            post_payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
                'scheduled_publish_time': scheduled_time,
                'published': 'false',
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/feed", data=post_payload)

        if response.status_code == 200:
            return "Post programado con exito!"
        else:
            return f"Error al programar post: {response.status_code}\n{response.json()}"

    else:
        if image:
            # Publicar inmediatamente con imagen
            image_filename = image.filename
            image.save(image_filename)
            img_file = open(image_filename, 'rb')
            payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
            }
            files = {
                'source': (image_filename, img_file)
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/photos", data=payload, files=files)
            img_file.close()
        else:
            # Publicar inmediatamente sin imagen
            payload = {
                'message': f"{name}\n\n{message}",
                'access_token': access_token,
            }
            response = requests.post(f"https://graph.facebook.com/v20.0/{page_id}/feed", data=payload)

        if response.status_code == 200:
            return "Post realizado correctamente"
        else:
            return f"Failed to post: {response.status_code}\n{response.json()}"


if __name__ == '__main__':
    app.run(debug=True)