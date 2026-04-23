# Guía de Testing con Postman - ArtRanking API

Guía paso a paso para probar la API de ArtRanking usando Postman.

---

## Requisitos Previos

- Postman instalado
- Servidor Flask corriendo (`python run.py`)
- MongoDB corriendo (`docker compose up -d`)
- Virtualenv activado (`source myEnv/bin/activate`)

---

## 1. Crear Colección en Postman

1. Abrir Postman
2. Click en **New** (arriba izquierda) → **Collection**
3. Nombre: `ArtRanking Test`
4. Click **Create**

---

## 2. Crear Carpeta "Auth"

Click derecho en la colección → **Add Folder** → Nombre: `Auth`

### Request 1: Register

- Click derecho en `Auth` → **Add Request**
- Nombre: `Register`
- Method: `POST`
- URL: `http://localhost:5000/auth/register`
- Tab **Body** → selecciona `raw` → formato `JSON`
- Body:
```json
{
  "email": "test@example.com",
  "password": "123456"
}
```
- Click **Send**
- ✅ Respuesta esperada: `{"id": "..."}`

### Request 2: Login

- Click derecho en `Auth` → **Add Request**
- Nombre: `Login`
- Method: `POST`
- URL: `http://localhost:5000/auth/login`
- Tab **Body** → `raw` → `JSON`
- Body:
```json
{
  "email": "test@example.com",
  "password": "123456"
}
```
- Click **Send**
- ✅ Copiar el token de la respuesta (ej: `{"token": "eyJ0eXAi..."}`)
- Guardar el token para usarlo en los siguientes requests

---

## 3. Crear Carpeta "Categorías" (Catálogo Maestro)

### Request 1: Crear Categoría
- Nombre: `Crear Categoría`
- Method: `POST`
- URL: `http://localhost:5000/categorias`
- Headers: 
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {token}`
- Body:
```json
{
  "nombre": "Pintura al Óleo",
  "descripcion": "Obras realizadas con técnica de óleo"
}
```
- ✅ Copiar el `id` de la categoría.

### Request 2: Listar Categorías
- Nombre: `Listar Categorías`
- Method: `GET`
- URL: `http://localhost:5000/categorias`

---

## 4. Crear Carpeta "Concursos"

### Request 1: Crear Concurso
- Nombre: `Crear Concurso`
- Method: `POST`
- URL: `http://localhost:5000/concursos`
- Tab **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {token}`
- Tab **Body** → `raw` → `JSON`:
```json
{
  "titulo": "Concurso de Bellas Artes",
  "descripcion": "Exhibición anual",
  "fecha_inicio": "2025-01-01T00:00:00",
  "fecha_fin": "2025-12-31T23:59:59",
  "categorias": ["{categoria_id_1}", "{categoria_id_2}"]
}
```
- Click **Send**
- ✅ Copiar el `id` del concurso de la respuesta

### Request 2: Listar Concursos
- Nombre: `Listar Concursos`
- Method: `GET`
- URL: `http://localhost:5000/concursos?activos=true`
- Headers: `Authorization: Bearer {token}`

### Request 3: Ver Detalle
- Nombre: `Detalle Concurso`
- Method: `GET`
- URL: `http://localhost:5000/concursos/{concurso_id}`
- Reemplazar `{concurso_id}` con el ID copiado

---

## 5. Gestión Avanzada de Concursos

### Request 4: Actualizar Concurso
- Nombre: `Actualizar Concurso`
- Method: `PUT`
- URL: `http://localhost:5000/concursos/{concurso_id}`
- Headers: `Authorization: Bearer {token}`
- Body → `raw` → `JSON`:
```json
{
  "titulo": "Concurso Actualizado",
  "descripcion": "Nueva descripción"
}
```

### Request 5: Cambiar Estado
- Nombre: `Cambiar Estado`
- Method: `PATCH`
- URL: `http://localhost:5000/concursos/{concurso_id}/estado`
- Headers: `Authorization: Bearer {token}`
- Body → `raw` → `JSON`:
```json
{
  "estado": "cerrado"
}
```
- ✅ Estados válidos: `activo`, `cerrado`, `cancelado`

### Request 6: Vincular Categoría
- Nombre: `Vincular Categoría`
- Method: `POST`
- URL: `http://localhost:5000/concursos/{concurso_id}/categorias`
- Headers: `Authorization: Bearer {token}`
- Body → `raw` → `JSON`:
```json
{
  "categoria_id": "{categoria_id}"
}
```

---

## 6. Crear Carpeta "Envíos"

### Request 1: Crear Envío
- Nombre: `Crear Envío`
- Method: `POST`
- URL: `http://localhost:5000/envios`
- Headers:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {token}`
- Body → `raw` → `JSON`:
```json
{
  "titulo": "Mi Obra Maestra",
  "descripcion": "Óleo sobre lienzo",
  "imagen_url": "https://example.com/obra.jpg",
  "concurso_id": "{concurso_id}",
  "categoria_id": "{categoria_id}",
  "etiquetas": ["arte", "oleo"]
}
```

### Request 2: Listar Envíos
- Nombre: `Listar Envíos`
- Method: `GET`
- URL: `http://localhost:5000/envios?concurso={concurso_id}`

### Request 3: Votar
- Nombre: `Votar Envío`
- Method: `POST`
- URL: `http://localhost:5000/envios/{envio_id}/votar`
- Headers: `Authorization: Bearer {token}`

### Request 4: Ver Ranking
- Nombre: `Ver Ranking`
- Method: `GET`
- URL: `http://localhost:5000/envios/concurso/{concurso_id}/ranking?limite=10`

---

## 7. Comentarios y Notificaciones

### Request 1: Añadir Comentario
- Nombre: `Añadir Comentario`
- Method: `POST`
- URL: `http://localhost:5000/votos/comentarios`
- Body → `raw` → `JSON`:
```json
{
  "user_id": "{tu_user_id}",
  "submission_id": "{envio_id}",
  "texto": "¡Increíble trabajo!"
}
```

### Request 2: Ver Notificaciones
- Nombre: `Ver Notificaciones`
- Method: `GET`
- URL: `http://localhost:5000/votos/notificaciones/{user_id}`

---

## 8. Perfil de Usuario

### Request 1: Ver Mi Perfil
- Nombre: `Mi Perfil`
- Method: `GET`
- URL: `http://localhost:5000/users/me`
- Headers: `Authorization: Bearer {token}`

### Request 2: Actualizar Mi Perfil
- Nombre: `Actualizar Perfil`
- Method: `PUT`
- URL: `http://localhost:5000/users/me`
- Headers: `Authorization: Bearer {token}`
- Body → `raw` → `JSON`:
```json
{
  "email": "nuevo_email@example.com"
}
```

---

## Resumen de Endpoints (Actualizado)

| Paso | Method | URL | Auth |
|------|--------|-----|------|
| Register | POST | `/auth/register` | No |
| Login | POST | `/auth/login` | No |
| **Crear Categoría** | **POST** | `/categorias` | **Sí** |
| **Listar Categorías** | **GET** | `/categorias` | **No** |
| Crear Concurso | POST | `/concursos` | Sí |
| Listar Concursos | GET | `/concursos` | Sí |
| Cambiar Estado | PATCH | `/concursos/{id}/estado` | Sí |
| **Vincular Categoría** | **POST** | `/concursos/{id}/categorias` | **Sí** |
| Crear Envío | POST | `/envios` | Sí |
| Actualizar Envío | PUT | `/envios/{id}` | Sí |
| Eliminar Envío | DELETE | `/envios/{id}` | Sí |
| Votar | POST | `/envios/{id}/votar` | Sí |
| Ranking | GET | `/envios/concurso/{id}/ranking` | No |
| Comentar | POST | `/votos/comentarios` | No |
| Notificaciones | GET | `/votos/notificaciones/{user_id}` | No |
| Mi Perfil | GET | `/users/me` | Sí |

---

## Flujo Completo de Testing

```
1. Registro/Login 
   → 2. Gestionar Perfil 
   → 3. Crear Categorías (Catálogo)
   → 4. Crear Concurso (Referenciando Categorías)
   → 5. Crear Envío 
   → 6. Votar y Comentar 
   → 7. Revisar Notificaciones 
   → 8. Ver Ranking
```

---

## Troubleshooting

### Error 403 Forbidden
- Token expirado o ausente. Haz Login de nuevo.
- Verificar que el servidor Flask esté corriendo: `python run.py`

### Error 400 Bad Request
- Revisa el formato JSON y campos requeridos según los esquemas en `app/schemas/`.

---

## Variables a Guardar

Durante el testing, guarda estos valores para reutilizar:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `token` | JWT para autenticación | `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` |
| `concurso_id` | ID del concurso creado | `507f1f77bcf86cd799439011` |
| `envio_id` | ID del envío creado | `507f1f77bcf86cd799439013` |
| `user_id` | Tu ID de usuario | `507f1f77bcf86cd799439014` |
| `categoria_id` | ID de la categoría creada | `507f1f77bcf86cd799439015` |

---

## Colección JSON para Importar

También puedes importar el archivo `ArtRanking.postman_collection.json` incluido en el proyecto:

1. Postman → **File** → **Import**
2. Seleccionar `ArtRanking.postman_collection.json`
3. Click **Import**
4. Configurar las variables en la colección importada
