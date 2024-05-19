from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from blockchain import Blockchain
import os

app = Flask(__name__, static_url_path='', static_folder='static')
socketio = SocketIO(app)

# Inicjalizacja blockchaina
blockchain = Blockchain()

# Endpoint do dodawania bloków
@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json['data']
    blockchain.add_block(data)
    response = {
        'message': 'Block added',
        'block': vars(blockchain.get_latest_block())
    }
    return jsonify(response), 200

# Endpoint do pobierania całego łańcucha
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [vars(block) for block in blockchain.chain]
    response = {
        'chain': chain_data,
        'length': len(chain_data)
    }
    return jsonify(response), 200

# Endpoint do wykonywania transakcji
@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.json['data']
    blockchain.add_block(data)
    response = {
        'message': 'Transaction successful',
        'block': vars(blockchain.get_latest_block())
    }
    return jsonify(response), 200

# Endpoint do pobierania stanu portfela
@app.route('/wallet/<address>', methods=['GET'])
def get_wallet(address):
    balance = sum(1 for block in blockchain.chain if block.data == address)
    response = {
        'address': address,
        'balance': balance
    }
    return jsonify(response), 200

# Endpoint do serwowania strony głównej
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# SocketIO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'message': 'Connected to the server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, port=5000)
