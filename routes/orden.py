import os, sys
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc
from flask_jwt_extended import jwt_required

from schemas.schemas import OrdenSchema
from schemas.schemas import OrdenActualizarSchema

from models.Orden import Orden
from models.BitacoraOrden import BitacoraOrden

orden = Blueprint("orden", __name__, url_prefix="/orden")


@orden.route("/ordenes", methods=["GET"])
@jwt_required()
def get_ordenes():
    try:
        ordenes: list[Orden] = Orden.query.order_by(desc(Orden.id)).all()
        ordenes: list[Orden] = [
            orden.serializar(
                relaciones=[
                    "producto",
                    "cliente",
                    "tamaño",
                    "color",
                    "bitacora",
                ]
            )
            for orden in ordenes
        ]
        return jsonify({"msg": "Ordenes encontradas", "ordenes": ordenes}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar ordenes"}), 500


@orden.route("/crear", methods=["POST"])
@jwt_required()
def crear_orden():
    try:
        data = request.get_json()
        try:
            OrdenSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg": "Error de validación", "errors": e.messages}), 400
        orden: Orden = Orden(**data)
        orden.save()
        return jsonify({"msg": "Orden creada", "orden": orden.serializar()}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al crear orden"}), 500


@orden.route("/actualizar", methods=["PUT"])
@jwt_required()
def actualizar_orden():
    try:
        data = request.get_json()
        try:
            OrdenActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify({"msg": "Error de validación", "errors": e.messages}), 400
        orden: Orden = Orden.query.get(data["id"])
        orden.producto_id = data["producto_id"]
        orden.cliente_id = data["cliente_id"]
        orden.ancho = data["ancho"]
        orden.alto = data["alto"]
        orden.largo = data["largo"]
        orden.color_id = data["color_id"]
        orden.nro_orden = data["nro_orden"]
        orden.fecha = data["fecha"]
        orden.fecha_entrega = data["fecha_entrega"]
        orden.save()
        return jsonify({"msg": "Orden actualizada", "orden": orden.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al actualizar orden"}), 500


@orden.route("/cancelar/<int:id>", methods=["PUT"])
@jwt_required()
def cancelar_orden(id):
    try:
        orden: Orden = Orden.query.get(id)
        orden.estado = "cancelada"
        orden.save()
        return jsonify({"msg": "Orden cancelada", "orden": orden.serializar()}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al cancelar orden"}), 500


@orden.route("/estado/<estado>")
@jwt_required()
def orden_proceso(estado):
    try:
        ordenes: list[Orden] = (
            Orden.query.filter(Orden.estado == estado).order_by(desc(Orden.id)).all()
        )
        ordenes: list[Orden] = [
            orden.serializar(
                relaciones=["bitacora_ultimo.[area,usuario]", "incidentes", "cliente"]
            )
            for orden in ordenes
        ]
        return jsonify({"msg": "Ordenes en proceso", "ordenes": ordenes}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Error al buscar ordenes"}), 500


@orden.route("/<int:id>")
@jwt_required()
def get_orden(id: int):
    try:
        orden: Orden = Orden.query.get(id)
        return (
            jsonify(
                {
                    "msg": "Orden encontrada",
                    "orden": orden.serializar(
                        relaciones=[
                            "cliente",
                            "producto",
                            "color",
                            "bitacora.[area,usuario]",
                            "incidentes.[area,usuario,tipo_incidente]",
                        ],
                    ),
                }
            ),
            200,
        )
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({"msg": "Error al buscar orden"}), 500


@orden.route("/exportar/<estado>")
@jwt_required()
def exportar_ordenes(estado):
    ordenes: list[Orden] = Orden.query.order_by(desc(Orden.id))
    if estado == "todas":
        ordenes: list[Orden] = ordenes.all()
    else:
        ordenes: list[Orden] = ordenes.filter(Orden.estado == estado).all()

    ordenes_reporte = list()
    for orden in ordenes:
        fila_reporte = {
            "NRO_ORDEN": orden.nro_orden,
            "FECHA_ORDEN": orden.fecha,
            "PRODUCTO": orden.producto.nombre,
            "CLIENTE": orden.cliente.nombre,
            "ESTADO": orden.estado,
            "INCIDENTES": len(orden.incidentes),
        }
        if len(orden.incidentes) <= 0:
            bitacora_vacio = {
                "AREA": "",
                "USUARIO": "",
                "INICIO": "",
                "FIN": "",
                "TIEMPO_ESTIMADO": "",
                "TIEMPO_REAL": "",
                "DIFERENCIA": "",
            }
            fila_reporte.update(bitacora_vacio)
        for bitacora in orden.bitacora:
            bitacora_data = {
                "AREA": bitacora.area.nombre,
                "USUARIO": bitacora.usuario.nombre,
                "INICIO": bitacora.inicio,
                "FIN": bitacora.fin,
                "TIEMPO_ESTIMADO": bitacora.tiempo_estimado(),
                "TIEMPO_REAL": bitacora.tiempo_real(),
                "DIFERENCIA": bitacora.diferencia(),
            }
            fila_reporte.update(bitacora_data)
        ordenes_reporte.append(fila_reporte)

    return jsonify({"msg": "Ordenes encontradas", "ordenes": ordenes_reporte}), 200
