# Justificación: Por qué usar MongoDB en ArtRanking-API

El proyecto **ArtRanking-API** utiliza MongoDB como su base de datos principal, interactuando con ella a través de `mongoengine` en Python. A continuación se explica por qué MongoDB es una excelente elección para este proyecto, junto con sus principales ventajas y desventajas.

## ¿Por qué MongoDB es una buena opción para ArtRanking?

1. **Flexibilidad en el Modelado de Datos:** En una plataforma de arte, los metadatos de las obras (envíos), los perfiles de usuario y las reglas de los concursos pueden evolucionar rápidamente. MongoDB, al ser una base de datos NoSQL orientada a documentos, permite esquemas dinámicos. Esto significa que podemos añadir nuevos campos a un documento sin afectar a los demás ni requerir complejas migraciones de base de datos.
2. **Sinergia con el Formato JSON:** Las APIs modernas (y los frameworks frontend) se comunican mediante JSON. MongoDB almacena los datos en formato BSON (una representación binaria de JSON). Esta naturalidad elimina la "fricción" de traducir tablas relacionales a objetos JSON, facilitando enormemente el flujo de datos desde la base de datos hasta el cliente.
3. **Listas y Documentos Embebidos:** El proyecto hace uso de las capacidades de MongoDB para almacenar arrays dentro del propio documento. Por ejemplo, en los envíos (`Envio`), se puede guardar una lista de los usuarios que han votado (`votantes`), así como el contador de votos, dentro del mismo documento. En una base de datos SQL, esto requeriría consultar múltiples tablas mediante `JOIN`s pesados. En MongoDB, recuperar un envío con todas sus interacciones principales toma una sola consulta rápida.
4. **Iteración Rápida (Ideal para el Desarrollo Rápido):** Al no requerir un esquema estricto ni herramientas pesadas de migración (como Alembic en el mundo SQL), MongoDB permite a los desarrolladores prototipar y añadir nuevas funcionalidades (como el sistema de Notificaciones o Etiquetas) con gran velocidad.
5. **Escalabilidad Horizontal:** Si la plataforma ArtRanking se populariza y crece el volumen de imágenes (metadatos), usuarios y sobre todo votos y comentarios concurrentes, MongoDB está diseñado para escalar horizontalmente de manera nativa mediante *Sharding*, repartiendo la carga entre múltiples servidores.

---

## Ventajas de usar MongoDB

- **Desarrollo Ágil:** Ausencia de esquemas rígidos (Schema-less), lo que evita migraciones constantes al añadir nuevas características.
- **Rendimiento de Lectura:** Al estructurar bien los documentos (ej. guardando datos relacionados juntos), la lectura de información es extremadamente rápida, ideal para una aplicación de "Ranking" donde las lecturas (ver galerías) superan ampliamente a las escrituras.
- **Integración perfecta en Python:** Herramientas como `mongoengine` (ODM) mapean las clases de Python a colecciones de MongoDB de manera intuitiva y limpia, validando los datos a nivel de aplicación.
- **Consultas Geoespaciales y Búsqueda de Texto:** Si en el futuro se quiere buscar arte por ubicación o implementar un buscador avanzado de títulos y descripciones, MongoDB tiene un soporte nativo excelente para esto.
- **Escalabilidad y Alta Disponibilidad:** Fácil configuración de réplicas (Replica Sets) para evitar caídas del sistema.

## Desventajas (y Retos) de usar MongoDB

- **Ausencia de `JOIN`s eficientes:** A diferencia de SQL, MongoDB no está optimizado para consultas relacionales complejas. Relaciones de muchos a muchos (como `EnvioEtiqueta`) o la necesidad de unir múltiples colecciones para generar un informe, pueden requerir del *Aggregation Framework* (`$lookup`), lo cual es menos intuitivo y más costoso computacionalmente que un simple `JOIN`.
- **Transacciones complejas:** Aunque las versiones modernas de MongoDB soportan transacciones ACID multi-documento, su uso penaliza el rendimiento. Las bases de datos relacionales siguen siendo superiores si la aplicación depende de operaciones transaccionales extremadamente estrictas.
- **Tamaño de almacenamiento:** MongoDB tiende a ocupar más espacio en disco y memoria RAM que las bases de datos relacionales tradicionales debido al almacenamiento repetido de los nombres de los campos en cada documento BSON y la naturaleza de la desnormalización.
- **Integridad de los datos delegada a la aplicación:** Mientras que en SQL la base de datos asegura rígidamente las llaves foráneas e integridad referencial, en MongoDB esta responsabilidad recae principalmente en el código (en este caso, en `mongoengine`). Si hay un fallo en la lógica de la app, es más fácil introducir datos inconsistentes o "huérfanos".
