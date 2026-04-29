"""
================================================================================
TESTS SIMPLES - ArtRanking
================================================================================
Tests básicos para verificar que la aplicación funciona.

EJECUTAR:
    pytest tests/test_simple.py -v
================================================================================
"""

# Importamos pytest para hacer tests
import pytest
# Importamos sys y os para rutas
import sys
import os

# Agregamos la ruta principal para importar la app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos create_app de la app Flask
from app import create_app
# Importamos TestConfig para tests
from config import TestConfig
# Importamos mongomock para simular base de datos
import mongomock


# =============================================================================
# CONFIGURACIÓN
# =============================================================================
# Fixtures son funciones que pytest ejecuta antes de cada test
# Preparan el entorno para testing

@pytest.fixture
def app():
    """
    Crea la app para testing
    Este fixture se ejecuta antes de cada test
    """
    # Usamos mongomock para no necesitar base de datos real
    TestConfig.MONGO_CLIENT_CLASS = mongomock.MongoClient
    # Creamos la app Flask
    app = create_app(TestConfig)
    return app


@pytest.fixture
def cliente(app):
    """
    Crea un cliente HTTP para hacer peticiones
    Simula un navegador
    """
    # test_client() crea un cliente de prueba
    return app.test_client()


# =============================================================================
# TESTS DE PÁGINAS
# =============================================================================
# Estos tests verifican que las páginas carguen bien
# No necesitan login ni base de datos

class TestPaginasPublicas:
    """Tests para páginas públicas"""
    
    def test_pagina_inicio_carga(self, cliente):
        """Verifica que la página de inicio carga"""
        # cliente.get('/') hace petición a la ruta principal
        respuesta = cliente.get('/')
        # Verificamos que el código sea 200 (OK)
        assert respuesta.status_code == 200
    
    def test_pagina_concursos_carga(self, cliente):
        """Verifica que la página de concursos carga"""
        respuesta = cliente.get('/concursos')
        assert respuesta.status_code == 200
    
    def test_pagina_ranking_carga(self, cliente):
        """Verifica que la página de ranking carga"""
        respuesta = cliente.get('/envios/ranking')
        assert respuesta.status_code == 200
    
    def test_pagina_login_carga(self, cliente):
        """Verifica que la página de login carga"""
        respuesta = cliente.get('/auth/login')
        assert respuesta.status_code == 200
    
    def test_pagina_registro_carga(self, cliente):
        """Verifica que la página de registro carga"""
        respuesta = cliente.get('/auth/registro')
        assert respuesta.status_code == 200


# =============================================================================
# TESTS DE API
# =============================================================================
# Estos tests verifican las APIs
# Algunos necesitan login, otros son públicos

class TestAPIs:
    """Tests para APIs"""
    
    def test_api_concursos_requiere_auth(self, cliente):
        """Verifica que la API de concursos necesita login"""
        respuesta = cliente.get('/concursos/api')
        # Debe redirigir (302) o rechazar (401) si no hay login
        assert respuesta.status_code in [302, 401]
    
    def test_api_envios_lista_publica(self, cliente):
        """Verifica que la lista de envíos es pública"""
        respuesta = cliente.get('/envios')
        # Esta API es pública
        assert respuesta.status_code == 200


# =============================================================================
# TESTS DE ERRORES
# =============================================================================
# Estos tests verifican errores
# Como páginas no encontradas (404)

class TestErrores:
    """Tests para errores"""
    
    def test_pagina_no_existente_404(self, cliente):
        """Verifica que páginas inexistentes dan 404"""
        respuesta = cliente.get('/pagina-que-no-existe')
        # Aceptamos 404 o 302 (redirect a home)
        assert respuesta.status_code in [404, 302]
    
    def test_concurso_no_existente_404(self, cliente):
        """Verifica que concurso inexistente da 404"""
        # Usamos un ID válido que no existe
        respuesta = cliente.get('/concursos/507f1f77bcf86cd799439011/detalle')
        assert respuesta.status_code == 404


# =============================================================================
# TESTS DE MODELOS
# =============================================================================
# Estos tests verifican que los modelos se crean bien
# No guardan en base de datos, solo en memoria

class TestModelos:
    """Tests para modelos"""
    
    def test_crear_usuario(self, app):
        """Verifica que se puede crear un usuario"""
        # Importamos el modelo Usuario
        from app.models.usuario import Usuario
        
        # app.app_context() es necesario para Flask
        with app.app_context():
            # Creamos usuario de prueba
            user = Usuario(
                email="test@example.com",
                password="password123",
                role="user"
            )
            # Verificamos que el objeto se crea bien
            assert user.email == "test@example.com"
            assert user.role == "user"
    
    def test_crear_concurso(self, app):
        """Verifica que se puede crear un concurso"""
        from app.models.concurso import Concurso
        from datetime import datetime, timedelta
        
        with app.app_context():
            # datetime.utcnow() es la fecha actual
            # timedelta(days=30) suma 30 días
            concurso = Concurso(
                titulo="Concurso Test",
                descripcion="Descripción test",
                fecha_inicio=datetime.utcnow(),
                fecha_fin=datetime.utcnow() + timedelta(days=30)
            )
            assert concurso.titulo == "Concurso Test"
            assert concurso.estado == "activo"  # valor por defecto
    
    def test_crear_envio(self, app):
        """Verifica que se puede crear un envío"""
        from app.models.envio import Envio
        
        with app.app_context():
            envio = Envio(
                titulo="Mi Obra",
                imagen_url="uploads/test.jpg",
                votos=0
            )
            assert envio.titulo == "Mi Obra"
            assert envio.votos == 0


# =============================================================================
# EJECUCIÓN DIRECTA
# =============================================================================
# Permite ejecutar el archivo con: python tests/test_simple.py
# En lugar de usar pytest desde la terminal

if __name__ == "__main__":
    print("="*60)
    print("TESTS SIMPLES - ARTRANKING")
    print("="*60)
    print("\nEjecutando tests...\n")
    import subprocess
    # subprocess.run ejecuta un comando
    # ['pytest', __file__, '-v'] ejecuta pytest en este archivo
    result = subprocess.run(['pytest', __file__, '-v'])
    # sys.exit(result.returncode) sale con el resultado (0 si OK)
    sys.exit(result.returncode)
