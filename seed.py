import pymongo
from bson import ObjectId
from datetime import datetime

# 1. Configuración de la conexión a tu Docker
# Usamos localhost porque Compass ya te confirmó que funciona ahí
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["artranking"]

def seed_db():
    print("🚀 Iniciando la siembra de la base de datos...")

    # 2. Limpiar todas las colecciones existentes para evitar duplicados
    colecciones = [
        "usuario", "perfil", "concursos", "categorias", 
        "envios", "votos", "comentarios", "etiquetas", 
        "envio_etiquetas", "notificacion"
    ]
    
    for col in colecciones:
        db[col].drop()
        print(f"  - Colección '{col}' limpiada.")

    print("\n🌱 Insertando nuevos registros...")

    # 3. Crear Usuarios (Entidad base)
    admin_id = db.usuario.insert_one({
        "nombre": "Marlen Admin",
        "email": "marlen@art.com",
        "rol": "admin",
        "fecha_registro": datetime.utcnow()
    }).inserted_id

    artista_id = db.usuario.insert_one({
        "nombre": "Jorge Artista",
        "email": "jorge@art.com",
        "rol": "artista",
        "fecha_registro": datetime.utcnow()
    }).inserted_id    
    
    artista_id = db.usuario.insert_one({
        "nombre": "Jorge Artista",
        "email": "jorge@art.com",
        "rol": "musicante",
        "fecha_registro": datetime.utcnow()
    }).inserted_id

    # 4. Crear Categorías
    cat_pintura = db.categorias.insert_one({
        "nombre": "Pintura al Óleo",
        "descripcion": "Obras tradicionales con base de aceite"
    }).inserted_id

    # 5. Crear Etiquetas
    tag_id = db.etiquetas.insert_one({"nombre": "Paisaje"}).inserted_id

    # 6. Crear un Concurso (Relacionado con Admin y Categoría)
    concurso_id = db.concursos.insert_one({
        "titulo": "Certamen Bilbao Arte 2026",
        "descripcion": "Concurso para artistas locales",
        "estado": "activo",
        "creado_por": admin_id,
        "categorias": [cat_pintura],
        "fecha_inicio": datetime.utcnow()
    }).inserted_id

    # --- SEGUNDO CONCURSO ---
    concurso_id_2 = db.concursos.insert_one({
        "titulo": "Bizkaia en un Click",
        "descripcion": "Concurso de fotografía urbana y paisajes",
        "estado": "activo",
        "creado_por": admin_id,
        "categorias": [cat_pintura], # Puedes usar la misma o crear otra
        "fecha_inicio": datetime.utcnow(),
        "fecha_fin": datetime.utcnow(), # Recuerda que en tu modelo es obligatorio
        "activo": True
    }).inserted_id

    # 7. Crear un Envío (Relacionado con Artista y Concurso)
    envio_id = db.envios.insert_one({
        "titulo": "Atardecer en la Ría",
        "archivo_url": "/static/uploads/obra1.jpg",
        "artista_id": artista_id,
        "concurso_id": concurso_id,
        "votos_count": 0
    }).inserted_id

    # 8. Relacionar Envío con Etiquetas (Colección intermedia)
    db.envio_etiquetas.insert_one({
        "envio_id": envio_id,
        "etiqueta_id": tag_id
    })

    # 9. Crear un Voto
    db.votos.insert_one({
        "envio_id": envio_id,
        "usuario_id": admin_id,
        "fecha": datetime.utcnow()
    })

    print("\n✅ ¡Base de datos poblada exitosamente!")
    print("👉 Ve a MongoDB Compass y dale a 'Refresh' para ver los cambios.")

if __name__ == "__main__":
    seed_db()