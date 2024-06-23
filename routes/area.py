from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin
from sqlalchemy import update

from schemas.schemas import AreaSchema
from schemas.schemas import AreaActualizarSchema

from models.Model import db
from models.Area import Area

area = Blueprint('area', __name__, url_prefix='/area')

@area.route('/areas', methods=['GET'])
def get_areas():
    try:
        areas:list[Area] = Area.query.order_by(Area.id).all()
        areas:list[Area] = [area.serializar() for area in areas] 
        return jsonify({"msg": "Áreas encontradas", "areas": areas}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar áreas", "error": str(e)}), 500

@area.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_area():
    try:
        data = request.get_json()
        try:
            area = AreaSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        area:Area = Area(**data)
        area.save()
        return jsonify({"msg":"Area creado", "area":area.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el area", "error":str(e)}), 500

@area.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_area():
    try:
        data = request.get_json()
        try:
            AreaActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        area:Area = Area.query.get(data.get('id'))
        if area is None:
            return jsonify({"msg":"Area no encontrado"}), 404

        area.nombre = data.get('nombre')
        area.descripcion = data.get('descripcion')
        area.finaliza = data.get('finaliza')
        area.save()

        area._finalizada()
        
        return jsonify({"msg":"Area actualizado", "area":area.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el area", "error":str(e)}), 500