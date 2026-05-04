# ArtRanking API 🎨🏆

ArtRanking es una plataforma web robusta diseñada para la gestión y participación en concursos de arte. Permite a los usuarios subir sus obras, participar en diversos concursos categorizados y recibir feedback de la comunidad a través de votos y comentarios. La aplicación cuenta con un sistema completo de administración y una arquitectura moderna basada en Flask y MongoDB.

## 🚀 Características Principales

- **Gestión de Usuarios y Perfiles**: Sistema de registro y login con perfiles personalizables (avatar, biografía).
- **Concursos Dinámicos**: Creación y gestión de concursos con estados (borrador, activo, cerrado).
- **Participación Artística**: Subida de obras asociadas a concursos y categorías específicas.
- **Interacción Social**: Sistema de votación y comentarios en las obras enviadas.
- **Panel de Administración**: Control total sobre usuarios, concursos, categorías y obras.
- **Sistema de Notificaciones**: Alertas automáticas para votos, comentarios y eventos de concursos.
- **Seguridad**: Autenticación basada en JWT (JSON Web Tokens) con almacenamiento seguro en cookies HttpOnly.

## 🛠️ Stack Tecnológico

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)
- **Base de Datos**: [MongoDB](https://www.mongodb.com/) con [MongoEngine](http://mongoengine.org/) (ODM)
- **Seguridad**: JWT (PyJWT) y Hash de contraseñas.
- **Frontend**: Jinja2 Templates, Vanilla CSS y JavaScript.
- **Validación**: Marshmallow.
- **Contenedores**: Docker (para la base de datos).

## 📋 Requisitos Previos

- Python 3.8+
- Docker y Docker Compose (opcional, para MongoDB)
- MongoDB (si no se usa Docker)

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd ArtRanking-API
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv myEnv
   source myEnv/bin/activate  # En Windows: myEnv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crea un archivo `.env` en la raíz con el siguiente contenido:
   ```env
   SECRET_KEY=tu_llave_secreta_super_segura
   MONGO_URI=mongodb://localhost:27017/artranking
   MONGO_DB=artranking
   ```

5. **Levantar la base de datos (Docker):**
   ```bash
   docker-compose up -d
   ```

## 🏃 Ejecución

Para iniciar el servidor de desarrollo:

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`.

## 📂 Estructura del Proyecto

```text
ArtRanking-API/
├── app/                  # Núcleo de la aplicación
│   ├── models/           # Modelos de MongoEngine
│   ├── routes/           # Blueprints y rutas
│   ├── services/         # Lógica de negocio
│   ├── schemas/          # Esquemas de validación (Marshmallow)
│   ├── templates/        # Vistas Jinja2
│   └── static/           # Archivos estáticos (CSS, JS, Imágenes)
├── tests/                # Pruebas unitarias e integración
├── seeds/                # Datos iniciales para la base de datos
├── config.py             # Configuraciones de Flask
├── run.py                # Punto de entrada de la aplicación
└── docker-compose.yml    # Orquestación de MongoDB
```

## 🧪 Pruebas

Para ejecutar la suite de pruebas:

```bash
pytest
```

## 📄 Documentación Adicional

- [Guía de Diseño](DESIGN.md): Detalles sobre la estética y componentes UI.
- [Estructura de Carpetas](estructura_carpetas.md): Explicación detallada del árbol de directorios.
- [Entidades de Base de Datos](tablas-entidades.md): Descripción de los modelos y relaciones.
- [Manual de Seeds](seeds/MANUAL_SEEDS.md): Cómo poblar la base de datos con datos de prueba.

---
Desarrollado como parte del Curso Fullstack Python.

## 👥 Colaboradores

- [Marlen Álvarez](https://github.com/alvarezmarlen)
- [fediralydev](https://www.linkedin.com/in/achrafrzz/)
- [Juan Carlos](https://github.com/JuanCarlos0977)
- [Kevin Ruiz](https://github.com/Kevingedev)
