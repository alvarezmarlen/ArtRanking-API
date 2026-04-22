```text
Usuarios
 Base del sistema
 nombre
 correo electrónico
 contraseña (hash)
 rol (admin/usuario)

Perfiles
 Extensión del usuario (1:1)
 user_id
 avatar
 bio

Concursos
 Evento principal
 título
 descripción
 fecha_inicio
 fecha_fin
 estado (borrador, activo, cerrado)


Categorías
 Relación: 1 Concurso → N Categorías
 nombre
 contest_id

Envíos
 Relación: Usuario + Concurso + Categoría
 título
 descripción
 file_url
 user_id
 contest_id
 category_id

Votos
 Relación: Usuario → Envío
 user_id
 submission_id
 valor (1–5 o me gusta)

Comentarios
 Relación: Usuario → Envío
 user_id
 submission_id
 texto
Etiquetas
 Clasificación flexible
 nombre

SubmissionTags
 Relación N:N
 submission_id
 tag_id

Notificaciones
 Eventos del sistema
 user_id
 tipo (voto, comentario, concurso)
 mensaje
 leído (true/false)
```