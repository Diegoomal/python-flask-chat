from . import app, illm
from asgiref.wsgi import WsgiToAsgi                                             # type: ignore
from flask import render_template, request, jsonify                             # type: ignore


@app.route('/', methods=['GET'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        user_message = request.json.get('message')
        response = illm.invoke(user_message)
        return jsonify({'response': response})

asgi_app = WsgiToAsgi(app)
