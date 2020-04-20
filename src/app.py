from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

# Creamos la aplicacion servidor de Flask
app = Flask(__name__)
# Creando la base de datos en MongoDb
app.config['MONGO_URI'] = 'mongodb://localhost/bdtareas'
# Creamos la conexion con la base de datos
mongo = PyMongo(app)

# Parar no tener problemas con React ya que en su entorno de desarrollo
# React crea su propio servidor, y para no tener ningun conflito
# Usamos Cors para que se comunique con el servidor de React
CORS(app)

# Creando la colecion de la base de datos
db = mongo.db.cltareas

# Crear tarea
@app.route('/tareas', methods=['POST'])
def crearTarea():
    # Insertamos el nuevo tarea ala Base de datos
    # Guardamos al tarea en una Variable ID
    # Ya retorna la Base de datos retorna un ID por defecto
    id = db.insert({
        'tareaNombre': request.json['tareaNombre'],
        'tarea': request.json['tarea'],
        'prioridad': request.json['prioridad'],
        'fecha': request.json['fecha']
    })
    # Convertimos el ID en un Objetocon ObjectId()
    # Convertimos el id a un String con str()
    # Retornamos al Cliente el ID del nuevo tarea
    return jsonify(str(ObjectId(id)))


# Obteniendo tarea
@app.route('/tareas', methods=['GET'])
def obtenerTareas():
    # Creamos un arreglo para los tarea que viene de la base de datos
    tareas = []
    # recoremos ese objecto (tarea)
   # para obtener su valor

    for doc in db.find():
        tareas.append({
            '_id': str(ObjectId(doc['_id'])),
            'tareaNombre': request.json['tareaNombre'],
            'tarea': request.json['tarea'],
            'prioridad': request.json['prioridad'],
            'fecha': request.json['fecha']
        })
        # retornamos el arreglo de tareas
    return jsonify(tareas)

# Obtener un unico tarea
@app.route('/tarea/<id>', methods=['GET'])
# Recibimos como parametro un Unico tarea con un ID
def obtenerTarea(id):
    # Creamos un variable para obtener el ID de esa tarea en especifica
    tarea = db.find_one({'_id': ObjectId(id)})
# retornamos en un formato json los datos
    return jsonify({
        '_id': str(ObjectId(tarea['_id'])),
        'tareaNombre': request.json['tareaNombre'],
        'tarea': request.json['tarea'],
        'prioridad': request.json['prioridad'],
        'fecha': request.json['fecha']
    })

# Eliminar tarea
@app.route('/tareas/<id>', methods=['DELETE'])
# Recibimos como parametro a esa unica tarea que queremos eliminar
def eliminarTarea(id):
    # Eliminamos al tarea atravez de ese ID unico
    db.delete_one({'_id': ObjectId(id)})
    # Retornamos al cliente un mensaje
    return jsonify({
        'msg': 'Tarea eliminada correctamente'
    })
# Actualizar tarea
@app.route('/tareas/<id>', methods=['PUT'])
# Indicamos atravez del ID que le pasamos
# Que tarea queremos eliminar
# Si el id es correcto Actualizamos los valores del tarea
def actualizarTarea(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'tareaNombre': request.json['tareaNombre'],
        'tarea': request.json['tarea'],
        'prioridad': request.json['prioridad'],
        'fecha': request.json['fecha']
    }})
    return jsonify({
        'msg': 'Tarea actualizada'
    })


# Iniciamos la app de del servidor
if __name__ == "__main__":
    app.run(debug=True)

#############################
# obtenemos todos las tareas
# Metodo GET
# http://localhost:5000/tareas
#############################

#############################
# Agregamos una tarea
# Metodo POST
# http://localhost:5000/tareas
#############################

#############################
# Obtenemos una tarea por id
# Metodo GET
# http://localhost:5000/tarea/<id>
#############################

#############################
# Agregamos una tarea
# Metodo POST
# http://localhost:5000/tareas
#############################

#############################
# Eliminamos una tarea
# Metodo DELETE
# http://localhost:5000/tareas/<id>
#############################

#############################
# Editar una tarea
# Metodo PUT
# http://localhost:5000/tareas/<id>
#############################
