from flask import Flask
from config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # IMPORTANTE: Importar los modelos para que Alembic los detecte
    from . import models

    @app.shell_context_processor
    def contexto_shell():
        context = {
            "db": db,
            "Usuario": models.Usuario,
            "Cliente": models.Cliente,
            "Producto": models.Producto,
        }
        for nombre in ("Venta", "DetalleVenta"):
            if hasattr(models, nombre):
                context[nombre] = getattr(models, nombre)
        return context

    return app