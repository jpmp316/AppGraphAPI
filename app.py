import requests
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

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    image = request.files['image']
    page_id = "363272963543755"
    access_token = 'EAAR4ZCnOHpb0BOyZARQXYlict6HMnOqiX2jLrD3BYz9rGqO6ZB2BjkEhByBbnmGeTlcfF4gTxMS6Iz9KKccwLTiC6M3qKc9TcO5qMUccFGx6DRUlBbJmvYiskAGvD9K5mrDBHrS5PzSKIF4n1EjD16yajMqTSc3MWFVOEJZBZCgUAtF9yKZC1BMpNEpssNe2ezNICS76Kf6gGhZAbq0dzqkZBDzI'
    if image:
        image_filename = image.filename
        image.save(image_filename)  # Guarda la imagen temporalmente en el servidor

        # Ahora envía la imagen junto con el mensaje a la Graph API
        payload = {
            'message': f"{name}\n\n{message}",
            'access_token': access_token,
        }
        img_file = open(image_filename, 'rb')
        files = {
            'source': (image_filename, img_file)
        }
            
        url = f"https://graph.facebook.com/v20.0/{page_id}/photos"
        response = requests.post(url, data=payload, files=files)
        img_file.close()  # Cierra el archivo después de la solicitud

    else:
        payload = {
            'message': f"{name}\n\n{message}",
            'access_token':access_token,
            
        }
        url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
        response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return "Post published successfully!"
    else:
        return f"Failed to publish post: {response.status_code}\n{response.json()}"
    # Procesamiento adicional...
    


if __name__ == '__main__':
    app.run(debug=True)