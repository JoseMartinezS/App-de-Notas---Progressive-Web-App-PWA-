from flask import Flask, request, jsonify, send_from_directory
import redis

app = Flask(__name__)

# Conexión a Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Ruta para servir la interfaz de la aplicación
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Ruta para guardar una nota
@app.route('/nota', methods=['POST'])
def guardar_nota():
    data = request.json
    titulo = data.get('titulo')
    contenido = data.get('contenido')

    if not titulo or not contenido:
        return jsonify({'error': 'Faltan campos: título y contenido'}), 400

    r.set(titulo, contenido)
    return jsonify({'mensaje': 'Nota guardada correctamente'}), 200

# Ruta para obtener una nota
@app.route('/nota/<titulo>', methods=['GET'])
def obtener_nota(titulo):
    contenido = r.get(titulo)

    if contenido is None:
        return jsonify({'error': 'Nota no encontrada'}), 404

    return jsonify({'titulo': titulo, 'contenido': contenido}), 200

# Ruta para servir archivos estáticos
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    app.run(debug=True)
