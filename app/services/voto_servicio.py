from app.models.voto import Voto
from app.models.notificacion import Notificacion
from app.models.envio import Envio

def votar(data, user_id):
    # Buscar envio
    envio = Envio.objects(id=data["submission_id"]).first()
    if not envio:
        return None, "Envío no encontrado"
    # Evitar votar por su propia obra
    if str(envio.autor.id) == user_id:
        return None, "No puedes votar por tu propia obra"

    # evitar doble voto
    existente = Voto.objects(user_id=user_id, submission_id=data["submission_id"]).first()
    if existente:
        return None, "Ya has votado por esta obra"

    voto = Voto(user_id=user_id, submission_id=data["submission_id"]).save()

    # Actualizar el contador de votos y la lista de votantes en el Envío
    envio.update(inc__votos=1, push__votantes=user_id)

    # Notificación al autor de la obra
    Notificacion(
        user_id=str(envio.autor.id),
        tipo="voto",
        mensaje=f"Tu obra '{envio.titulo}' recibió un voto"
    ).save()

    return voto, None