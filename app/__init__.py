from flask import Flask
from config import DevelopmentConfig
from app.extensiones.db import init_db
from mongoengine.connection import get_db
from app.routes.auth_rutas import auth_bp
from app.routes.usuario_rutas import usuario_bp
from app.routes.concurso_rutas import concurso_bp
from app.routes.envio_rutas import envio_bp
from app.routes.voto_rutas import voto_bp
from app.routes.categoria_rutas import categoria_bp
from flask import render_template

from app.routes.admin_rutas import admin_bp
from app.models.concurso import Concurso
from app.models.envio import Envio
from app.models.usuario import Usuario
from app.models.voto import Voto

def create_app(config_class=DevelopmentConfig):
   app = Flask(__name__)
   app.config.from_object(config_class)

   app.register_blueprint(auth_bp, url_prefix="/auth")
   app.register_blueprint(usuario_bp, url_prefix="/users")
   app.register_blueprint(concurso_bp, url_prefix="/concursos")
   app.register_blueprint(envio_bp, url_prefix="/envios")
   app.register_blueprint(voto_bp, url_prefix="/votos")
   app.register_blueprint(admin_bp, url_prefix="/admin")
   app.register_blueprint(categoria_bp, url_prefix="/categorias")

   # Inicializar DB
   init_db(app)

   @app.route("/")
   def home():
    """Render homepage with real data from database."""
    # Fetch stats from database
    total_obras = Envio.objects().count()
    concursos_activos = Concurso.objects(activo=True, estado="activo").count()
    total_votos = Voto.objects().count()
    total_artistas = Usuario.objects().count()

    # Fetch active contests (limit 3 for homepage)
    # Don't dereference categories to avoid schema mismatch
    concursos = Concurso.objects(activo=True, estado="activo").limit(3)

    # Fetch featured submissions (limit 4)
    obras = Envio.objects().order_by('-votos').limit(4)

    return render_template("index.html",
                          total_obras=total_obras,
                          concursos_activos=concursos_activos,
                          total_votos=total_votos,
                          total_artistas=total_artistas,
                          concursos=concursos,
                          obras=obras)

   @app.route("/test-db")
   def test_db():
      db = get_db()
      collections = db.list_collection_names()
      return {"collections": collections}

   return app