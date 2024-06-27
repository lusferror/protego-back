from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from middlewares.admin import middleware_admin

from marshmallow import ValidationError
from schemas.schemas import UsuarioRegistroSchema
from schemas.schemas import UsuarioActualizarSchema
from schemas.schemas import UsuarioContrasenaSchema

from models.Model import db
from models.Usuario import Usuario
from models.RolUsuario import RolUsuario
from models.Rol import Rol

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario.route('/registro', methods=['POST'])
@jwt_required()
@middleware_admin
def registro() -> jsonify:
    try:
        data:dict  = request.get_json()
        try:
            UsuarioRegistroSchema().load(data)
        except ValidationError as e:
            return jsonify(e.messages), 400
        
        usuario = Usuario()
        usuario.nombre = data.get('nombre')
        usuario.segundo_nombre = data.get('segundo_nombre')
        usuario.apellido = data.get('apellido')
        usuario.segundo_apellido = data.get('segundo_apellido')
        usuario.email = data.get('email')
        usuario.password = generate_password_hash(data.get('password'))
        usuario.area_id = data.get('area_id') if data.get('area_id') else None
        usuario.rut = data.get('rut')
        for roles in data.get('roles'):
            rol:RolUsuario = RolUsuario(rol_id=roles, activo=True)
            usuario.roles_usuario.append(rol)
        
        usuario.save()
        msg:dict = {
            "msg": "Usuario creado correctamente",
            "usuario": usuario.serializar(relaciones=['roles', 'area']),
        }
        return jsonify(msg), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"msg": str(e)}), 500

@usuario.route('/usuarios', methods=['GET'])
@jwt_required()
@middleware_admin
def get_usuarios() -> jsonify:
    try:
        usuarios: list[Usuario] = Usuario.query.order_by(Usuario.id).all()
        response: dict = {
            "msg": "Consulta exitosa",
            "usuarios": [usuario.serializar(relaciones=['roles', 'area']) for usuario in usuarios]
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ha ocurrido un error en la consulta"}), 500
    
@usuario.route('/maestros', methods=['GET'])
@jwt_required()
def get_maestros() -> jsonify:
    try:
        rut:str = get_jwt_identity()
        jefe_area:Usuario = Usuario.query.filter_by(rut=rut).first()
        maestros:Usuario = Usuario.query.filter_by(area_id=jefe_area.area_id).all()
        reponse:dict = {
            "msg": "Consulta exitosa",
            "maestros": [maestro.serializar() for maestro in maestros]
        }
        return jsonify(reponse), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ha ocurrido un error en la consulta"}), 500
    
@usuario.route('/actualizar', methods=['PUT'])
@jwt_required()
@middleware_admin
def actualizar() -> jsonify:
    try:
        data:dict = request.get_json()
        try:
            UsuarioActualizarSchema().load(data)
        except ValidationError as e:
            return jsonify(e.messages), 400
        
        usuario:Usuario = Usuario.query.get(data.get('id'))
        usuario.nombre = data.get('nombre')
        usuario.segundo_nombre = data.get('segundo_nombre')
        usuario.apellido = data.get('apellido')
        usuario.segundo_apellido = data.get('segundo_apellido')
        usuario.email = data.get('email')
        usuario.area_id = data.get('area_id')
        usuario.telefono = data.get('telefono')
        usuario.update()
        
        #Actualizamos los roles
        roles:list[int] = data.get("roles")
        for rol in roles:
            rol_usuario = RolUsuario.query.filter_by(rol_id=rol, usuario_id=usuario.id).one_or_none()
            if not rol_usuario:
                rol_usuario = RolUsuario(rol_id=rol, usuario_id=usuario.id, activo=True)
                rol_usuario.save()
            else:
                rol_usuario.activo = True
                rol_usuario.update()
        
        #Desactivamos los roles que no esten en la lista        
        roles_inactivos:list[RolUsuario] = RolUsuario.query.where(
        and_(RolUsuario.rol_id.not_in(roles), RolUsuario.usuario_id == usuario.id)).all()
        for rol in roles_inactivos:
            rol.activo = False
            rol.update()

        msg:dict = {
            "msg": "Usuario actualizado correctamente",
            "usuario": usuario.serializar(relaciones=['roles', 'area']),
        }
        return jsonify(msg), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"msg": str(e)}), 500
    
@usuario.route('/desactivar/<int:id>', methods=['DELETE'])
@jwt_required()
@middleware_admin
def desactivar(id:int) -> jsonify:
    try:
        usuario:Usuario = Usuario.query.get(id)
        usuario.activo = False
        usuario.update()
        return jsonify({"msg": "Usuario desactivado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"msg": str(e)}), 500

@usuario.route('/activar/<int:id>', methods=['PATCH'])
@jwt_required()
@middleware_admin
def activar(id:int) -> jsonify:
    try:
        usuario:Usuario = Usuario.query.get(id)
        usuario.activo = True
        usuario.update()
        return jsonify({"msg": "Usuario activado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"msg": str(e)}), 500

@usuario.route('/operadores/<int:area_id>', methods=['GET'])
@jwt_required()
def get_operadores(area_id:int) -> jsonify:
    try:
        operadores: list[Usuario] = Usuario.query.filter_by(area_id=area_id).all()
        response: dict = {
            "msg": "Consulta exitosa",
            "usuarios": list(map(lambda operador: {
                "id": operador.id,
                "nombre": operador.nombre_completo(),
                "rol": operador.roles[0].nombre
            }, operadores))
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ha ocurrido un error en la consulta"}), 500

@usuario.route('/contrasena', methods=['PUT'])
@jwt_required()
@middleware_admin
def contrasena() -> jsonify:
    try:
        data:dict = request.get_json()
        try:
            UsuarioContrasenaSchema().load(data)
        except ValidationError as e:
            return jsonify(e.messages), 400
        usuario:Usuario = Usuario.query.get(data.get('id'))
        usuario.password = generate_password_hash(data.get('password'))
        usuario.update()
        return jsonify({"msg": "Contraseña cambiada correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Ha ocurrido un error al cambiar contraseña", "error":str(e)}), 500

