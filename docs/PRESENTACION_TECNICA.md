
# Guía de Presentación: Arquitectura ArtRanking-API

Este documento sirve como apoyo para la presentación técnica del sistema, detallando la interacción entre los modelos, servicios y rutas bajo una arquitectura modular y escalable.

---

## 1. Visión General de la Arquitectura
El proyecto sigue un patrón de **arquitectura por capas** para separar responsabilidades y facilitar el mantenimiento:

- **Modelos (Models):** Definición de la estructura de datos en MongoDB usando MongoEngine.
- **Servicios (Services):** Contienen la lógica de negocio pura (validaciones, cálculos, actualizaciones complejas).
- **Rutas (Routes/Blueprints):** Gestionan los endpoints HTTP, reciben peticiones y delegan el trabajo a los servicios.

---

## 2. Capa de Modelos (Entidades)
Utilizamos **MongoEngine** (ODM) para mapear objetos Python a documentos de MongoDB. Los modelos principales son:

- **Usuario:** Gestión de identidad y roles (`admin`, `user`).
- **Concurso:** Define eventos con fechas, estados y categorías.
- **Envío (Envio):** Representa las obras participantes. Incluye referencias al autor, al concurso y mantiene un contador de votos y una lista de votantes para optimizar lecturas.
- **Voto:** Registro individual de cada voto para asegurar integridad y evitar duplicados.
- **Categoría/Etiqueta:** Metadatos para clasificar y filtrar contenido.

> **Punto clave:** Usamos `ReferenceField` para mantener relaciones de integridad entre documentos.

---

## 3. Capa de Servicios (Lógica de Negocio)
Los servicios actúan como un puente. En lugar de escribir lógica en las rutas, creamos funciones reutilizables.

**Ejemplo: El Servicio de Votación (`votar`)**
1. Valida la existencia de la obra.
2. Verifica que el usuario no vote por su propia obra.
3. Comprueba si el usuario ya ha votado (integridad).
4. Realiza una **actualización sincronizada**:
   - Crea el documento `Voto`.
   - Actualiza el `Envio` (incrementa `votos` y añade al usuario a `votantes`).
   - Genera una `Notificacion` para el autor.

---

## 4. Capa de Rutas (Endpoints)
Organizadas mediante **Blueprints** de Flask para mantener el código modular.

- **Modularidad:** Cada recurso tiene su propio archivo (ej: `voto_rutas.py`, `concurso_rutas.py`).
- **Seguridad:** Uso de decoradores personalizados como `@jwt_requerido` para proteger endpoints sensibles.
- **Esquemas (Schemas):** Integración con `Marshmallow` para validar que los datos recibidos (JSON) cumplen con el formato esperado antes de procesarlos.

---

## 5. Caso de Éxito: El Sistema de Votaciones
Para tu presentación, puedes destacar cómo se conectan las tres capas:

1. **Ruta (`POST /votos/`):** Recibe el ID de la obra y el token del usuario. Valida el JSON con un Esquema.
2. **Servicio (`votar`):** Ejecuta las reglas de negocio (no autovotarse, no duplicar votos).
3. **Modelo (`Envio/Voto`):** Persiste los datos en MongoDB.
4. **Frontend:** Recibe la respuesta y actualiza la UI dinámicamente mediante `voting.js` y el sistema modular de alertas (`showAlert`).

---

## 6. Conclusión Técnica
Esta estructura permite que el sistema sea:
- **Testeable:** Los servicios se pueden probar independientemente de la web.
- **Seguro:** Centralizamos la validación y autenticación.
- **Mantenible:** Cambiar la lógica de negocio no afecta a las rutas y viceversa.
