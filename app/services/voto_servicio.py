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
    # Comprobamos tanto en la colección Voto como en la lista de votantes del Envio
    existente = Voto.objects(usuario=user_id, envio=data["submission_id"]).first()
    if existente or user_id in [str(v.id) if hasattr(v, 'id') else str(v) for v in envio.votantes]:
        return None, "Ya has votado por esta obra"

    # Crear el voto
    voto = Voto(usuario=user_id, envio=envio).save()

    # Actualizar el contador de votos y la lista de votantes en el Envío
    # Obtenemos el objeto usuario para la lista de referencias
    from app.models.usuario import Usuario
    usuario_vota = Usuario.objects(id=user_id).first()
    
    if usuario_vota:
        if usuario_vota not in envio.votantes:
            envio.votantes.append(usuario_vota)
            envio.votos = (envio.votos or 0) + 1
            envio.save()

    # Notificación al autor de la obra
    Notificacion(
        user_id=str(envio.autor.id),
        tipo="voto",
        mensaje=f"Tu obra '{envio.titulo}' recibió un voto"
    ).save()

    return voto, None