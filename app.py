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
    payload = {
        'message': f"{name}\n\n{message}",
        'access_token':'EAAR4ZCnOHpb0BO6gbbopGV8uPnsUEpXM85zti9H5uFSW1UKG1uFJwyMfkfbZB9Q5T2YF316IXH5JbFwy7altN8KikzRQmn4vrg4e0aagNf9JNdcb2cjJDqBKDgyM4oHaFRBSfCXjfVXDAxCeMolHgRGrRZAZCZBf8ZAgSbpWipfk7vcYRbctMARjJfKt18OniEiT1vOIJ1snkaocKhArvBo1Kz',
        'published': True  # Este parámetro asegura que la publicación sea visible públicamente
        
    }
   
    page_id = "363272963543755"
    url = f"https://graph.facebook.com/v20.0/{page_id}/feed"

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return "Post published successfully!"
    else:
        return f"Failed to publish post: {response.status_code}\n{response.json()}"
    # Procesamiento adicional...
    


if __name__ == '__main__':
    app.run(debug=True)