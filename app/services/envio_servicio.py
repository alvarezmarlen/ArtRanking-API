"""
Servicio de Envíos (Submissions).
Lógica de negocio para gestionar envíos de obras a concursos.
"""
from app.models.envio import Envio
from app.models.concurso import Concurso
from app.models.categoria import Categoria
from app.models.etiqueta import Etiqueta
from app.models.envio_etiqueta import EnvioEtiqueta
from bson import ObjectId


def crear_envio(data, usuario_id):
    """
    Crea un nuevo envío a concurso.
    Valida que el concurso esté activo y la categoría pertenezca al concurso.
    Crea etiquetas automáticamente si no existen.
    Retorna: (Envio, None) o (None, mensaje_error)
    """
    concurso = Concurso.objects(id=data["concurso_id"]).first()

    if not concurso or not concurso.activo:
        return None, "Concurso no encontrado o inactivo"

    # Validar si el usuario ya participó en este concurso
    ya_participo = Envio.objects(autor=usuario_id, concurso=concurso.id).first()
    if ya_participo:
        return None, "Ya has participado en este concurso"

    categoria = Categoria.objects(id=data["categoria_id"]).first()

    if not categoria:
        return None, "Categoría no encontrada"

    if categoria not in concurso.categorias:
        return None, "Categoría no pertenece al concurso"

    envio = Envio(
        titulo=data["titulo"],
        descripcion=data.get("descripcion", ""),
        imagen_url=data["imagen_url"],
        autor=usuario_id,
        concurso=concurso.id,
        categoria=categoria.id
    ).save()

    if "etiquetas" in data:
        for tag_nombre in data["etiquetas"]:
            etiqueta = Etiqueta.objects(nombre=tag_nombre).first()

            if not etiqueta:
                etiqueta = Etiqueta(nombre=tag_nombre).save()

            EnvioEtiqueta(
                envio=envio,
                etiqueta=etiqueta
            ).save()

    return envio, None


def obtener_envios(concurso_id=None, categoria_id=None, autor_id=None):
    """
    Lista envíos con filtros opcionales.
    Ordenados por votos desc, luego fecha desc.
    Retorna: QuerySet de Envio
    """
    query = {}

    if concurso_id:
        query["concurso"] = ObjectId(concurso_id)

    if categoria_id:
        query["categoria"] = ObjectId(categoria_id)

    if autor_id:
        query["autor"] = ObjectId(autor_id)

    return Envio.objects(**query).order_by("-votos", "-fecha_envio")


def obtener_envio(envio_id):
    """
    Busca un envío por su ID.
    Retorna: Envio o None
    """
    return Envio.objects(id=envio_id).first()


def actualizar_envio(envio_id, data, usuario_id):
    """
    Actualiza un envío solo si el usuario es el autor.
    Retorna: Envio actualizado o None
    """
    envio = Envio.objects(id=envio_id, autor=usuario_id).first()

    if not envio:
        return None

    envio.update(**data)
    envio.reload()

    return envio


def eliminar_envio(envio_id, usuario_id):
    """
    Elimina un envío y sus relaciones de etiquetas.
    Solo el autor puede eliminarlo.
    Retorna: True/False
    """
    envio = Envio.objects(id=envio_id, autor=usuario_id).first()

    if not envio:
        return False

    EnvioEtiqueta.objects(envio=envio).delete()
    envio.delete()

    return True


def votar_envio(envio_id, usuario_id):
    """
    Registra un voto para un envío.
    Valida que no sea duplicado ni auto-voto.
    Retorna: (Envio, None) o (None, mensaje_error)
    """
    envio = Envio.objects(id=envio_id).first()

    if not envio:
        return None, "Envío no encontrado"

    if usuario_id in [str(v.id) for v in envio.votantes]:
        return None, "Ya has votado este envío"

    if str(envio.autor.id) == str(usuario_id):
        return None, "No puedes votar tu propio envío"

    envio.votos += 1
    envio.votantes.append(ObjectId(usuario_id))
    envio.save()

    return envio, None


def obtener_etiquetas_envio(envio_id):
    """
    Obtiene todas las etiquetas asociadas a un envío.
    Retorna: lista de Etiqueta
    """
    relaciones = EnvioEtiqueta.objects(envio=envio_id)
    return [rel.etiqueta for rel in relaciones]


def obtener_ranking(concurso_id, limite=10):
    """
    Obtiene el ranking de envíos por votos en un concurso.
    limite: cuántos resultados traer (default 10)
    Retorna: lista ordenada de Envio
    """
    return Envio.objects(concurso=concurso_id).order_by("-votos")[:limite]
