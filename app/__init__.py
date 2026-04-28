import os
from flask import Flask, request, redirect, url_for, g, flash, jsonify
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

   # Aplicando el middleware de jwt
   @app.before_request
   def middleware():
      # Lista de rutas que NO requieren autenticación
      public_endpoints = ['auth.login', 'auth.login_page', 'auth.registro_page', 'auth.register', 'home', 'static', 'concurso.detalle_pagina']
      token = request.cookies.get("access_token")
      g.user = None

      if token:
         payload = verificar_token(token)
         if payload:
            # Opcional: Cargar usuario en g.user para usarlo en templates
            g.user = Usuario.objects(id=payload["user_id"]).first()

      # Si no hay usuario y la ruta no es pública
      if not g.user and request.endpoint not in public_endpoints:
         # Si es una petición de API o AJAX, devolvemos JSON 401 en lugar de redireccionar a HTML
         if request.path.startswith('/envios/') or request.path.startswith('/votos/') or request.headers.get('Accept') == 'application/json':
             return jsonify({"error": "Tu sesión ha expirado o no has iniciado sesión. Por favor, inicia sesión de nuevo."}), 401
         return redirect(url_for("home"))
      
      # 2. Protección Admin: Si intenta entrar a una ruta de admin y NO es admin -> Error 403
      if request.blueprint == 'admin' and (not g.user or g.user.role != 'admin'):
         return redirect(url_for("error_403"))
      
   # Asegurar que la carpeta de uploads exista
   os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

   # Inicializar DB
   init_db(app)

   @app.route("/error-403")
   def error_403():
      return render_template("common/errores/403.html"), 403

   @app.errorhandler(404)
   def page_not_found(e):
      return render_template("common/errores/404.html"), 404

   @app.errorhandler(500)
   def internal_server_error(e):
      # Si es una petición de API o AJAX, devolvemos JSON en lugar de HTML
      if request.path.startswith('/envios/') or request.path.startswith('/votos/') or request.headers.get('Accept') == 'application/json':
         return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
      return render_template("common/errores/500.html"), 500

   # Handler específico para errores de base de datos (documentos que no existen)
   from mongoengine.errors import DoesNotExist
   @app.errorhandler(DoesNotExist)
   def handle_does_not_exist(e):
      return render_template("common/errores/404.html", message="El recurso solicitado no existe o ha sido eliminado."), 404

   @app.route("/")
   def home():
    """Render homepage with real data from database."""
    # Fetch stats from database
    total_obras = Envio.objects().count()
    concursos_activos = Concurso.objects(activo=True, estado="activo").count()
    total_votos = Voto.objects().count()
    total_artistas = Usuario.objects().count()

    # Fetch active contests safely
    concursos_query = Concurso.objects(activo=True, estado="activo").limit(10)
    concursos = []
    for c in concursos_query:
        try:
            # Forzamos la dereferencia para verificar que existe
            if c.creado_por:
                concursos.append(c)
            if len(concursos) >= 3: break
        except DoesNotExist:
            continue

    # Fetch featured submissions safely
    obras_query = Envio.objects().order_by('-votos').limit(10)
    obras = []
    for o in obras_query:
        try:
            # Verificamos autor y concurso
            if o.autor and o.concurso:
                obras.append(o)
            if len(obras) >= 4: break
        except DoesNotExist:
            continue

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