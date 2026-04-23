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
    data = schema.load(request.json)

    voto, error = votar(data, request.user["user_id"])

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Voto registrado"})

# comentarios
@voto_bp.route("/comentarios", methods=["POST"])
def comentar():
    from app.models.comentario import Comentario

    data = request.json

    comentario = Comentario(
        user_id=data["user_id"],
        submission_id=data["submission_id"],
        texto=data["texto"]
    ).save()

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
