import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flaskr.modelos import Usuarios, Roles
from flask import abort
from flaskr.modelos.modelo import RolesEnum, EstadoPedidoEnum

from .modelos.modelo import db
from .vistas.vistas import (
    VistaSignin,
    VistalogIn,
    UsuariosResource,
    ProductosResource,
    PedidoResource,
    ReportePedidoResource,
    PedidoPorUsuarioYEstadoResource,
    PerfilUsuario
)
from flaskr.modelos import Usuarios


def create_app(config_name='default'):
    app = Flask(__name__)

    # Configuración DB → ahora con Neon
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar DB
    db.init_app(app)
    migrate = Migrate(app, db)

    # JWT
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'
    jwt = JWTManager(app)

    # CORS
    CORS(app)

    # Documentación con RESTX
    api = Api(
        app,
        version='1.0',
        title='API de Qlocuri',
        description='Documentación de la API RESTful para el sistema de pedidos Qlocuri',
        doc='/docs'
    )

    # Auth
    api.add_resource(VistaSignin, '/signin')
    api.add_resource(VistalogIn, '/login')

    # CRUDs
    api.add_resource(UsuariosResource, '/usuarios', '/usuarios/<int:id>')
    api.add_resource(ProductosResource, '/productos', '/productos/<int:id>')
    api.add_resource(PedidoResource, '/pedidos', '/pedidos/<int:id>')
    api.add_resource(ReportePedidoResource, '/reportes_pedidos', '/reportes_pedidos/<int:id>')
    api.add_resource(PedidoPorUsuarioYEstadoResource, '/pedidos/estado/<string:estado>')
    api.add_resource(PerfilUsuario, '/perfil')
    api.add_resource(PedidoPorUsuarioYEstadoResource, '/pedidos/usuario/estado/<string:estado>')
    api.add_resource(PedidoPorUsuarioYEstadoResource, '/pedidos/usuario/estado/<string:estado>/<int:id>')

    # 👇 CREAR TABLAS AUTOMÁTICAMENTE EN NEON (SOLO LA PRIMERA VEZ)
    with app.app_context():
        db.create_all()

    return app
