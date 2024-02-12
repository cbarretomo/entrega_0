from flask_restful import Resource, reqparse
from ..modelos import db, Usuarios, Categorias, Tareas, UsuarioSchema, CategoriaSchema, TareasSchema
from flask import request
from datetime import datetime
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash


tareas_schema = TareasSchema()
usuarios_schema = UsuarioSchema()
categorias_schema = CategoriaSchema()

class VistaTareas(Resource):
    #@jwt_required()
    #def get(self):
     #   return[tareas_schema.dump(tarea) for tarea in Tareas.query.all()]
    @jwt_required()
    def post(self):
        token_user_id = get_jwt_identity()
        nueva_tarea = Tareas(texto_task = request.json['texto_task'],
                             fecha_creacion = datetime.strptime(request.json['fecha_creacion'], '%d/%m/%Y').date(),
                             fecha_finalizacion = datetime.strptime(request.json['fecha_finalizacion'], '%d/%m/%Y').date(),
                             estado = request.json['estado'],
                             id_usuario = token_user_id,
                             id_categoria = request.json['id_categoria']
                            )
        db.session.add(nueva_tarea)
        db.session.commit()
        return tareas_schema.dump(nueva_tarea)
    
class VistaTarea(Resource):
    @jwt_required()
    def get(self, id_tarea):
        return tareas_schema.dump(Tareas.query.get_or_404(id_tarea))
    @jwt_required()
    def put(self, id_tarea):
        tarea = Tareas.query.get_or_404(id_tarea)
        tarea.texto_task = request.json.get('texto_task', tarea.texto_task)
        tarea.fecha_creacion = datetime.strptime(request.json.get('fecha_creacion', tarea.fecha_creacion), '%d/%m/%Y').date()
        tarea.fecha_finalizacion = datetime.strptime(request.json.get('fecha_finalizacion', tarea.fecha_finalizacion), '%d/%m/%Y').date()
        tarea.estado = request.json.get('estado', tarea.estado)
        tarea.id_usuario = request.json.get('id_usuario', tarea.id_usuario)
        tarea.id_categoria = request.json.get('id_categoria', tarea.id_categoria)
        db.session.commit()
        return tareas_schema.dump(tarea)
    
    def delete(self, id_tarea):
        tarea = Tareas.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return {'mensaje': 'Operacion exitosa'}, 204

class VistaUsuarios(Resource):
    def post(self):
        nuevo_usuario = Usuarios(nombre_usuario=request.json['nombre_usuario'],
                                 contrasenia= generate_password_hash(request.json['contrasenia']),
                                 imagen_perfil=request.json['imagen_perfil'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return{'mensaje':'Usuario creado'}

class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        return usuarios_schema.dump(Usuarios.query.get_or_404(id_usuario))
    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuarios.query.get_or_404(id_usuario)
        usuario.nombre_usuario = request.json.get('nombre_usuario', usuario.nombre_usuario)
        usuario.contrasenia = request.json.get('contrasenia', usuario.contrasenia)
        usuario.imagen_perfil = request.json.get('imagen_perfil', usuario.imagen_perfil)
        db.session.commit()
        return usuarios_schema.dump(usuario)
    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuarios.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return "Operacion exitosa", 204

class VistaCategorias(Resource):
    @jwt_required()
    def get(self):
        return[categorias_schema.dump(categoria) for categoria in Categorias.query.all()]
    @jwt_required()
    def post(self):
        nueva_categoria = Categorias(nombre = request.json['nombre'],
                                     descripcion = request.json['descripcion'])
        db.session.add(nueva_categoria)
        db.session.commit()
        return{'mensaje':'Categoria creada'}

class VistaCategoria(Resource):
    @jwt_required()   
    def put(self, id_categoria):
        categoria = Categorias.query.get_or_404(id_categoria)
        categoria.nombre = request.json.get('nombre', categoria.nombre)
        categoria.descripcion = request.json.get('descripcion', categoria.descripcion)
        db.session.commit()
        return{'mensaje':'Categoria actualizada '}
    @jwt_required() 
    def delete(self,id_categoria):
        categoria = Categorias.query.get_or_404(id_categoria)
        db.session.delete(categoria)
        db.session.commit()
        return{'mensaje':'Categoria eliminada'}

class TareaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        token_user_id = get_jwt_identity()
        if token_user_id != int(id_usuario):
            return {"mensaje": "Acceso denegado","usuario":token_user_id}, 403
        usuario = Usuarios.query.get_or_404(id_usuario)
        return [tareas_schema.dump(al) for al in usuario.tareas]

class IniciarSesion(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nombre_usuario', required=True)
        parser.add_argument('contrasenia', required=True)
        args = parser.parse_args()

        # Buscamos el usuario en la base de datos
        usuario = Usuarios.query.filter_by(nombre_usuario=args['nombre_usuario']).first()

        # Verificamos si el usuario existe y la contraseña es correcta
        if not usuario or not check_password_hash(usuario.contrasenia, args['contrasenia']):
            return {'mensaje': 'Usuario o contraseña incorrectos'}, 401

        # Generamos el token de autenticación
        token_de_acceso = create_access_token(identity=usuario.id_usuario)


        # Creamos la respuesta con el token y otros datos del usuario (opcional)
        return {
            'mensaje': 'Inicio de sesión exitoso',
            'token_de_acceso': token_de_acceso
        }

      