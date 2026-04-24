from flask import Blueprint, render_template, jsonify, request
from bson import ObjectId

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def dashboard():
    """Vista principal del dashboard administrativo."""
    return render_template("admin/dashboard.html")

@admin_bp.route("/concursos")
def concursos():
    """Gestión de concursos (Placeholder)."""
    from mongoengine.connection import get_db
    db = get_db()
    lista_concursos = list(db.concursos.find())
    return render_template("admin/concurso.html", concursos=lista_concursos)

@admin_bp.route("/api/concursos/<id>")
def obtener_concurso(id):
    """Esta es la función para el botón EDITAR (la que usa el ID)."""
    from mongoengine.connection import get_db
    db = get_db()
    
    # Buscamos el concurso específico en MongoDB
    concurso = db.concursos.find_one({'_id': ObjectId(id)})
    
    if concurso:
        return jsonify({
            'titulo': concurso.get('titulo', ''),
            'descripcion': concurso.get('descripcion', ''),
            'estado': concurso.get('estado', 'activo')
        })
    return jsonify({'error': 'No encontrado'}), 404

@admin_bp.route("/api/concursos/guardar", methods=["POST"])
def guardar_concurso():
    from mongoengine.connection import get_db
    db = get_db()
    
    # Recogemos los datos que vienen del formulario
    id_concurso = request.form.get("id")
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    estado = request.form.get("estado")

    datos = {
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": estado
    }

    try:
        if id_concurso and id_concurso != "":
            # Si hay ID, es una EDICIÓN (Update)
            db.concursos.update_one(
                {'_id': ObjectId(id_concurso)},
                {'$set': datos}
            )
        else:
            # Si no hay ID, es uno NUEVO (Insert)
            db.concursos.insert_one(datos)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error al guardar: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route("/envios")
def envios():
    """Gestión de envíos (Placeholder)."""
    return render_template("admin/dashboard.html")

@admin_bp.route("/ranking")
def ranking():
    """Gestión de ranking (Placeholder)."""
    return render_template("admin/dashboard.html")

@admin_bp.route("/participantes")
def participantes():
    """Gestión de participantes (Placeholder)."""
    return render_template("admin/dashboard.html")
