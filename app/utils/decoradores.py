from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import verificar_token

def jwt_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if not auth:
            return jsonify({"error": "Token requerido"}), 401

        token = auth.split(" ")[1]
        payload = verificar_token(token)

        if not payload:
            return jsonify({"error": "Token inválido"}), 401

        request.user = payload
        return f(*args, **kwargs)

    return wrapper