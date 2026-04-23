from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def dashboard():
    """Vista principal del dashboard administrativo."""
    return render_template("admin/dashboard.html")

@admin_bp.route("/concursos")
def concursos():
    """Gestión de concursos (Placeholder)."""

    return render_template("admin/concurso.html")

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
