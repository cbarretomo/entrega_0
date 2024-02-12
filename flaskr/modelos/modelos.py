from typing import Any
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key =True)
    nombre_usuario = db.Column(db.String(128))
    contrasenia = db.Column(db.String(32))
    imagen_perfil = db.Column(db.String(256))
    tareas = db.relationship('Tareas', cascade='all, delete, delete-orphan')

class Categorias(db.Model):
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    descripcion = db.Column(db.String(256))
    tareas = db.relationship('Tareas', cascade='all, delete, delete-orphan')

class Tareas(db.Model):
    id_tarea = db.Column(db.Integer, primary_key =True)
    texto_task = db.Column(db.String(256))
    fecha_creacion = db.Column(db.Date())
    fecha_finalizacion = db.Column(db.Date())
    estado = db.Column(db.String(128))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'))

class EnumDiccionario(fields.Field):
    def _serialize(self, value, atrr, obj, **kwargs):
        if value is None:
            return None
        return {'llave':value.name, 'valor':value.value}

class TareasSchema(SQLAlchemyAutoSchema):
    medio =EnumDiccionario(attribute=('medio'))
    class Meta:
        model = Tareas
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    medio =EnumDiccionario(attribute=('medio'))
    class Meta:
        model = Usuarios
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    medio =EnumDiccionario(attribute=('medio'))
    class Meta:
        model = Categorias
        include_relationships = True
        load_instance = True