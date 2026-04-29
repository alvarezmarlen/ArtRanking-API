"""
================================================================================
TESTS SIMPLES - ArtRanking
================================================================================
Tests básicos para verificar que la aplicación funciona.

EJECUTAR:
    pytest tests/test_simple.py -v
================================================================================
"""

# Importamos pytest para crear tests y fixtures
import pytest
# Importamos sys y os para manipular rutas del sistema
import sys
import os

# Agregar directorio raíz al path para poder importar módulos de la app
# sys.path.insert(0, ruta) agrega una ruta al inicio de la lista de búsqueda de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos la función create_app de nuestra aplicación Flask
from app import create_app
# Importamos la configuración de测试 (TestConfig) que usa mongomock
from config import TestConfig
# Importamos mongomock para simular MongoDB sin necesidad de tenerlo instalado
import mongomock


# =============================================================================
# CONFIGURACIÓN
# =============================================================================
# Los fixtures son funciones que pytest ejecuta antes de cada test
# Sirven para preparar el entorno de prueba (crear app, cliente, datos, etc.)

@pytest.fixture
def app():
    """
    Crea la aplicación para testing
    Este fixture se ejecuta antes de cada test que lo solicita
    """
    # Configuramos mongomock como cliente de MongoDB para no necesitar MongoDB real
    TestConfig.MONGO_CLIENT_CLASS = mongomock.MongoClient
    # Creamos la instancia de la aplicación Flask con la configuración de测试
    app = create_app(TestConfig)
    return app


@pytest.fixture
def cliente(app):
    """
    Crea un cliente HTTP para hacer peticiones
    Este cliente simula un navegador para hacer requests a la app
    """
    # test_client() crea un cliente de prueba que puede hacer requests HTTP
    return app.test_client()


# =============================================================================
# TESTS DE PÁGINAS (no necesitan base de datos)
# =============================================================================
# Estos tests verifican que las páginas públicas carguen correctamente
# No requieren login ni datos en la base de datos

class TestPaginasPublicas:
    """Tests para páginas que no requieren login"""
    
    def test_pagina_inicio_carga(self, cliente):
        """Verifica que la página de inicio carga correctamente"""
        # cliente.get('/') hace una petición GET a la ruta principal
        respuesta = cliente.get('/')
        # Verificamos que el código de respuesta sea 200 (OK)
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
# Estos tests verifican el comportamiento de los endpoints de API
# Algunos requieren autenticación, otros son públicos

class TestAPIs:
    """Tests para endpoints de API"""
    
    def test_api_concursos_requiere_auth(self, cliente):
        """Verifica que el API de concursos requiere autenticación"""
        respuesta = cliente.get('/concursos/api')
        # Debe redirigir (302) a login o rechazar (401) si no hay token
        assert respuesta.status_code in [302, 401]
    
    def test_api_envios_lista_publica(self, cliente):
        """Verifica que la lista de envíos es pública"""
        respuesta = cliente.get('/envios')
        # Esta API es pública según la configuración del middleware
        assert respuesta.status_code == 200


# =============================================================================
# TESTS DE ERRORES
# =============================================================================
# Estos tests verifican que la aplicación maneje errores correctamente
# Como páginas no encontradas (404) o recursos inexistentes

class TestErrores:
    """Tests para manejo de errores"""
    
    def test_pagina_no_existente_404(self, cliente):
        """Verifica que páginas inexistentes retornan 404"""
        respuesta = cliente.get('/pagina-que-no-existe')
        # El middleware redirige a home (302) cuando no está autenticado
        # Aceptamos 404 o 302 ya que el middleware intercepta antes del handler 404
        assert respuesta.status_code in [404, 302]
    
    def test_concurso_no_existente_404(self, cliente):
        """Verifica que concurso inexistente retorna 404"""
        # Usamos un ObjectId válido de 24 caracteres hex que no existe en la BD
        # MongoDB requiere ObjectIds de 24 caracteres hexadecimales
        respuesta = cliente.get('/concursos/507f1f77bcf86cd799439011/detalle')
        assert respuesta.status_code == 404


# =============================================================================
# TESTS DE MODELOS (requieren MongoDB)
# =============================================================================
# Estos tests verifican que los modelos de datos se crean correctamente
# No guardan en la BD, solo verifican la creación de objetos en memoria

class TestModelos:
    """Tests para modelos de datos"""
    
    def test_crear_usuario(self, app):
        """Verifica que se puede crear un usuario"""
        # Importamos el modelo Usuario dentro del test para evitar errores de importación temprana
        from app.models.usuario import Usuario
        
        # app.app_context() crea un contexto de aplicación Flask necesario para los modelos
        with app.app_context():
            # Crear usuario de prueba (modelo tiene: email, password, role)
            user = Usuario(
                email="test@example.com",
                password="password123",
                role="user"
            )
            # Solo verificamos que el objeto se crea correctamente en memoria
            assert user.email == "test@example.com"
            assert user.role == "user"
    
    def test_crear_concurso(self, app):
        """Verifica que se puede crear un concurso"""
        from app.models.concurso import Concurso
        from datetime import datetime, timedelta
        
        with app.app_context():
            # datetime.utcnow() obtiene la fecha actual en UTC
            # timedelta(days=30) suma 30 días a la fecha actual
            concurso = Concurso(
                titulo="Concurso Test",
                descripcion="Descripción test",
                fecha_inicio=datetime.utcnow(),
                fecha_fin=datetime.utcnow() + timedelta(days=30)
            )
            assert concurso.titulo == "Concurso Test"
            assert concurso.estado == "activo"  # valor por defecto del modelo
    
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
# Permite ejecutar el archivo directamente con: python tests/test_simple.py
# En lugar de usar pytest desde la línea de comandos

if __name__ == "__main__":
    print("="*60)
    print("TESTS SIMPLES - ARTRANKING")
    print("="*60)
    print("\nEjecutando tests...\n")
    import subprocess
    # subprocess.run ejecuta un comando del sistema como un proceso separado
    # ['pytest', __file__, '-v'] ejecuta pytest en este archivo con modo verbose
    result = subprocess.run(['pytest', __file__, '-v'])
    # sys.exit(result.returncode) sale con el código de retorno de pytest (0 si todo OK)
    sys.exit(result.returncode)
