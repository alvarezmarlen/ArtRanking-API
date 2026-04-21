from app.models.voto import Voto
from app.models.notificacion import Notificacion

def votar(user_id, submission_id):
    # evitar doble voto
    existente = Voto.objects(user_id=user_id, submission_id=submission_id).first()
    if existente:
        return None

    voto = Voto(user_id=user_id, submission_id=submission_id).save()

    # notificación mock
    Notificacion(
        user_id="owner_mock",
        tipo="voto",
        mensaje="Tu obra recibió un voto"
    ).save()

    return voto