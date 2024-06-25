from models.Linea import Linea
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from middlewares.admin import middleware_admin
from marshmallow import ValidationError

from schemas.schemas import LineaSchema
from schemas.schemas import LineaActualizarSchema


linea = Blueprint('linea', __name__, url_prefix='/linea')

@linea.route('/lineas', methods=['GET'])
@jwt_required()
def get_lineas():
    try:
        lineas:list[Linea] = Linea.query.order_by(Linea.id).all()
        return jsonify({"msg": "Lineas encontradas", "lineas": [linea.serializar(relaciones=['productos.[tamanos]']) for linea in lineas]}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar las lineas", "error": str(e)}), 500

@linea.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_linea():
    try:
        data = request.get_json()
        try:
            LineaSchema().load(data)
        except ValidationError as e:
            print(e)
            return jsonify({"msg":e.messages}), 400
        linea = Linea(**data)
        linea.save()
        return jsonify({"msg": "Linea creada exitosamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al crear la linea", "error": str(e)}), 500
    
@linea.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_linea():
    try:
        data = request.get_json()
        try:
            LineaActualizarSchema().load(data)
        except ValidationError as e:
            print(e)
            return jsonify({"msg":e.messages}), 400
        linea:Linea = Linea.query.get(data.get('id'))
        if linea is None:
            return jsonify({"msg":"Linea no encontrada"}), 404
        linea.nombre = data['nombre']
        linea.descripcion = data['descripcion']
        linea.save()
        return jsonify({"msg":"Linea actualizada exitosamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar la linea", "error": str(e)}), 500