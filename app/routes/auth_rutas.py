from flask import Blueprint, request, jsonify, render_template
from app.services.auth_servicio import registrar_usuario, login_usuario
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro")
def registro_page():
    """Render registration page"""
    return render_template("user/auth/registro.html")

@auth_bp.route("/login")
def login_page():
    """Render login page"""
    return render_template("user/auth/login.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    from app.schemas.usuario_esquema import UsuarioSchema

    schema = UsuarioSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user, error = registrar_usuario(data)

    if error:
        return jsonify({"error": error}), 409

    return jsonify({"id": str(user.id)}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    token = login_usuario(request.json)

    if not token:
        return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify({"token": token})