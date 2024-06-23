from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin

from schemas.schemas import TiempoAreaSchema
from schemas.schemas import TiempoAreaActualizarSchema

from models.Model import db
from models.TiempoArea import TiempoArea

tiempo_area = Blueprint('tiempo_area', __name__, url_prefix='/tiempo_area')

@tiempo_area.route('/tiempo_areas', methods=['GET'])
def get_tiempo_areas():
    try:
        tiempo_areas:list[TiempoArea] = TiempoArea.query.order_by(TiempoArea.id).all()
        tiempo_areas:list[TiempoArea] = [tiempo_area.serializar(relaciones=['area', 'producto']) for tiempo_area in tiempo_areas] 
        return jsonify({"msg": "Tiempos encontradas", "tiempo_areas": tiempo_areas}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar tiempos", "error": str(e)}), 500

@tiempo_area.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_tiempo_area():
    try:
        data = request.get_json()
        try:
            tiempo_area = TiempoAreaSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        tiempo_area:TiempoArea = TiempoArea(**data)
        tiempo_area.save()
        return jsonify({"msg":"Tiempo creado", "tiempo":tiempo_area.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el tiempo", "error":str(e)}), 500

@tiempo_area.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_tiempo_area():
    try:
        data = request.get_json()
        try:
            TiempoAreaActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        tiempo_area:TiempoArea = TiempoArea.query.get(data.get('id'))
        if tiempo_area is None:
            return jsonify({"msg":"Tiempo no encontrado"}), 404

        tiempo_area.area_id = data.get('area_id')
        tiempo_area.producto_id = data.get('producto_id')
        tiempo_area.tiempos = data.get('tiempos')
        tiempo_area.save()
        return jsonify({"msg":"Tiempo actualizado", "tiempo_area":tiempo_area.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el tiempo", "error":str(e)}), 500