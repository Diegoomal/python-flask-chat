import base64
from . import app, illm, agent, illm_vision
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
        files = request.json.get('files')

        if 'run-agent' in user_message:
            response = agent.invoke(user_message)
            return jsonify({'response': response['output']})
        elif files is not None:
            response = illm_vision.bind(images=[
                str(file['content']).replace('data:image/jpeg;base64,', '') 
                for file in files
            ]).invoke(
                user_message if '' not in user_message else 'descreva a imagem'
            )
            return jsonify({'response': str(response)})
        else:
            response = illm.invoke(user_message)
            return jsonify({'response': response})

asgi_app = WsgiToAsgi(app)
