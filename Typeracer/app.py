# app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_race', methods=['POST'])
def start_race():
    user_id = request.json.get('userId')
    # Start race logic here
    # Send real-time updates to clients
    emit('race_started', {'message': 'Race started!'}, broadcast=True)
    return jsonify({'success': True})

if __name__ == '__main__':
    socketio.run(app)
