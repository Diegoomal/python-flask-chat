from . import app, illm, agent
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

        if 'run-agent' in user_message:
            response = agent.invoke(user_message)
            return jsonify({'response': response['output']})
        else:
            response = illm.invoke(user_message)
            return jsonify({'response': response})

asgi_app = WsgiToAsgi(app)
