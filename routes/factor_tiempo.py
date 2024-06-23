from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from middlewares.admin  import middleware_admin

from schemas.schemas import FactorTiempoSchema
from schemas.schemas import FactorTiempoActualizarSchema

from models.Model import db
from models.FactorTiempo import FactorTiempo

factor_tiempo = Blueprint('factor_tiempo', __name__, url_prefix='/factor_tiempo')

@factor_tiempo.route('/factor_tiempo', methods=['GET'])
def get_factor_tiempo():
    try:
        factor_tiempo:list[FactorTiempo] = FactorTiempo.query.order_by(FactorTiempo.id).all()
        factor_tiempo:list[FactorTiempo] = [factor_tiempo.serializar(relaciones=['grupo']) for factor_tiempo in factor_tiempo] 
        return jsonify({"msg": "Tiempos encontradas", "factor_tiempo": factor_tiempo}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar tiempos", "error": str(e)}), 500

@factor_tiempo.route('/crear', methods=['POST'])
@jwt_required()
@middleware_admin
def crear_factor_tiempo():
    try:
        data = request.get_json()
        try:
            factor_tiempo = FactorTiempoSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        factor_tiempo:FactorTiempo = FactorTiempo(**data)
        factor_tiempo.save()
        return jsonify({"msg":"Tiempo creado", "tiempo":factor_tiempo.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al crear el tiempo", "error":str(e)}), 500

@factor_tiempo.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar_tiempo_area():
    try:
        data = request.get_json()
        try:
            FactorTiempoActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Error en los datos enviados", "error":e.messages}), 400

        factor_tiempo:FactorTiempo = FactorTiempo.query.get(data.get('id'))
        if factor_tiempo is None:
            return jsonify({"msg":"Tiempo no encontrado"}), 404

        factor_tiempo.alto = data.get('alto')
        factor_tiempo.ancho = data.get('ancho')
        factor_tiempo.factor = data.get('factor')
        factor_tiempo.grupo_id = data.get('grupo_id')
        factor_tiempo.save()
        return jsonify({"msg":"Tiempo actualizado", "factor_tiempo":factor_tiempo.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg":"Error al actualizar el tiempo", "error":str(e)}), 500