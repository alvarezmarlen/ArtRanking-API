from flask import Blueprint, request, jsonify
from app.services.voto_servicio import votar
from app.utils.decoradores import jwt_requerido

voto_bp = Blueprint("votos", __name__)


# votos
@voto_bp.route("/", methods=["POST"])
@jwt_requerido
def crear_voto():
    """Crear nuevo voto a concurso (requiere JWT)."""
    from app.schemas.voto_esquema import VotoSchema
    schema = VotoSchema()
    
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({"error": "Datos inválidos"}), 400

    voto, error = votar(data, request.user["user_id"])

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Voto registrado"})

# comentarios
@voto_bp.route("/comentarios", methods=["POST"])
@jwt_requerido
def comentar():
    from app.models.comentario import Comentario

    data = request.json
    user_id = request.user["user_id"]

    try:
        comentario = Comentario(
            usuario=user_id,
            envio=data["submission_id"],
            texto=data["texto"]
        ).save()
    except Exception as e:
        return jsonify({"error": "Error al guardar comentario"}), 400

    return jsonify({"message": "Comentario añadido"})

# Notificaciones
@voto_bp.route("/notificaciones/<user_id>")
def get_notificaciones(user_id):
    from app.models.notificacion import Notificacion

    notis = Notificacion.objects(user_id=user_id)

    return jsonify([{
        "mensaje": n.mensaje,
        "leido": n.leido
    } for n in notis])
