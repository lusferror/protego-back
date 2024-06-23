from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity
from models.Usuario import Usuario
from flask import jsonify
from models.RolUsuario import RolUsuario

def middleware_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rut:str = get_jwt_identity()
        usuario: Usuario = Usuario.query.filter_by(rut=rut, activo=True).join(Usuario.roles_usuario.and_(RolUsuario.rol_id == 1, RolUsuario.activo == True)).first()
        if not usuario:
            return jsonify({"msg": "Usuario no encontrado"}), 403
        return f(*args, **kwargs)
    return decorated_function