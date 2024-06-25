import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.Model import db
from dotenv import load_dotenv

#Modelos
from models.Usuario import Usuario
from models.Rol import Rol
from models.RolUsuario import RolUsuario
from models.Area import Area
from models.Linea import Linea
from models.Producto import Producto
from models.Color import Color
from models.Tamano import Tamano
from models.TipoIncidente import TipoIncidente
from models.Incidente import Incidente
from models.Cliente import Cliente
from models.Orden import Orden
from models.BitacoraOrden import BitacoraOrden
from models.TiempoArea import TiempoArea
from models.FactorTiempo import FactorTiempo
from models.Grupo import Grupo


#Rutas
from routes.login import login
from routes.usuario import usuario
from routes.rol import rol
from routes.linea import linea
from routes.producto import producto
from routes.color import color
from routes.area import area
from routes.tipo_incidentes import tipo_incidente
from routes.cliente import cliente
from routes.grupo import grupo
from routes.tiempo_area import tiempo_area
from routes.factor_tiempo import factor_tiempo
from routes.orden import orden
from routes.bitacora_orden import bitacora_orden
from routes.tamanos import tamano

from werkzeug.security import generate_password_hash

load_dotenv()


app = Flask(__name__)
#Config for the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

#Rutas
app.register_blueprint(login)
app.register_blueprint(usuario)
app.register_blueprint(rol)
app.register_blueprint(linea)
app.register_blueprint(producto)
app.register_blueprint(color)
app.register_blueprint(area)
app.register_blueprint(tipo_incidente)
app.register_blueprint(cliente)
app.register_blueprint(grupo)
app.register_blueprint(tiempo_area)
app.register_blueprint(factor_tiempo)
app.register_blueprint(orden)
app.register_blueprint(bitacora_orden)
app.register_blueprint(tamano)


#Configuracion de migraciones
migrate = Migrate(app, db)

#Configuracion de JWT
jwt = JWTManager(app)

#Configuracion de CORS
CORS(app)

#Inicializacion de la base de datos
db.init_app(app)

@app.route('/<passwor>')
def create_password(passwor):
    return generate_password_hash(passwor)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    DEBUG = bool(os.environ.get('DEBUG', True))
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)