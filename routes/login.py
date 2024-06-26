from flask import request, jsonify, Blueprint
from models.Usuario import Usuario
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

login = Blueprint('login', __name__, url_prefix='/login')

@login.route('', methods=['POST'])
def login_user() -> jsonify:
    try:
        rut = request.json.get('rut')
        password = request.json.get('password')

        if not rut:
            return jsonify({"msg": "El email es erequerido!"}), 400
        if not password:
            return jsonify({"msg": "La conteraseña es requerida!"}), 400

        usuario:Usuario = Usuario.query.filter_by(rut=rut).first()

        if not usuario:
            return jsonify({"msg": "Usuario o contraseña son incorrectos!"}), 401

        if not check_password_hash(usuario.password, password):
            return jsonify({"msg": "Usuario o contraseña son incorrectos!"}), 401
        
        expiracion = timedelta(hours=10)
        token = create_access_token(identity=rut, expires_delta=expiracion)

        data = {
            "msg": "Inicio de sesion exitoso!",
            "token": token,
            "usuario": usuario.serializar(relaciones=['area', 'roles'])
        }

        return jsonify(data), 200
    
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500
