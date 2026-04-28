import os
import uuid
from flask import Blueprint, jsonify, request, current_app, render_template
from werkzeug.utils import secure_filename
from app.services.envio_servicio import (
    crear_envio,
    obtener_envios,
    obtener_envio,
    actualizar_envio,
    eliminar_envio,
    votar_envio,
    obtener_etiquetas_envio,
    obtener_ranking
)
from app.utils.decoradores import jwt_requerido
from mongoengine.errors import DoesNotExist

envio_bp = Blueprint("envio", __name__)


@envio_bp.route("/ranking", methods=["GET"])  # GET /envios/ranking (HTML Page - Public)
def ranking_pagina():
    """Render página de ranking global (HTML). Público, no requiere JWT."""
    from app.models.envio import Envio
    from app.models.concurso import Concurso

    # Obtener parámetros de filtro
    concurso_id = request.args.get("concurso")
    limite = request.args.get("limite", 50, type=int)

    # Query base - solo envíos de concursos activos
    query = {}
    if concurso_id:
        query["concurso"] = concurso_id

    # Obtener envíos ordenados por votos
    envios = Envio.objects(**query).order_by("-votos")[:limite]

    # Enriquecer datos para el template
    ranking = []
    for i, envio in enumerate(envios, 1):
        try:
            ranking.append({
                "posicion": i,
                "id": str(envio.id),
                "titulo": envio.titulo,
                "descripcion": envio.descripcion,
                "imagen_url": envio.imagen_url,
                "votos": envio.votos,
                "autor": envio.autor,
                "concurso": envio.concurso
            })
        except:
            continue

    # Obtener lista de concursos activos para el filtro
    concursos = Concurso.objects(activo=True, estado="activo")

    return render_template("user/ranking.html",
                         ranking=ranking,
                         concursos=concursos,
                         concurso_filtro=concurso_id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@envio_bp.route("/participar", methods=["POST"])
@jwt_requerido
def participar():
    """Subir obra a un concurso (Multipart/Form-data)."""
    # 1. Validar si hay archivo
    if 'archivo' not in request.files:
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400
    
    file = request.files['archivo']
    if file.filename == '':
        return jsonify({"error": "Archivo vacío"}), 400
    
    if file and allowed_file(file.filename):
        # Generar nombre único para evitar colisiones
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar archivo
        file.save(filepath)
        
        # 2. Obtener datos del formulario
        data = {
            "titulo": request.form.get("titulo"),
            "descripcion": request.form.get("descripcion"),
            "concurso_id": request.form.get("concurso_id"),
            "categoria_id": request.form.get("categoria_id"),
            "imagen_url": f"uploads/{filename}" # Ruta relativa para el frontend
        }
        
        # 3. Crear envío en DB
        envio, error = crear_envio(data, request.user["user_id"])
        
        if error:
            # Si falla la DB, borramos el archivo subido para no dejar basura
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": error}), 400
            
        return jsonify({
            "id": str(envio.id),
            "titulo": envio.titulo,
            "mensaje": "¡Has participado con éxito!"
        }), 201
    
    return jsonify({"error": "Extensión de archivo no permitida"}), 400


@envio_bp.route("", methods=["POST"])  # POST /envios
@jwt_requerido
def crear():
    """Crear nuevo envío a concurso (requiere JWT)."""
    from app.schemas.envio_esquema import EnvioCreateSchema

    schema = EnvioCreateSchema()
    data = schema.load(request.json)

    envio, error = crear_envio(data, request.user["user_id"])

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "id": str(envio.id),
        "titulo": envio.titulo,
        "mensaje": "Envío creado exitosamente"
    }), 201


@envio_bp.route("", methods=["GET"])  # GET /envios
def listar():
    """Listar envíos. Query params: concurso, categoria, autor."""
    concurso_id = request.args.get("concurso")
    categoria_id = request.args.get("categoria")
    autor_id = request.args.get("autor")

    envios = obtener_envios(concurso_id, categoria_id, autor_id)

    resultado = []
    for e in envios:
        resultado.append({
            "id": str(e.id),
            "titulo": e.titulo,
            "descripcion": e.descripcion,
            "imagen_url": e.imagen_url,
            "autor": str(e.autor.id),
            "concurso": str(e.concurso.id),
            "categoria": str(e.categoria.id),
            "votos": e.votos,
            "fecha_envio": e.fecha_envio.isoformat() if e.fecha_envio else None
        })

    return jsonify(resultado)


@envio_bp.route("/<envio_id>", methods=["GET"])  # GET /envios/<id>
def detalle(envio_id):
    """Obtener detalle de un envío con sus etiquetas."""
    envio = obtener_envio(envio_id)

    if not envio:
        return jsonify({"error": "Envío no encontrado"}), 404

    etiquetas = obtener_etiquetas_envio(envio_id)

    return jsonify({
        "id": str(envio.id),
        "titulo": envio.titulo,
        "descripcion": envio.descripcion,
        "imagen_url": envio.imagen_url,
        "autor": str(envio.autor.id),
        "concurso": str(envio.concurso.id),
        "categoria": str(envio.categoria.id),
        "votos": envio.votos,
        "fecha_envio": envio.fecha_envio.isoformat() if envio.fecha_envio else None,
        "etiquetas": [et.nombre for et in etiquetas]
    })


@envio_bp.route("/<envio_id>", methods=["PUT"])  # PUT /envios/<id>
@jwt_requerido
def actualizar(envio_id):
    """Actualizar envío propio (requiere JWT)."""
    from app.schemas.envio_esquema import EnvioUpdateSchema

    schema = EnvioUpdateSchema()
    data = schema.load(request.json)

    envio = actualizar_envio(envio_id, data, request.user["user_id"])

    if not envio:
        return jsonify({"error": "Envío no encontrado o no autorizado"}), 404

    return jsonify({
        "id": str(envio.id),
        "titulo": envio.titulo,
        "mensaje": "Envío actualizado"
    })


@envio_bp.route("/<envio_id>", methods=["DELETE"])  # DELETE /envios/<id>
@jwt_requerido
def eliminar(envio_id):
    """Eliminar envío propio (requiere JWT)."""
    if eliminar_envio(envio_id, request.user["user_id"]):
        return jsonify({"mensaje": "Envío eliminado"})

    return jsonify({"error": "Envío no encontrado o no autorizado"}), 404


@envio_bp.route("/<envio_id>/votar", methods=["POST"])  # POST /envios/<id>/votar
@jwt_requerido
def votar(envio_id):
    """Votar por un envío (requiere JWT, no auto-votos)."""
    envio, error = votar_envio(envio_id, request.user["user_id"])

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "id": str(envio.id),
        "votos": envio.votos,
        "mensaje": "Voto registrado"
    })


@envio_bp.route("/concurso/<concurso_id>/ranking", methods=["GET"])  # GET /envios/concurso/<id>/ranking
def ranking(concurso_id):
    """Obtener ranking de envíos por votos. Query param: limite (default 10)."""
    limite = request.args.get("limite", 10, type=int)
    envios = obtener_ranking(concurso_id, limite)

    resultado = []
    for i, e in enumerate(envios, 1):
        resultado.append({
            "posicion": i,
            "id": str(e.id),
            "titulo": e.titulo,
            "autor": str(e.autor.id),
            "votos": e.votos,
            "imagen_url": e.imagen_url
        })

    return jsonify(resultado)
