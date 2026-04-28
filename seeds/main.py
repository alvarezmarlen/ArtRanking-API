
import os
import sys
from mongoengine import connect, disconnect
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.concurso import Concurso
from app.models.envio import Envio
from app.models.voto import Voto
from app.models.comentario import Comentario
from app.models.etiqueta import Etiqueta
from app.models.envio_etiqueta import EnvioEtiqueta
from app.models.notificacion import Notificacion
from app.models.perfil import Perfil

def run_seeds():
    print("Iniciando carga de seeds...")
    
    # Conexión a la base de datos
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/artranking')
    disconnect()
    connect(host=mongo_uri)
    
    # Limpiar base de datos (Opcional, pero recomendado para seeds limpios)
    print("Limpiando colecciones...")
    Usuario.objects().delete()
    Categoria.objects().delete()
    Concurso.objects().delete()
    Envio.objects().delete()
    Voto.objects().delete()
    Comentario.objects().delete()
    Etiqueta.objects().delete()
    EnvioEtiqueta.objects().delete()
    Notificacion.objects().delete()
    Perfil.objects().delete()

    # 1. Usuarios
    print("Creando usuarios...")
    usuarios = []
    roles = ["admin", "user", "user", "user", "user", "user"]
    for i in range(6):
        u = Usuario(
            email=f"user{i}@test.com",
            password=generate_password_hash("password123"),
            role=roles[i]
        ).save()
        usuarios.append(u)
    
    # 2. Perfiles
    print("Creando perfiles...")
    for u in usuarios:
        Perfil(
            usuario=u,
            nombre=f"Nombre {u.email.split('@')[0]}",
            bio=f"Esta es la biografía del usuario {u.email}",
            avatar="https://via.placeholder.com/150"
        ).save()

    # 3. Categorías
    print("Creando categorías...")
    categorias_nombres = ["Dibujo Digital", "Escultura", "Pintura al Óleo", "Acuarela", "Arte 3D"]
    categorias = []
    for nombre in categorias_nombres:
        cat = Categoria(
            nombre=nombre,
            descripcion=f"Categoría dedicada a {nombre}"
        ).save()
        categorias.append(cat)

    # 4. Etiquetas
    print("Creando etiquetas...")
    etiquetas_nombres = ["Retrato", "Paisaje", "Oscuro", "Colorido", "Minimalista", "Surrealista"]
    etiquetas = []
    for nombre in etiquetas_nombres:
        et = Etiqueta(nombre=nombre).save()
        etiquetas.append(et)

    # 5. Concursos (Comics, Manga, Fotografía)
    print("Creando concursos...")
    concursos_data = [
        {"titulo": "Gran Concurso de Comics 2026", "desc": "Saca tu lado superhéroe."},
        {"titulo": "Manga Fest: Shonen vs Shojo", "desc": "El mejor dibujo estilo japonés."},
        {"titulo": "Fotografía Urbana: Luces y Sombras", "desc": "Captura la esencia de la ciudad."},
        {"titulo": "Comics Retro: Años 90", "desc": "Vuelve a la era de los 90."},
        {"titulo": "Manga de Terror: Junji Ito Style", "desc": "Terror en blanco y negro."},
        {"titulo": "Fotografía de Naturaleza", "desc": "La belleza de lo salvaje."}
    ]
    concursos = []
    for i, data in enumerate(concursos_data):
        c = Concurso(
            titulo=data["titulo"],
            descripcion=data["desc"],
            fecha_inicio=datetime.utcnow(),
            fecha_fin=datetime.utcnow() + timedelta(days=30),
            creado_por=usuarios[0], # El admin
            categorias=[categorias[0], categorias[1]],
            estado="activo",
            activo=True
        ).save()
        concursos.append(c)

    # 6. Envíos (Obras)
    print("Creando envíos...")
    envios = []
    for i in range(10):
        envio = Envio(
            titulo=f"Obra Maestra #{i+1}",
            descripcion=f"Descripción de la obra maestra número {i+1}",
            imagen_url=f"https://picsum.photos/seed/art{i}/800/600",
            autor=usuarios[i % 5 + 1], # Distribuir entre usuarios no-admin
            concurso=concursos[i % len(concursos)],
            categoria=categorias[i % len(categorias)],
            votos=0
        ).save()
        envios.append(envio)

    # 7. Votos
    print("Creando votos...")
    for i in range(15):
        v = Voto(
            usuario=usuarios[i % 6],
            envio=envios[i % 10],
            value=1
        ).save()
        # Actualizar contador de votos en el envío
        envio_target = envios[i % 10]
        envio_target.votos += 1
        envio_target.save()

    # 8. Comentarios
    print("Creando comentarios...")
    for i in range(10):
        Comentario(
            usuario=usuarios[i % 6],
            envio=envios[i % 10],
            texto=f"¡Increíble trabajo! Me encanta el detalle #{i+1}"
        ).save()

    # 9. EnvioEtiquetas (Relación)
    print("Creando relaciones Envio-Etiqueta...")
    for i in range(15):
        EnvioEtiqueta(
            envio=envios[i % 10],
            etiqueta=etiquetas[i % 6]
        ).save()

    # 10. Notificaciones
    print("Creando notificaciones...")
    for i in range(10):
        Notificacion(
            user_id=str(usuarios[i % 6].id),
            tipo="voto" if i % 2 == 0 else "comentario",
            mensaje=f"Has recibido un {'voto' if i % 2 == 0 else 'comentario'} en tu obra.",
            leido=False
        ).save()

    print("\n¡Seeds cargados con éxito!")
    print(f"- Usuarios: {Usuario.objects.count()}")
    print(f"- Concursos: {Concurso.objects.count()}")
    print(f"- Envíos: {Envio.objects.count()}")
    print(f"- Categorías: {Categoria.objects.count()}")

if __name__ == "__main__":
    run_seeds()
