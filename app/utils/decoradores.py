from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import verificar_token

def jwt_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Buscar token en cabeceras o cookies
        token = request.cookies.get("access_token")
        auth = request.headers.get("Authorization")
        
        if auth and " " in auth:
            token = auth.split(" ")[1]

        if not token:
            return jsonify({"error": "Sesión requerida"}), 401

        payload = verificar_token(token)
        if not payload:
            return jsonify({"error": "Sesión expirada o inválida"}), 401

        request.user = payload
        return f(*args, **kwargs)

    return wrapper