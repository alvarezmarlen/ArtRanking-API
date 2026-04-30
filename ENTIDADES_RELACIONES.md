# Entidades y Relaciones del Proyecto ArtRanking-API

Este documento recoge las entidades principales definidas en `app/models` y sus relaciones.

---

## 1. Usuario
Colección: `usuarios` (por convención de MongoEngine)

Campos principales:
- `email`: Email único.
- `password`: Contraseña.
- `role`: Rol del usuario (`user` por defecto).

Relaciones:
- 1 Usuario puede tener 1 `Perfil`.
- 1 Usuario puede crear muchos `Concurso` (`Concurso.creado_por`).
- 1 Usuario puede ser autor de muchos `Envio` (`Envio.autor`).
- 1 Usuario puede hacer muchos `Comentario` (`Comentario.usuario`).
- 1 Usuario puede hacer muchos `Voto` (`Voto.usuario`).
- 1 Usuario puede aparecer en `Envio.votantes` como lista de usuarios que ya votaron una obra.

---

## 2. Perfil
Colección: `perfil` (por convención de MongoEngine)

Campos principales:
- `usuario`: ReferenceField a `Usuario`.
- `nombre`: Nombre público.
- `avatar`: URL o identificador de imagen.
- `bio`: Biografía.

Relaciones:
- `Perfil.usuario` referencia a 1 `Usuario`.

---

## 3. Concurso
Colección: `concursos`

Campos principales:
- `titulo`: Nombre del concurso.
- `descripcion`: Descripción del concurso.
- `fecha_inicio`: Fecha de inicio.
- `fecha_fin`: Fecha de fin.
- `estado`: Estado del concurso (`activo` por defecto).
- `creado_por`: ReferenceField a `Usuario`.
- `categorias`: ListField de referencias a `Categoria`.
- `activo`: Booleano de visibilidad.
- `fecha_creacion`: Fecha de creación.

Relaciones:
- `Concurso.creado_por` referencia a 1 `Usuario`.
- `Concurso.categorias` es una lista de referencias a `Categoria`.
- 1 Concurso puede tener muchos `Envio`.

---

## 4. Categoria
Colección: `categorias`

Campos principales:
- `nombre`: Nombre de categoría.
- `descripcion`: Descripción.

Relaciones:
- `Categoria` puede aparecer en la lista `Concurso.categorias`.
- 1 `Categoria` puede vincularse a muchos `Envio` como categoría de obra.

---

## 5. Envio
Colección: `envios`

Campos principales:
- `titulo`: Nombre de la obra.
- `descripcion`: Descripción.
- `imagen_url`: URL de la imagen.
- `autor`: ReferenceField a `Usuario`.
- `concurso`: ReferenceField a `Concurso`.
- `categoria`: ReferenceField a `Categoria`.
- `votos`: Contador de votos.
- `votantes`: ListField de ReferenceField a `Usuario`.
- `fecha_envio`: Fecha de envío.

Relaciones:
- `Envio.autor` referencia a 1 `Usuario`.
- `Envio.concurso` referencia a 1 `Concurso`.
- `Envio.categoria` referencia a 1 `Categoria`.
- `Envio.votantes` almacena una lista de `Usuario` que ya votaron ese envío.
- 1 `Envio` puede tener muchos `Comentario`.
- 1 `Envio` puede tener muchos `Voto`.
- 1 `Envio` puede estar vinculado a muchas `Etiqueta` mediante `EnvioEtiqueta`.

---

## 6. Comentario
Colección: `comentario` (por convención de MongoEngine)

Campos principales:
- `usuario`: ReferenceField a `Usuario`.
- `envio`: ReferenceField a `Envio`.
- `texto`: Texto del comentario.
- `fecha`: Fecha del comentario.

Relaciones:
- `Comentario.usuario` referencia a 1 `Usuario`.
- `Comentario.envio` referencia a 1 `Envio`.

---

## 7. Voto
Colección: `voto` (por convención de MongoEngine)

Campos principales:
- `usuario`: ReferenceField a `Usuario`.
- `envio`: ReferenceField a `Envio`.
- `value`: Valor del voto (por defecto 1).

Relaciones:
- `Voto.usuario` referencia a 1 `Usuario`.
- `Voto.envio` referencia a 1 `Envio`.

---

## 8. Etiqueta
Colección: `etiquetas`

Campos principales:
- `nombre`: Nombre único de la etiqueta.

Relaciones:
- `Etiqueta` se conecta con `Envio` mediante la entidad de unión `EnvioEtiqueta`.

---

## 9. EnvioEtiqueta
Colección: `envio_etiquetas`

Campos principales:
- `envio`: ReferenceField a `Envio`.
- `etiqueta`: ReferenceField a `Etiqueta`.

Relaciones:
- `EnvioEtiqueta.envio` referencia a 1 `Envio`.
- `EnvioEtiqueta.etiqueta` referencia a 1 `Etiqueta`.
- Representa la relación many-to-many entre `Envio` y `Etiqueta`.

---

## 10. Notificacion
Colección: `notificacion` (por convención de MongoEngine)

Campos principales:
- `user_id`: Identificador del usuario como cadena.
- `tipo`: Tipo de notificación (`voto`, `comentario`, etc.).
- `mensaje`: Mensaje descriptivo.
- `leido`: Booleano de leído.
- `fecha`: Fecha de la notificación.

Relaciones:
- `Notificacion.user_id` no es una referencia MongoEngine explícita, sino un identificador de usuario en texto.

---

## Mapa de relaciones resumido

- `Usuario` 1:N `Concurso`
- `Usuario` 1:N `Envio`
- `Usuario` 1:N `Comentario`
- `Usuario` 1:N `Voto`
- `Usuario` 1:1 `Perfil`
- `Concurso` 1:N `Envio`
- `Concurso` N:M `Categoria` (lista de categorías)
- `Categoria` 1:N `Envio`
- `Envio` 1:N `Comentario`
- `Envio` 1:N `Voto`
- `Envio` N:M `Etiqueta` a través de `EnvioEtiqueta`
- `Envio` 1:N `Usuario` en `votantes` (lista denormalizada)

---

## Entidades por orden de importancia

1. `Usuario` (1:1 Perfil, 1:N Concurso, 1:N Envio, 1:N Comentario, 1:N Voto, N:M Envio como votante)
2. `Envio` (1:N Comentario, 1:N Voto, N:M Etiqueta, 1:1 Usuario autor, 1:1 Concurso, 1:1 Categoria, N:M Usuario en votantes)
3. `Concurso` (1:N Envio, N:M Categoria, 1:1 Usuario creador)
4. `Categoria` (1:N Envio, N:M Concurso)
5. `Voto` (1:1 Usuario, 1:1 Envio)
6. `Comentario` (1:1 Usuario, 1:1 Envio)
7. `Etiqueta` (N:M Envio a través de EnvioEtiqueta)
8. `EnvioEtiqueta` (1:1 Envio, 1:1 Etiqueta)
9. `Perfil` (1:1 Usuario)
10. `Notificacion` (relación implícita con Usuario vía `user_id` en texto)

---

## Observaciones

- `EnvioEtiqueta` funciona como tabla intermedia para etiquetas.
- `Notificacion` usa `user_id` como texto en lugar de `ReferenceField`, por lo que la relación no está forzada en MongoEngine.
- `Categoria` es reutilizable entre concursos y envíos.
- `Envio.votantes` es una forma de evitar doble voto con una lista de referencias a `Usuario`.
