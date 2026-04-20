"""
Servicio de Concursos.
Lógica de negocio para gestionar concursos artísticos y sus categorías.
"""
from datetime import datetime
from app.models.concurso import Concurso
from app.models.categoria import Categoria


def crear_concurso(data, usuario_id):
    """
    Crea un nuevo concurso con sus categorías.
    data: dict con titulo, descripcion, fecha_inicio, fecha_fin, categorias (opcional)
    usuario_id: ID del admin que lo crea
    Retorna: objeto Concurso guardado
    """
    concurso = Concurso(
        titulo=data["titulo"],
        descripcion=data.get("descripcion", ""),
        fecha_inicio=data["fecha_inicio"],
        fecha_fin=data["fecha_fin"],
        creado_por=usuario_id
    ).save()

    if "categorias" in data:
        for cat_data in data["categorias"]:
            categoria = Categoria(
                nombre=cat_data["nombre"],
                descripcion=cat_data.get("descripcion", ""),
                concurso=concurso
            ).save()
            concurso.categorias.append(categoria)
        concurso.save()

    return concurso


def obtener_concursos(activos=True):
    """
    Lista concursos filtrando por activos/inactivos.
    activos=True: solo concursos activos y estado="activo"
    Retorna: QuerySet de Concurso
    """
    if activos:
        return Concurso.objects(activo=True, estado="activo")
    return Concurso.objects()


def obtener_concurso(concurso_id):
    """
    Busca un concurso por su ID.
    Retorna: Concurso o None si no existe
    """
    return Concurso.objects(id=concurso_id).first()


def actualizar_concurso(concurso_id, data):
    """
    Actualiza campos de un concurso.
    data: dict con campos a actualizar
    Retorna: Concurso actualizado o None
    """
    concurso = Concurso.objects(id=concurso_id).first()

    if not concurso:
        return None

    concurso.update(**data)
    concurso.reload()

    return concurso


def eliminar_concurso(concurso_id):
    """
    Elimina lógicamente un concurso (soft delete).
    Marca activo=False y estado="cancelado"
    Retorna: True si se eliminó, False si no existe
    """
    concurso = Concurso.objects(id=concurso_id).first()

    if not concurso:
        return False

    concurso.activo = False
    concurso.estado = "cancelado"
    concurso.save()

    return True


def cambiar_estado_concurso(concurso_id, nuevo_estado):
    """
    Cambia el estado del concurso (activo, cerrado, cancelado).
    Retorna: Concurso actualizado o None
    """
    concurso = Concurso.objects(id=concurso_id).first()

    if not concurso:
        return None

    concurso.estado = nuevo_estado
    concurso.save()

    return concurso


def agregar_categoria(concurso_id, data):
    """
    Agrega una categoría a un concurso existente.
    data: dict con nombre y descripcion de la categoría
    Retorna: Categoria creada o None si no existe el concurso
    """
    concurso = Concurso.objects(id=concurso_id).first()

    if not concurso:
        return None

    categoria = Categoria(
        nombre=data["nombre"],
        descripcion=data.get("descripcion", ""),
        concurso=concurso
    ).save()

    concurso.categorias.append(categoria)
    concurso.save()

    return categoria


def obtener_categorias_concurso(concurso_id):
    """
    Obtiene todas las categorías de un concurso.
    Retorna: lista de Categoria o None si no existe el concurso
    """
    concurso = Concurso.objects(id=concurso_id).first()

    if not concurso:
        return None

    return concurso.categorias
