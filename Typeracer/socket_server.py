# socket_server.py
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Additional connection handling (e.g., user authentication)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Additional disconnection handling

if __name__ == '__main__':
    socketio.run(app, port=5001)
