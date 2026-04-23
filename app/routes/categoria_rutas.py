"""
Rutas de Categorías (Blueprint).
Endpoints REST para gestionar el catálogo maestro de categorías.
Prefijo URL: /categorias
"""
from flask import Blueprint, jsonify, request
from app.services.categoria_servicio import (
    crear_categoria,
    obtener_categorias,
    obtener_categoria,
    actualizar_categoria,
    eliminar_categoria
)
from app.utils.decoradores import jwt_requerido

categoria_bp = Blueprint("categoria", __name__)

@categoria_bp.route("", methods=["POST"])
@jwt_requerido
def crear():
    """Crear nueva categoría (requiere JWT)."""
    from app.schemas.envio_esquema import CategoriaSchema
    schema = CategoriaSchema()
    data = schema.load(request.json)
    
    categoria = crear_categoria(data)
    return jsonify({
        "id": str(categoria.id),
        "nombre": categoria.nombre,
        "mensaje": "Categoría creada exitosamente"
    }), 201

@categoria_bp.route("", methods=["GET"])
def listar():
    """Listar todas las categorías."""
    categorias = obtener_categorias()
    resultado = [{
        "id": str(c.id),
        "nombre": c.nombre,
        "descripcion": c.descripcion
    } for c in categorias]
    return jsonify(resultado)

@categoria_bp.route("/<categoria_id>", methods=["GET"])
def detalle(categoria_id):
    """Obtener detalle de una categoría."""
    categoria = obtener_categoria(categoria_id)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404
    
    return jsonify({
        "id": str(categoria.id),
        "nombre": categoria.nombre,
        "descripcion": categoria.descripcion
    })

@categoria_bp.route("/<categoria_id>", methods=["PUT"])
@jwt_requerido
def actualizar(categoria_id):
    """Actualizar categoría (requiere JWT)."""
    categoria = actualizar_categoria(categoria_id, request.json)
    if not categoria:
        return jsonify({"error": "Categoría no encontrada"}), 404
    
    return jsonify({
        "id": str(categoria.id),
        "nombre": categoria.nombre,
        "mensaje": "Categoría actualizada"
    })

@categoria_bp.route("/<categoria_id>", methods=["DELETE"])
@jwt_requerido
def eliminar(categoria_id):
    """Eliminar categoría (requiere JWT)."""
    if eliminar_categoria(categoria_id):
        return jsonify({"mensaje": "Categoría eliminada"})
    return jsonify({"error": "Categoría no encontrada"}), 404
