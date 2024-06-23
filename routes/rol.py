from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from middlewares.admin import middleware_admin
from models.Rol import Rol
from schemas.schemas import RolSchema, RolActualizarSchema

rol = Blueprint('rol', __name__, url_prefix='/rol')

@rol.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_rol():
    try:
        data = request.get_json()
        try:
            RolSchema().load(data)
        except ValidationError as e:
            return jsonify(e.messages), 400
        rol = Rol(**data)
        rol.save()
        return jsonify({'msg': 'Rol creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@rol.route('/roles', methods=['GET'])
@jwt_required()
@middleware_admin
def roles():
    try:
        roles: list[Rol] = Rol.query.order_by(Rol.id).all()
        roles= list(map(lambda rol:{
            'id': rol.id,
            'nombre': rol.nombre,
            'descripcion': rol.descripcion
        }, roles))

        return jsonify({"msg":"Consulta exitosa", "roles":roles}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400
    
@rol.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_rol():
    try:
        data = request.get_json()
        try:
            RolActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify(e.messages), 400
        rol:Rol = Rol.query.get(data.get('id'))
        if rol is None:
            return jsonify({'msg': 'Rol no encontrado'}), 404
        rol.nombre = data['nombre']
        rol.descripcion = data['descripcion']
        rol.save()
        return jsonify({'msg': 'Rol actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400