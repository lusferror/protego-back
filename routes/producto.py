from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from middlewares.admin import middleware_admin

from schemas.schemas import ProductoSchema
from schemas.schemas import ProductoActualizarSchema

from models.Producto import Producto


producto = Blueprint('producto', __name__, url_prefix='/producto')

@producto.route('/productos', methods=['GET'])
@jwt_required()
def productos():
    try:
        productos: list[Producto] = Producto.query.order_by(Producto.id).all()
        productos = [producto.serializar(relaciones=['linea', 'grupo']) for producto in productos]
        return jsonify({"msg":"Consulta exitosa", "productos":productos}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400

@producto.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_producto():
    try:
        data = request.get_json()
        try:
            ProductoSchema().load(data)
        except ValidationError as e:
            return jsonify({'msg': e.messages}), 400

        producto = Producto(**data)
        producto.save()
        return jsonify({"msg":"Producto creado", "producto":producto.serializar(relaciones=['linea', 'grupo'])}), 201
    except Exception as e:
        return jsonify({'msg': str(e)}), 400
    
@producto.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_producto():
    try:
        data = request.get_json()
        try:
            ProductoActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({'msg': e.messages}), 400

        producto:Producto = Producto.query.get(data['id'])
        if producto is None:
            return jsonify({'msg': 'Producto no encontrado'}), 404
        producto.update(data)
        return jsonify({"msg":"Producto actualizado", "producto":producto.serializar(relaciones=['linea', 'grupo'])}), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 400