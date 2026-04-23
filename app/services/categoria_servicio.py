"""
Servicio de Categorías.
Lógica de negocio para gestionar el catálogo maestro de categorías artísticas.
"""
from app.models.categoria import Categoria

def crear_categoria(data):
    """
    Crea una nueva categoría independiente.
    data: dict con nombre y descripcion
    Retorna: objeto Categoria guardado
    """
    categoria = Categoria(
        nombre=data["nombre"],
        descripcion=data.get("descripcion", "")
    ).save()
    return categoria

def obtener_categorias():
    """
    Lista todas las categorías del sistema.
    Retorna: QuerySet de Categoria
    """
    return Categoria.objects()

def obtener_categoria(categoria_id):
    """
    Busca una categoría por su ID.
    Retorna: Categoria o None si no existe
    """
    return Categoria.objects(id=categoria_id).first()

def actualizar_categoria(categoria_id, data):
    """
    Actualiza campos de una categoría.
    data: dict con campos a actualizar
    Retorna: Categoria actualizada o None
    """
    categoria = Categoria.objects(id=categoria_id).first()
    if not categoria:
        return None
    
    categoria.update(**data)
    categoria.reload()
    return categoria

def eliminar_categoria(categoria_id):
    """
    Elimina permanentemente una categoría.
    Retorna: True si se eliminó, False si no existe
    """
    categoria = Categoria.objects(id=categoria_id).first()
    if not categoria:
        return False
    
    categoria.delete()
    return True
