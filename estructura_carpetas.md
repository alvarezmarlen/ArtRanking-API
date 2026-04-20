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
│   │   ├── migrate.py     # Flask-Migrate
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
│
│   ├── utils/
│   │   ├── jwt_utils.py
│   │   └── decoradores.py
│
├── migrations/            # generado por Flask-Migrate
│
├── run.py
├── requirements.txt
└── .env
```
