from flaskr import create_app
from .modelos import db, Tareas, Usuarios, Categorias, TareasSchema
from datetime import datetime
from flask_restful import Api
from .vistas import VistaTareas, VistaTarea, VistaUsuario, VistaUsuarios, VistaCategoria, VistaCategorias, TareaUsuario, IniciarSesion
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaTareas, '/tareas')
api.add_resource(VistaTarea, '/tarea/<int:id_tarea>')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaCategorias, '/categorias')
api.add_resource(VistaCategoria, '/categoria/<int:id_categoria>')
api.add_resource(TareaUsuario, '/usuario/<int:id_usuario>/tarea')
api.add_resource(IniciarSesion,'/login')

jwt = JWTManager(app)



    


