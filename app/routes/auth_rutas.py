from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response, flash
from app.services.auth_servicio import registrar_usuario, login_usuario
from marshmallow import ValidationError
from app.utils.jwt_utils import generar_token   

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro")
def registro_page():
    """Render registration page"""
    return render_template("user/auth/registro.html")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Render login page"""
    return render_template("user/auth/login.html")



@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    if password != password_confirm:
        flash("Las contraseñas no coinciden", "error")
        return redirect(url_for("auth.registro_page"))
    user, error = registrar_usuario({"email": email, "password": password})
    if error:
        flash(error, "error")
        return redirect(url_for("auth.registro_page"))
    # Login automático tras registro
    token = generar_token(user)
    response = make_response(redirect(url_for("home")))
    response.set_cookie("access_token", token, httponly=True, samesite='Lax')
    flash("Cuenta creada exitosamente", "success")
    return response

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form
    user = login_usuario(data)
    if not user:
        flash("Credenciales inválidas", "error")
        return redirect(url_for("auth.login_page"))
    token = generar_token(user)

     # --- LOGICA DE REDIRECCIÓN POR ROL ---
    if user.role == "admin":
        target_url = url_for("admin.dashboard")
    else:
        target_url = url_for("home")
    # -------------------------------------

    response = make_response(redirect(target_url))
    # Seteamos la cookie HttpOnly
    response.set_cookie("access_token", token, httponly=True, samesite='Lax')
    flash(f"Bienvenido de nuevo, {user.email}", "success")
    return response

@auth_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("home")))
    response.delete_cookie("access_token")
    flash("Sesión cerrada", "info")
    return response