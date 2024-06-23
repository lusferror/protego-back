from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin

from schemas.schemas import TipoIncidenteSchema
from schemas.schemas import TipoIncidenteActualizarSchema
from schemas.schemas import IncidenteSchema

from models.Model import db
from models.TipoIncidente import TipoIncidente
from models.Incidente import Incidente

tipo_incidente = Blueprint('tipo_incidente', __name__, url_prefix='/tipo_incidente')

@tipo_incidente.route('/tipo_incidente', methods=['GET'])
def get_tipo_incidente():
    try:
        tipo_incidente:list[TipoIncidente] = TipoIncidente.query.order_by(TipoIncidente.id).all()
        tipo_incidente:list[TipoIncidente] = [tipo_incidente.serializar() for tipo_incidente in tipo_incidente] 
        return jsonify({"msg": "Áreas encontradas", "tipo_incidente": tipo_incidente}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar áreas", "error": str(e)}), 500

@tipo_incidente.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_tipo_incidente():
    try:
        data = request.get_json()
        try:
            tipo_incidente = TipoIncidenteSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        tipo_incidente:TipoIncidente = TipoIncidente(**data)
        tipo_incidente.save()
        return jsonify({"msg":"TipoIncidente creado", "tipo_incidente":tipo_incidente.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el tipo_incidente", "error":str(e)}), 500

@tipo_incidente.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_tipo_incidente():
    try:
        data = request.get_json()
        try:
            TipoIncidenteActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        tipo_incidente:TipoIncidente = TipoIncidente.query.get(data.get('id'))
        if tipo_incidente is None:
            return jsonify({"msg":"TipoIncidente no encontrado"}), 404

        tipo_incidente.nombre = data.get('nombre')
        tipo_incidente.descripcion = data.get('descripcion')
        tipo_incidente.save()
        return jsonify({"msg":"TipoIncidente actualizado", "tipo_incidente":tipo_incidente.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el tipo_incidente", "error":str(e)}), 500
    
@tipo_incidente.route('/incidente', methods=['POST'])
@jwt_required()
def incidente():
    try:
        data = request.get_json()
        try:
            IncidenteSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        incidente:Incidente = Incidente(**data)
        incidente.save()
        return jsonify({"msg":"Detención creada", "detencion":incidente.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el tipo_incidente", "error":str(e)}), 500