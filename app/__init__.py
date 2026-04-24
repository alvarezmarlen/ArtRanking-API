from flask import Flask, request, redirect, url_for, g, flash
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
from app.utils.jwt_utils import verificar_token
from app.models.usuario import Usuario
from app.routes.admin_rutas import admin_bp

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

   # Aplicando el middleware de jwt
   @app.before_request
   def middleware():
      # Lista de rutas que NO requieren autenticación
      public_endpoints = ['auth.login', 'auth.login_page', 'auth.registro_page', 'auth.register', 'home', 'static']
      token = request.cookies.get("access_token")
      g.user = None

      if token:
         payload = verificar_token(token)
         if payload:
            # Opcional: Cargar usuario en g.user para usarlo en templates
            g.user = Usuario.objects(id=payload["user_id"]).first()

      # Si no hay usuario y la ruta no es pública, redirigir al home
      if not g.user and request.endpoint not in public_endpoints:
         return redirect(url_for("home"))
      # 2. Protección Admin: Si intenta entrar a una ruta de admin y NO es admin -> Error 403
      if request.blueprint == 'admin' and (not g.user or g.user.role != 'admin'):
         return redirect(url_for("error_403"))
      
   # Inicializar DB
   init_db(app)

   @app.route("/error-403")
   def error_403():
      return render_template("common/errores/403.html"), 403

   @app.route("/")
   def home():

    return render_template("index.html")
    
   @app.route("/test-db")
   def test_db():
      db = get_db()
      collections = db.list_collection_names()
      return {"collections": collections}

   return app