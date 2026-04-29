# Presentación: Arquitectura de la API ArtRanking

## Introducción

La API ArtRanking es una aplicación web desarrollada con Flask y MongoDB que permite gestionar concursos artísticos, envíos de obras, votaciones y perfiles de usuarios. Esta presentación se centra en la arquitectura backend, específicamente en los componentes clave: **Modelos**, **Servicios** y **Rutas**.

La arquitectura sigue un patrón de diseño MVC (Model-View-Controller) adaptado, donde:
- **Modelos**: Representan las entidades de datos y su persistencia en MongoDB.
- **Servicios**: Contienen la lógica de negocio y operaciones CRUD.
- **Rutas**: Definen los endpoints REST y manejan las solicitudes HTTP.

## Modelos

Los modelos definen la estructura de los datos almacenados en MongoDB utilizando MongoEngine. Cada modelo hereda de `Document` y define campos con validaciones.

### Usuario
- **Propósito**: Representa a los usuarios del sistema (artistas, votantes, administradores).
- **Campos principales**:
  - `email`: Campo único y requerido para autenticación.
  - `password`: Hash de la contraseña.
  - `role`: Rol del usuario (por defecto "user", puede ser "admin").

### Categoría
- **Propósito**: Clasifica las obras artísticas (pintura, escultura, digital, etc.).
- **Campos principales**:
  - `nombre`: Identificador único de la categoría.
  - `descripcion`: Detalles opcionales sobre la categoría.

### Otros Modelos
- **Concurso**: Gestiona los concursos artísticos con fechas, categorías y estados.
- **Envío**: Representa las obras enviadas por usuarios a concursos.
- **Voto**: Registra los votos de usuarios en envíos.
- **Comentario**: Comentarios en envíos.
- **Notificación**: Mensajes del sistema a usuarios.
- **Perfil**: Información adicional de usuarios.
- **Etiqueta**: Etiquetas para clasificar envíos.

## Servicios

Los servicios encapsulan la lógica de negocio, separando las operaciones de datos de las rutas. Utilizan los modelos para interactuar con la base de datos.

### Servicio de Autenticación (auth_servicio.py)
- **Funciones principales**:
  - `registrar_usuario(data)`: Crea un nuevo usuario con validación de email único y hash de contraseña.
  - `login_usuario(data)`: Verifica credenciales y retorna el usuario si son válidas.
- **Propósito**: Manejar registro y login de usuarios, incluyendo generación de tokens JWT.

### Servicio de Categorías (categoria_servicio.py)
- **Funciones principales**:
  - `crear_categoria(data)`: Crea una nueva categoría.
  - `obtener_categorias()`: Lista todas las categorías.
  - `obtener_categoria(id)`: Busca una categoría por ID.
  - `actualizar_categoria(id, data)`: Actualiza una categoría.
  - `eliminar_categoria(id)`: Elimina una categoría.
- **Propósito**: Gestionar el catálogo maestro de categorías artísticas.

### Otros Servicios
- **Servicio de Concursos**: Maneja creación, listado y gestión de concursos.
- **Servicio de Envíos**: Gestiona subida y validación de obras artísticas.
- **Servicio de Votos**: Controla el sistema de votación con validaciones.

## Rutas

Las rutas definen los endpoints REST utilizando Blueprints de Flask. Incluyen autenticación JWT donde es necesario y validación de datos con Marshmallow.

### Rutas de Autenticación (auth_rutas.py)
- **Endpoints**:
  - `GET /registro`: Renderiza página de registro.
  - `POST /register`: Registra un nuevo usuario y genera token JWT.
  - `GET /login`: Renderiza página de login.
  - `POST /login`: Autentica usuario y redirige según rol.
- **Características**: Maneja tanto API REST como renderizado de templates HTML.

### Rutas de Categorías (categoria_rutas.py)
- **Endpoints**:
  - `POST /categorias`: Crea una nueva categoría (requiere JWT).
  - `GET /categorias`: Lista todas las categorías.
  - `GET /categorias/<id>`: Detalle de una categoría.
  - `PUT /categorias/<id>`: Actualiza una categoría (requiere JWT).
  - `DELETE /categorias/<id>`: Elimina una categoría (requiere JWT).
- **Características**: Endpoints REST puros con autenticación.

### Otras Rutas
- **Rutas de Concursos**: Gestión completa de concursos (crear, listar, detalles).
- **Rutas de Envíos**: Subida de obras, galería, validaciones.
- **Rutas de Votos**: Sistema de votación con restricciones.
- **Rutas de Admin**: Panel administrativo para gestión del sistema.

## Arquitectura General

```
Cliente (Browser/Postman) 
    ↓ HTTP Requests
Rutas (Blueprints)
    ↓ Llamadas a Servicios
Servicios (Lógica de Negocio)
    ↓ Operaciones en Modelos
Modelos (MongoDB Documents)
    ↓ Persistencia
MongoDB
```

### Tecnologías Utilizadas
- **Flask**: Framework web para Python.
- **MongoEngine**: ODM para MongoDB.
- **JWT**: Autenticación basada en tokens.
- **Marshmallow**: Validación y serialización de datos.
- **Werkzeug**: Utilidades de seguridad (hash de contraseñas).

### Seguridad
- Autenticación JWT en endpoints sensibles.
- Hash de contraseñas con Werkzeug.
- Validación de datos con esquemas Marshmallow.
- Decoradores personalizados para control de acceso.

## Conclusión

Esta arquitectura proporciona una separación clara de responsabilidades, facilitando el mantenimiento y escalabilidad. Los modelos definen la estructura de datos, los servicios manejan la lógica de negocio, y las rutas exponen la funcionalidad a través de una API REST. Esta estructura permite una fácil expansión del sistema y una clara división de tareas en el desarrollo backend.</content>
<parameter name="filePath">/home/penascalf5/Documentos/Visual Studio Code/17-BBDDconBackend/ArtRanking-API/@doc/presentacion.md