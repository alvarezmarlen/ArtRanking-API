from flask import Blueprint, request, jsonify
from app.services.voto_servicio import votar

voto_bp = Blueprint("votos", __name__)


# votos
@voto_bp.route("/", methods=["POST"])
def crear_voto():
    data = request.json

    voto = votar(data["user_id"], data["submission_id"])

    if not voto:
        return jsonify({"error": "Ya votaste"}), 400

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
