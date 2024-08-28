from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import desc, or_
from schemas.schemas import BitacoraOrdenSchema
from marshmallow import ValidationError
from datetime import datetime

from models.BitacoraOrden import BitacoraOrden
from models.Orden import Orden
from models.Area import Area

bitacora_orden = Blueprint('bitacora_orden', __name__, url_prefix='/bitacora_orden')

@bitacora_orden.route('<nro_orden>/<int:area_id>', methods=['GET'])
@jwt_required()
def index(nro_orden: str, area_id: int):
    try:
        orden:Orden = Orden.query.filter(Orden.nro_orden==nro_orden, or_(Orden.estado=='proceso', Orden.estado=='creada', Orden.estado == 'pausada')).one_or_none()
        if orden is None:
            return jsonify({"msg": "No se encontró la orden"}), 400
        orden.estado = "proceso"
        orden.update()
        bitacora:BitacoraOrden = BitacoraOrden.query.filter_by(orden_id=orden.id, area_id=area_id).order_by(desc(BitacoraOrden.id)).first()
        return jsonify({
            "msg":"Orden encontrada", 
            "bitacora":bitacora.serializar() if bitacora is not None else None,
            "orden":orden.serializar()
            }), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al obtener la bitácora", "error":str(e)}), 500
    
@bitacora_orden.route('/crear', methods=['POST'])
@jwt_required()
def store():
    try:
        data = request.get_json()
        try:
            BitacoraOrdenSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg":"Ha ocurrido un error", "errores":list(e.messages)}), 400
        bitacora:BitacoraOrden = BitacoraOrden(**data)
        bitacora.inicio = datetime.now();
        bitacora.save()

        orden:Orden = Orden.query.get(bitacora.orden_id)
        orden.estado = "proceso"
        orden.update()

        return jsonify({"msg":"Bitácora creada", "bitacora":bitacora.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al crear la bitácora", "error":str(e)}), 500

@bitacora_orden.route('/finalizar/<int:id>', methods=['PUT'])
@jwt_required()
def finalizar(id:int):
    try:
        bitacora:BitacoraOrden = BitacoraOrden.query.get(id)
        if bitacora is None:
            return jsonify({"msg": "No se encontró la bitácora"}), 400
        bitacora.fin = datetime.now()
        bitacora.estado = "Finalizado"
        bitacora.update()

        area:Area = Area.query.get(bitacora.area_id)
        print(area.finaliza)
        if area is not None and area.finaliza is True:
            orden:Orden = Orden.query.get(bitacora.orden_id)
            print(orden)
            orden.estado = "Finalizado"
            orden.update()

        return jsonify({"msg":"Bitácora finalizada", "bitacora":bitacora.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al finalizar la bitácora", "error":str(e)}), 500
    
@bitacora_orden.route('/pausar/<int:id>', methods=['PUT'])
@jwt_required()
def pausar(id:int):
    try:
        bitacora:BitacoraOrden = BitacoraOrden.query.get(id)
        if bitacora is None:
            return jsonify({"msg": "No se encontró la bitácora"}), 400
        bitacora.fin = datetime.now()
        bitacora.estado = "Pausado"
        bitacora.update()

        orden:Orden = Orden.query.get(bitacora.orden_id)
        orden.estado = "pausada"
        orden.update()

        return jsonify({"msg":"Bitácora pausada", "bitacora":bitacora.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al pausar la bitácora", "error":str(e)}), 500
    