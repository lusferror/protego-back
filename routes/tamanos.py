from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from middlewares.admin import middleware_admin
from marshmallow import ValidationError

from schemas.schemas import TamanoSchema
from schemas.schemas import TamanoActualizarSchema

from models.Tamano import Tamano

tamano  = Blueprint('tamano', __name__, url_prefix='/tamano')

@tamano.route('/tamanos', methods=['GET'])
@jwt_required()
def get_tamanos():
    try:
        tamanos:list[Tamano] = Tamano.query.order_by(Tamano.id).all()
        tamanos = list(map(lambda tamano: {
            **tamano.serializar(),
            "producto_nombre": tamano.producto.nombre,
        }, tamanos))
        return jsonify({"msg":"Tamanos encontrados", "tamanos":tamanos}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al buscar tamanos", "error":str(e)}), 500

@tamano.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_tamano():
    try:
        data = request.get_json()
        try:
            TamanoSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error al validar los datos", "error":e.messages}), 400
        tamano = Tamano(**data)
        tamano.save()
        return jsonify({"msg":"Tamano creado", "tamano":tamano.serializar()}), 201  
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear tamano", "error":str(e)}), 500

@tamano.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_tamano():
    try:
        data = request.get_json()
        try:
            TamanoActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error al validar los datos", "error":e.messages}), 400
        tamano:Tamano = Tamano.query.get(data['id'])
        if not tamano:
            return jsonify({"msg":"Tamano no encontrado"}), 404
        tamano.update(data)
        return jsonify({"msg":"Tamano actualizado", "tamano":tamano.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar tamano", "error":str(e)}), 500