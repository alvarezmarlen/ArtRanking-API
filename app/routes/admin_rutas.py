from flask import Blueprint, render_template, jsonify, request, session
from bson import ObjectId
from datetime import datetime


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def dashboard():
    """Vista principal del dashboard administrativo."""
    return render_template("admin/dashboard.html")


@admin_bp.route("/concursos")
def concursos():
    from mongoengine.connection import get_db
    db = get_db()
    lista_concursos = list(db.concursos.find())
    return render_template("admin/concurso.html", concursos=lista_concursos)

@admin_bp.route("/api/concursos/<id>")
def obtener_concurso(id):
    from mongoengine.connection import get_db
    db = get_db()
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
    
    id_concurso = request.form.get("id")
    
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "estado": request.form.get("estado"),
        # AGREGAMOS ESTO: Para que MongoDB no rechace el guardado por falta de campos
        "fecha_inicio": datetime.utcnow(),
        "creado_por": ObjectId(session.get("user_id") or "69ea009812fd61d1004f74f8"),
        "categorias": []
    }

    try:
        if id_concurso and id_concurso != "" and id_concurso != "None":
            # MODIFICAR
            db.concursos.update_one(
                {'_id': ObjectId(id_concurso)},
                {'$set': {
                    "titulo": datos["titulo"],
                    "descripcion": datos["descripcion"],
                    "estado": datos["estado"]
                }}
            )
        else:
            # CREAR NUEVO
            db.concursos.insert_one(datos)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_bp.route("/api/concursos/eliminar/<id>", methods=["DELETE", "POST"])
def eliminar_concurso(id):
    from mongoengine.connection import get_db
    db = get_db()
    
    try:
        # Borramos el concurso físicamente de MongoDB
        resultado = db.concursos.delete_one({'_id': ObjectId(id)})
        
        if resultado.deleted_count > 0:
            return jsonify({"status": "success", "message": "Concurso eliminado"}), 200
        return jsonify({"status": "error", "message": "No se encontró el concurso"}), 404
        
    except Exception as e:
        print(f"Error al eliminar: {e}")
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
