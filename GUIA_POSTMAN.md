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

## 3. Crear Carpeta "Concursos"

### Request 1: Crear Concurso

- Nombre: `Crear Concurso`
- Method: `POST`
- URL: `http://localhost:5000/concursos`
- Tab **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {token}` (pegar tu token aquí)
- Tab **Body** → `raw` → `JSON`:
```json
{
  "titulo": "Concurso de Fotografía",
  "descripcion": "Mejor foto de naturaleza",
  "fecha_inicio": "2025-01-01T00:00:00",
  "fecha_fin": "2025-12-31T23:59:59",
  "categorias": [
    {"nombre": "Paisajes", "descripcion": "Fotos de paisajes"},
    {"nombre": "Retratos", "descripcion": "Fotos de personas"}
  ]
}
```
- Click **Send**
- ✅ Copiar el `id` del concurso de la respuesta

### Request 2: Listar Concursos

- Nombre: `Listar Concursos`
- Method: `GET`
- URL: `http://localhost:5000/concursos?activos=true`
- Headers: `Authorization: Bearer {token}`
- Click **Send**

### Request 3: Ver Detalle

- Nombre: `Detalle Concurso`
- Method: `GET`
- URL: `http://localhost:5000/concursos/{concurso_id}`
- Reemplazar `{concurso_id}` con el ID copiado
- Click **Send**
- ✅ Buscar en la respuesta el `id` de una categoría:
  ```json
  "categorias": [{"id": "...", "nombre": "Paisajes"}]
  ```

---

## 4. Crear Carpeta "Envíos"

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
  "titulo": "Atardecer en la playa",
  "descripcion": "Foto tomada en Cancún",
  "imagen_url": "https://example.com/playa.jpg",
  "concurso_id": "{concurso_id}",
  "categoria_id": "{categoria_id}",
  "etiquetas": ["playa", "atardecer", "mar"]
}
```
- Reemplazar IDs con los valores copiados
- Click **Send**
- ✅ Copiar el `id` del envío de la respuesta

### Request 2: Listar Envíos por Concurso

- Nombre: `Listar Envíos`
- Method: `GET`
- URL: `http://localhost:5000/envios?concurso={concurso_id}`
- Click **Send**

### Request 3: Votar

- Nombre: `Votar Envío`
- Method: `POST`
- URL: `http://localhost:5000/envios/{envio_id}/votar`
- Headers: `Authorization: Bearer {token}`
- Click **Send**
- ✅ Respuesta esperada: `{"votos": 1, "mensaje": "Voto registrado"}`

### Request 4: Ver Ranking

- Nombre: `Ver Ranking`
- Method: `GET`
- URL: `http://localhost:5000/envios/concurso/{concurso_id}/ranking?limite=10`
- Click **Send**
- ✅ Ver ranking ordenado por votos

---

## Resumen de Endpoints

| Paso | Method | URL | Headers | Body |
|------|--------|-----|---------|------|
| Register | POST | `/auth/register` | Content-Type: json | email, password |
| Login | POST | `/auth/login` | Content-Type: json | email, password |
| Crear Concurso | POST | `/concursos` | Authorization + Content-Type | titulo, fechas, categorias |
| Listar Concursos | GET | `/concursos?activos=true` | Authorization | - |
| Detalle Concurso | GET | `/concursos/{id}` | - | - |
| Crear Envío | POST | `/envios` | Authorization + Content-Type | titulo, imagen_url, ids |
| Listar Envíos | GET | `/envios?concurso={id}` | - | - |
| Votar | POST | `/envios/{id}/votar` | Authorization | - |
| Ranking | GET | `/envios/concurso/{id}/ranking` | - | - |

---

## Flujo Completo de Testing

```
1. Register 
   → 2. Login (guardar token) 
   → 3. Crear Concurso (guardar concurso_id) 
   → 4. Crear Envío (usar concurso_id + categoria_id, guardar envio_id) 
   → 5. Votar (usar envio_id) 
   → 6. Ver Ranking
```

---

## Troubleshooting

### Error 403 Forbidden
- Verificar que el servidor Flask esté corriendo: `python run.py`
- Verificar que el token no haya expirado (duración: 1 hora)
- Obtener nuevo token haciendo Login de nuevo

### Error 404 Not Found
- Verificar que MongoDB esté corriendo: `docker compose ps`
- Verificar que los IDs usados existan en la base de datos

### Error 400 Bad Request
- Verificar que el JSON en el Body sea válido
- Verificar que todos los campos requeridos estén presentes

---

## Variables a Guardar

Durante el testing, guarda estos valores para reutilizar:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `token` | JWT para autenticación | `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` |
| `concurso_id` | ID del concurso creado | `507f1f77bcf86cd799439011` |
| `categoria_id` | ID de categoría del concurso | `507f1f77bcf86cd799439012` |
| `envio_id` | ID del envío creado | `507f1f77bcf86cd799439013` |

---

## Colección JSON para Importar

También puedes importar el archivo `ArtRanking.postman_collection.json` incluido en el proyecto:

1. Postman → **File** → **Import**
2. Seleccionar `ArtRanking.postman_collection.json`
3. Click **Import**
4. Configurar las variables en la colección importada
