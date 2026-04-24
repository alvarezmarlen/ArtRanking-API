from flask import Blueprint, request, jsonify, render_template
from app.services.auth_servicio import registrar_usuario, login_usuario

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
    user = registrar_usuario(request.json)
    return jsonify({"id": str(user.id)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    token = login_usuario(request.json)

    if not token:
        return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify({"token": token})