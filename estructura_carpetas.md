```text
artranking-api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│
│   ├── extensiones/
│   │   ├── __init__.py
│   │   ├── db.py          # instancia de mongodb engine
│   │   
│   │
│   ├── models/            # AQUÍ VAN TUS ENTIDADES
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── perfil.py
│   │   ├── concurso.py
│   │   ├── categoria.py
│   │   ├── envio.py
│   │   ├── voto.py
│   │   ├── comentario.py
│   │   ├── etiqueta.py
│   │   ├── envio_etiqueta.py
│   │   └── notificacion.py
│
│   ├── routes/
│   │   ├── auth_rutas.py
│   │   ├── concurso_rutas.py
│   │   ├── envio_rutas.py
│   │   ├── voto_rutas.py
│   │   └── usuario_rutas.py
│
│   ├── services/         # lógica de negocio
│   │   ├── auth_servicio.py
│   │   ├── concurso_servicio.py
│   │   ├── envio_servicio.py
│   │   └── voto_servicio.py
│
│   ├── schemas/          # validación / serialización
│   │   ├── usuario_esquema.py
│   │   ├── envio_esquema.py
│   │   └── voto_esquema.py
|   
│   ├── static/               # Archivos públicos del navegador
│   │   ├── css/
│   │   │   └── style.css     # Diseño y reglas SEO
│   │   ├── js/
│   │   │   └── main.js       # Interactividad y validación cliente
│   │   └── img/              # Imágenes y logos del sistema
│
|   
│   ├── templates/            # Motor de plantillas Jinja2
│   │   ├── layouts/
│   │   │   └── base.html     # Estructura maestra
│   │   ├── macros/
│   │   │   └── componentes.html
│   │   ├── errores/
│   │   │   └── 404.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── registro.html
│   │   ├── concursos/
│   │   │   ├── lista.html
│   │   │   └── detalle.html
│   │   ├── envios/
│   │   │   ├── subir_obra.html
│   │   │   └── galeria.html
│   │   └── perfil/
│   │       └── ver_perfil.html
|
│   ├── utils/
│   │   ├── jwt_utils.py
│   │   └── decoradores.py
│
│
├── myEnv
├──.env
├── config.py
├── requirements.txt
└── run.py
```
