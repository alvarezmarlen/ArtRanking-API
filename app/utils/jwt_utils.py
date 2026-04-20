import jwt
import datetime
from flask import current_app

def generar_token(usuario):
    payload = {
        "user_id": str(usuario.id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def verificar_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except:
        return None