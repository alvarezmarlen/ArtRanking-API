from flask import Blueprint, jsonify, request
from app.models.usuario import Usuario
from app.utils.decoradores import jwt_requerido

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/me", methods=["GET"])
@jwt_requerido
def get_me():
    user = Usuario.objects(id=request.user["user_id"]).first()
    return jsonify({"email": user.email})


@usuario_bp.route("/me", methods=["PUT"])
@jwt_requerido
def update_me():
    user = Usuario.objects(id=request.user["user_id"]).first()
    data = request.json

    user.update(**data)
    return jsonify({"message": "Actualizado"})