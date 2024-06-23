from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin

from schemas.schemas import GrupoSchema
from schemas.schemas import GrupoActualizarSchema

from models.Model import db
from models.Grupo import Grupo

grupo = Blueprint('grupo', __name__, url_prefix='/grupo')

@grupo.route('/grupos', methods=['GET'])
def get_grupos():
    try:
        grupos:list[Grupo] = Grupo.query.order_by(Grupo.id).all()
        grupos:list[Grupo] = [grupo.serializar() for grupo in grupos] 
        return jsonify({"msg": "Áreas encontradas", "grupos": grupos}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar grupos", "error": str(e)}), 500

@grupo.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_grupo():
    try:
        data = request.get_json()
        try:
            grupo = GrupoSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        grupo:Grupo = Grupo(**data)
        grupo.save()
        return jsonify({"msg":"Grupo creado", "grupo":grupo.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el grupo", "error":str(e)}), 500

@grupo.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_grupo():
    try:
        data = request.get_json()
        try:
            GrupoActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        grupo:Grupo = Grupo.query.get(data.get('id'))
        if grupo is None:
            return jsonify({"msg":"Grupo no encontrado"}), 404

        grupo.nombre = data.get('nombre')
        grupo.descripcion = data.get('descripcion')
        grupo.save()
        return jsonify({"msg":"Grupo actualizado", "grupo":grupo.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el grupo", "error":str(e)}), 500