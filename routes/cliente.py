from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from middlewares.admin import middleware_admin
from flask_jwt_extended import jwt_required

from models.Cliente import Cliente
from models.Model import db

from schemas.schemas import ClienteSchema
from schemas.schemas import ClienteActualizarSchema

cliente = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente.route('/clientes', methods=['GET'])
@jwt_required()
def get_clientes():
    try:
        clientes: list[Cliente] = Cliente.query.order_by(Cliente.id).all()
        clientes: list[Cliente] = [cliente.serializar() for cliente in clientes]
        return jsonify({"msg": "Clientes encontrados", "clientes": clientes}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar clientes", "error": str(e)}), 500
    
@cliente.route('/crear', methods=['POST'])
@jwt_required()
def crear_cliente():
    try:
        data = request.get_json()
        ClienteSchema().load(data)
        cliente:Cliente = Cliente(**data)
        cliente.save()
        return jsonify({"msg": "Cliente creado", "cliente": cliente.serializar()}), 201
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"msg": "Error al validar datos", "error": e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear cliente", "error": str(e)}), 500

@cliente.route('/actualizar', methods=['PUT'])
@jwt_required()
def actualizar_cliente():
    try:
        data = request.get_json()
        ClienteActualizarSchema().load(data)
        cliente: Cliente = Cliente.query.get(data['id'])
        cliente.nombre = data['nombre']
        cliente.rut = data['rut']
        cliente.direccion = data['direccion']
        cliente.telefono = data['telefono'] if 'telefono' in data else cliente.telefono
        cliente.email = data['email']
        cliente.save()
        return jsonify({"msg": "Cliente actualizado", "cliente": cliente.serializar()}), 200
    except ValidationError as e:
        return jsonify({"msg": "Error al validar datos", "error": e.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"msg": "Error al actualizar cliente", "error": str(e)}), 500

@cliente.route('/desactivar/<int:id>', methods=['DELETE'])
@jwt_required()
def desactivar_cliente(id):
    try:
        cliente: Cliente = Cliente.query.get(id)
        cliente.activo = False
        cliente.save()
        return jsonify({"msg": "Cliente desactivado", "cliente": cliente.serializar()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al desactivar cliente", "error": str(e)}), 500

@cliente.route('/activar/<int:id>', methods=['PATCH'])
@jwt_required()
def activar_cliente(id):
    try:
        cliente: Cliente = Cliente.query.get(id)
        cliente.activo = True
        cliente.save()
        return jsonify({"msg": "Cliente activado", "cliente": cliente.serializar()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al activar cliente", "error": str(e)}), 500

@cliente.route('/activos')
@jwt_required()
def clientes_activos():
    try:
        clientes: list[Cliente] = Cliente.query.filter_by(activo=True).all()
        clientes: list[Cliente] = [cliente.serializar() for cliente in clientes]
        return jsonify({"msg": "Clientes activos encontrados", "clientes": clientes}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar clientes activos", "error": str(e)}), 500

