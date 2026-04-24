from app.models.usuario import Usuario
from app.utils.jwt_utils import generar_token
from werkzeug.security import generate_password_hash, check_password_hash

def registrar_usuario(data):
    # Verificar si el email ya existe
    usuario_existente = Usuario.objects(email=data["email"]).first()
    if usuario_existente:
        return None, "El email ya está registrado"

    password_hash = generate_password_hash(data["password"])

    user = Usuario(
        email=data["email"],
        password=password_hash,
        role="user" # Asegurar rol por defecto
    ).save()

    return user, None


def login_usuario(data):
    user = Usuario.objects(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return None

    return user #Devolvemos el objeto de usuario para manejarlo en la ruta