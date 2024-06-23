from flask import Blueprint, request, jsonify
from models.Model import db
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin

from schemas.schemas import ColorSchema 
from schemas.schemas import ColorActualizarSchema

from models.Color import Color

color = Blueprint('color', __name__, url_prefix='/color')

@color.route('/colores', methods=['GET'])
@jwt_required()
def get_colores():
    try:
        colores:list[Color] = Color.query.order_by(Color.id).all()
        colores = [color.serializar() for color in colores]
        return jsonify({"msg":"Colores encontrados", "colores":colores}), 200
    except Exception as e:
        print(e)
        return jsonify({'msg':"Error al buscar los colores","error":str(e)}), 500

@color.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_color():
    try:
        data = request.get_json()
        try:
            color = ColorSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        color:Color = Color(**data)
        color.save()
        return jsonify({"msg":"Color creado", "color":color.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el color", "error":str(e)}), 500

@color.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_color():
    try:
        data = request.get_json()
        try:
            ColorActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        color:Color = Color.query.get(data.get('id'))
        if color is None:
            return jsonify({"msg":"Color no encontrado"}), 404

        color.nombre = data.get('nombre')
        color.descripcion = data.get('descripcion')
        color.save()
        return jsonify({"msg":"Color actualizado", "color":color.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el color", "error":str(e)}), 500