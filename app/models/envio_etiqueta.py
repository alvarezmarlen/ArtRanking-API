from mongoengine import Document, ReferenceField
from app.models.envio import Envio
from app.models.etiqueta import Etiqueta


class EnvioEtiqueta(Document):
    """
    Modelo de relación Envio-Etiqueta (Many-to-Many).
    Conecta un envío con sus etiquetas.
    Permite que un envío tenga múltiples etiquetas
    y una etiqueta esté en múltiples envíos.
    """
    # envio: obra etiquetada
    # etiqueta: palabra clave asignada
    envio = ReferenceField(Envio, required=True)
    etiqueta = ReferenceField(Etiqueta, required=True)

    meta = {
        "collection": "envio_etiquetas"  # nombre de la colección en MongoDB
    }
