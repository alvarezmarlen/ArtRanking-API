from bson import ObjectId
from datetime import datetime
from mongoengine.connection import get_db
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash
from mongoengine.errors import ValidationError

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
    db = get_db()
    concurso = db.concursos.find_one({'_id': ObjectId(id)})
    if concurso:
        return jsonify({
            'titulo': concurso.get('titulo', ''),
            'descripcion': concurso.get('descripcion', ''),
            'estado': concurso.get('estado', 'activo'),
            # Enviamos las fechas en formato ISO para que JS las lea fácil
            'fecha_inicio': concurso.get('fecha_inicio').isoformat() if concurso.get('fecha_inicio') else '',
            'fecha_fin': concurso.get('fecha_fin').isoformat() if concurso.get('fecha_fin') else ''
        })
    return jsonify({'error': 'No encontrado'}), 404


@admin_bp.route("/api/concursos/guardar", methods=["POST"])
def guardar_concurso():  
    db = get_db()
    admin_id = session.get("user_id")
    id_concurso = request.form.get("id")

    # CAPTURAMOS LAS FECHAS DEL FORMULARIO
    f_inicio_str = request.form.get("fecha_inicio")
    f_fin_str = request.form.get("fecha_fin")

    # Convertimos el texto del calendario a fecha de Python
    try:
        f_inicio = datetime.strptime(f_inicio_str, '%Y-%m-%d') if f_inicio_str else datetime.utcnow()
        f_fin = datetime.strptime(f_fin_str, '%Y-%m-%d') if f_fin_str else datetime(2025, 12, 31)
    except ValueError:
        return jsonify({"status": "error", "message": "Formato de fecha inválido"}), 400

    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "estado": request.form.get("estado", "activo"),
        "creado_por": ObjectId(admin_id),
        "fecha_inicio": f_inicio, # Ya no es automático, es lo que tú elijas
        "fecha_fin": f_fin,       # Ya no es automático, es lo que tú elijas
        "categorias": [],
        "activo": True,  
        "fecha_creacion": datetime.utcnow()
    }

    try:
        if id_concurso and id_concurso not in ["", "None", "undefined"]:
            db.concursos.update_one(
                {'_id': ObjectId(id_concurso)},
                {'$set': {
                    "titulo": datos["titulo"],
                    "descripcion": datos["descripcion"],
                    "estado": datos["estado"],
                    "fecha_inicio": datos["fecha_inicio"],
                    "fecha_fin": datos["fecha_fin"]
                }}
            )
        else:
            db.concursos.insert_one(datos)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
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

@admin_bp.route("/usuarios")
def usuarios():
    """Gestión de usuarios."""
    usuarios_list = Usuario.objects().filter(role='admin').all()
    return render_template("admin/usuarios.html", usuarios=usuarios_list)

@admin_bp.route("/usuarios/crear", methods=["POST"])
def usuarios_crear():
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    if Usuario.objects(email=email).first():
        flash("El email ya está registrado", "error")
        return redirect(url_for("admin.usuarios"))

    try:
        Usuario(
            email=email,
            password=generate_password_hash(password),
            role=role
        ).save()
        flash("Usuario creado exitosamente", "success")
    except ValidationError as e:
        # Aquí capturamos el error de MongoEngine
        flash(f"Error de validación: Formato de correo electrónico no válido.", "error")
    except Exception as e:
        flash(f"Ocurrió un error inesperado.", "error")
    return redirect(url_for("admin.usuarios"))

@admin_bp.route("/usuarios/editar/<id>", methods=["POST"])
def usuarios_editar(id):
    user = Usuario.objects(id=id).first()
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("admin.usuarios"))

    email = request.form.get("email")
    role = request.form.get("role")
    password = request.form.get("password")

    # Verificar si el email ya existe en otro usuario
    if email != user.email and Usuario.objects(email=email).first():
        flash("El nuevo email ya está en uso", "error")
        return redirect(url_for("admin.usuarios"))

    user.email = email
    user.role = role
    if password:
        user.password = generate_password_hash(password)
    
    user.save()
    flash("Usuario actualizado correctamente", "success")
    return redirect(url_for("admin.usuarios"))

@admin_bp.route("/usuarios/eliminar/<id>", methods=["POST"])
def usuarios_eliminar(id):
    user = Usuario.objects(id=id).first()
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("admin.usuarios"))

    # Evitar que un admin se elimine a sí mismo si fuera necesario, 
    # pero por simplicidad permitimos borrar cualquiera por ahora.
    user.delete()
    flash("Usuario eliminado correctamente", "success")
    return redirect(url_for("admin.usuarios"))

