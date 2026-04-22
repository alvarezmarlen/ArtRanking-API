from flask import Flask
from config import DevelopmentConfig
from app.extensiones.db import init_db
from mongoengine.connection import get_db
from app.routes.auth_rutas import auth_bp
from app.routes.usuario_rutas import usuario_bp
from app.routes.concurso_rutas import concurso_bp
from app.routes.envio_rutas import envio_bp
from flask import render_template

from app.routes.voto_rutas import voto_bp

def create_app(config_class=DevelopmentConfig):
   app = Flask(__name__)
   app.config.from_object(config_class)

   app.register_blueprint(auth_bp, url_prefix="/auth")
   app.register_blueprint(usuario_bp, url_prefix="/users")
   app.register_blueprint(concurso_bp, url_prefix="/concursos")
   app.register_blueprint(envio_bp, url_prefix="/envios")
   
   app.register_blueprint(voto_bp, url_prefix="/votos")

   # Inicializar DB
   init_db(app)

   @app.route("/")
   def home():
# Como base.html está dentro de la carpeta 'layouts'
    return render_template("index.html")
    
   @app.route("/test-db")
   def test_db():
      db = get_db()
      collections = db.list_collection_names()
      return {"collections": collections}

   return app