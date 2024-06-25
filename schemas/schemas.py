from marshmallow import Schema, fields

class RolSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'});
    descripcion = fields.Str()

class RolActualizarSchema(RolSchema):
    id = fields.Int(required=True)

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    rut = fields.Str(required=True, error_messages={'required': 'El rut es requerido'})
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    segundo_nombre = fields.Str(allow_none=True)
    apellido = fields.Str(required=True, error_messages={'required': 'El apellido es requerido'})
    segundo_apellido = fields.Str(allow_none=True)
    email = fields.Str(required=True, error_messages={'required': 'El email es requerido'})
    area_id = fields.Int(required=False, allow_none=True)
    roles = fields.List(fields.Int(), required=True, error_messages={'required': 'Los roles son requeridos'})
    telefono = fields.Str(allow_none=True)

class UsuarioRegistroSchema(UsuarioSchema):
    password = fields.Str(required=True, error_messages={'required': 'La contraseña es requerida'})

class UsuarioActualizarSchema(UsuarioSchema):
    id = fields.Int(required=True)

class LineaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    descripcion = fields.Str(allow_none=True)

class LineaActualizarSchema(LineaSchema):
    id = fields.Int(required=True)

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    codigo = fields.Str(required=True, error_messages={'required': 'El código es requerido'})
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    linea_id = fields.Int(required=True, error_messages={'required': 'La línea es requerida'})
    grupo_id = fields.Int(allow_none=True)

class ProductoActualizarSchema(ProductoSchema):
    id = fields.Int(required=True)

class ColorSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    descripcion = fields.Str(allow_none=True)

class ColorActualizarSchema(ColorSchema):
    id = fields.Int(required=True)

class AreaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    descripcion = fields.Str(allow_none=True)
    finaliza = fields.Bool(allow_none=True)

class AreaActualizarSchema(AreaSchema):
    id = fields.Int(required=True)

class TipoIncidenteSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    descripcion = fields.Str(allow_none=True)

class TipoIncidenteActualizarSchema(TipoIncidenteSchema):
    id = fields.Int(required=True)

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    rut = fields.Str(required=True, error_messages={'required': 'El rut es requerido'})
    direccion = fields.Str(allow_none=True)
    telefono = fields.Str(allow_none=True)
    email = fields.Str(required=True, error_messages={'required': 'El email es requerido'})

class ClienteActualizarSchema(ClienteSchema):
    id = fields.Int(required=True)

class GrupoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, error_messages={'required': 'El nombre es requerido'})
    descripcion = fields.Str(allow_none=True)

class GrupoActualizarSchema(GrupoSchema):
    id = fields.Int(required=True)

class TiempoAreaSchema(Schema):
    id = fields.Int(dump_only=True)
    tiempos = fields.Int(required=True, error_messages={'required': 'El tiempo es requerido'})
    area_id = fields.Int(required=True, error_messages={'required': 'El área es requerida'})
    producto_id = fields.Int(required=True, error_messages={'required': 'El producto es requerido'})

class TiempoAreaActualizarSchema(TiempoAreaSchema):
    id = fields.Int(required=True)

class FactorTiempoSchema(Schema):
    id = fields.Int(dump_only=True)
    alto = fields.Int(required=True, error_messages={'required': 'El alto es requerido'})
    ancho = fields.Int(required=True, error_messages={'required': 'El ancho es requerido'})
    factor = fields.Float(required=True, error_messages={'required': 'El factor es requerido'})
    grupo_id = fields.Int(required=True, error_messages={'required': 'El grupo es requerido'})

class FactorTiempoActualizarSchema(FactorTiempoSchema):
    id = fields.Int(required=True)

class OrdenSchema(Schema):
    id = fields.Int(dump_only=True)
    nro_orden = fields.Str(required=True, error_messages={'required': 'El número de orden es requerido'})
    fecha = fields.DateTime(required=True, error_messages={'required': 'La fecha es requerida'})
    fecha_entrega = fields.DateTime(required=True, error_messages={'required': 'La fecha de entrega es requerida'})
    cliente_id = fields.Int(required=True, error_messages={'required': 'El cliente es requerido'})
    producto_id = fields.Int(required=True, error_messages={'required': 'El producto es requerido'})
    ancho = fields.Int(allow_none=True)
    alto = fields.Int(allow_none=True)
    largo = fields.Int(allow_none=True)
    color_id = fields.Int(allow_none=True)
    observaciones = fields.Str(allow_none=True)
    estado = fields.Str(allow_none=True)

class OrdenActualizarSchema(OrdenSchema):
    id = fields.Int(required=True)

class BitacoraOrdenSchema(Schema):
    id = fields.Int(dump_only=True)
    orden_id = fields.Int(required=True, error_messages={'required': 'La orden es requerida'})
    area_id = fields.Int(required=True, error_messages={'required': 'El área es requerida'})
    usuario_id = fields.Int(required=True, error_messages={'required': 'El usuario es requerido'})

class IncidenteSchema(Schema):
    id = fields.Int(dump_only=True)
    tipo_incidente_id = fields.Int(required=True, error_messages={'required': 'El tipo de incidente es requerido'})
    usuario_id = fields.Int(required=True, error_messages={'required': 'El usuario es requerido'})
    area_id = fields.Int(required=True, error_messages={'required': 'El área es requerida'})
    orden_id = fields.Int(allow_none=True)

class TamanoSchema(Schema):
    id = fields.Int(dump_only=True)
    producto_id = fields.Int(required=True, error_messages={'required': 'El producto es requerido'})
    largo = fields.Int(required=True, error_messages={'required': 'El largo es requerido'})
    ancho = fields.Int(required=True, error_messages={'required': 'El ancho es requerido'})
    alto = fields.Int(required=True, error_messages={'required': 'El alto es requerido'})

class TamanoActualizarSchema(TamanoSchema):
    id = fields.Int(required=True)