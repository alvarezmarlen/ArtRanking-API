"""
Rutas de Concursos (Blueprint).
Endpoints REST para gestionar concursos artísticos.
Prefijo URL: /concursos
"""
from flask import Blueprint, jsonify, request, render_template, g
from app.models.envio import Envio
from app.models.concurso import Concurso
from app.services.concurso_servicio import (
    crear_concurso,
    obtener_concursos,
    obtener_concurso,
    actualizar_concurso,
    eliminar_concurso,
    cambiar_estado_concurso,
    agregar_categoria,
    obtener_categorias_concurso
)
from app.utils.decoradores import jwt_requerido

concurso_bp = Blueprint("concurso", __name__)


@concurso_bp.route("", methods=["POST"])  # POST /concursos
@jwt_requerido
def crear():
    """Crear nuevo concurso (requiere JWT)."""
    from app.schemas.envio_esquema import ConcursoCreateSchema

    schema = ConcursoCreateSchema()
    data = schema.load(request.json)

    concurso = crear_concurso(data, request.user["user_id"])

    return jsonify({
        "id": str(concurso.id),
        "titulo": concurso.titulo,
        "mensaje": "Concurso creado exitosamente"
    }), 201


@concurso_bp.route("", methods=["GET"])  # GET /concursos (HTML Page - Public)
def listar_pagina():
    """Render página de lista de concursos (HTML). Público, no requiere JWT."""
    # Obtener parámetro de filtro (activos o todos)
    mostrar_activos = request.args.get("activos", "true").lower() == "true"

    # Obtener concursos según filtro
    if mostrar_activos:
        concursos = Concurso.objects(activo=True, estado="activo")
    else:
        concursos = Concurso.objects(activo=True)

    return render_template("user/concursos/lista.html",
                         concursos=concursos,
                         mostrar_activos=mostrar_activos)


@concurso_bp.route("/api", methods=["GET"])  # GET /concursos/api (API JSON)
@jwt_requerido
def listar_api():
    """Listar concursos (API JSON). Query param: activos=true/false. Requiere JWT."""
    activos = request.args.get("activos", "true").lower() == "true"
    concursos = obtener_concursos(activos)

    resultado = []
    for c in concursos:
        resultado.append({
            "id": str(c.id),
            "titulo": c.titulo,
            "descripcion": c.descripcion,
            "estado": c.estado,
            "fecha_inicio": c.fecha_inicio.isoformat() if c.fecha_inicio else None,
            "fecha_fin": c.fecha_fin.isoformat() if c.fecha_fin else None,
            "categorias": [str(cat.id) for cat in c.categorias]
        })

    return jsonify(resultado)


@concurso_bp.route("/<concurso_id>/detalle", methods=["GET"])  # GET /concursos/<id>/detalle (HTML Page)
def detalle_pagina(concurso_id):
    """Render página de detalle de concurso (HTML)."""
    concurso = obtener_concurso(concurso_id)

    if not concurso:
        return render_template("common/errores/404.html"), 404

    return render_template("user/concursos/detalle.html", concurso=concurso)


@concurso_bp.route("/<concurso_id>", methods=["GET"])  # GET /concursos/<id> (API)
def detalle(concurso_id):
    """Obtener detalle de un concurso con sus categorías (API JSON)."""
    concurso = obtener_concurso(concurso_id)

    if not concurso:
        return jsonify({"error": "Concurso no encontrado"}), 404

    return jsonify({
        "id": str(concurso.id),
        "titulo": concurso.titulo,
        "descripcion": concurso.descripcion,
        "estado": concurso.estado,
        "fecha_inicio": concurso.fecha_inicio.isoformat() if concurso.fecha_inicio else None,
        "fecha_fin": concurso.fecha_fin.isoformat() if concurso.fecha_fin else None,
        "creado_por": str(concurso.creado_por.id),
        "categorias": [{
            "id": str(cat.id),
            "nombre": cat.nombre,
            "descripcion": cat.descripcion
        } for cat in concurso.categorias]
    })


@concurso_bp.route("/<concurso_id>", methods=["PUT"])  # PUT /concursos/<id>
@jwt_requerido
def actualizar(concurso_id):
    """Actualizar concurso (requiere JWT)."""
    concurso = actualizar_concurso(concurso_id, request.json)

    if not concurso:
        return jsonify({"error": "Concurso no encontrado"}), 404

    return jsonify({
        "id": str(concurso.id),
        "titulo": concurso.titulo,
        "mensaje": "Concurso actualizado"
    })


@concurso_bp.route("/<concurso_id>", methods=["DELETE"])  # DELETE /concursos/<id>
@jwt_requerido
def eliminar(concurso_id):
    """Eliminar concurso (soft delete, requiere JWT)."""
    if eliminar_concurso(concurso_id):
        return jsonify({"mensaje": "Concurso eliminado"})

    return jsonify({"error": "Concurso no encontrado"}), 404


@concurso_bp.route("/<concurso_id>/estado", methods=["PATCH"])  # PATCH /concursos/<id>/estado
@jwt_requerido
def cambiar_estado(concurso_id):
    """Cambiar estado del concurso: activo, cerrado, cancelado."""
    nuevo_estado = request.json.get("estado")

    if not nuevo_estado:
        return jsonify({"error": "Estado requerido"}), 400

    concurso = cambiar_estado_concurso(concurso_id, nuevo_estado)

    if not concurso:
        return jsonify({"error": "Concurso no encontrado"}), 404

    return jsonify({
        "id": str(concurso.id),
        "estado": concurso.estado,
        "mensaje": f"Estado cambiado a {nuevo_estado}"
    })


@concurso_bp.route("/<concurso_id>/categorias", methods=["POST"])  # POST /concursos/<id>/categorias
@jwt_requerido
def agregar_cat(concurso_id):
    """Vincular categoría existente a un concurso (requiere JWT)."""
    categoria_id = request.json.get("categoria_id")

    if not categoria_id:
        return jsonify({"error": "categoria_id requerido"}), 400

    categoria = agregar_categoria(concurso_id, categoria_id)

    if not categoria:
        return jsonify({"error": "Concurso o Categoría no encontrados"}), 404

    return jsonify({
        "id": str(categoria.id),
        "nombre": categoria.nombre,
        "mensaje": "Categoría vinculada al concurso"
    }), 201


@concurso_bp.route("/<concurso_id>/categorias", methods=["GET"])  # GET /concursos/<id>/categorias
def listar_categorias(concurso_id):
    """Listar categorías de un concurso."""
    categorias = obtener_categorias_concurso(concurso_id)

    if categorias is None:
        return jsonify({"error": "Concurso no encontrado"}), 404

    return jsonify([{
        "id": str(c.id),
        "nombre": c.nombre,
        "descripcion": c.descripcion
    } for c in categorias])
