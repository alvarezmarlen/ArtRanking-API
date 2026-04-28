
# Manual de Ejecución de Seeds

Este directorio contiene los scripts para poblar la base de datos con datos de prueba para todos los modelos del sistema.

## Requisitos Previos

1. Tener el entorno virtual activado:
   ```bash
   source myEnv/bin/activate
   ```
2. Asegurarse de que MongoDB esté en ejecución.

## Cómo ejecutar los seeds

Para cargar todos los datos de una vez (Recomendado):

```bash
export PYTHONPATH=$PYTHONPATH:.
python3 seeds/main.py
```

### ¿Qué hace este script?
- **Limpia la base de datos**: Elimina los registros existentes para evitar duplicados o conflictos.
- **Crea Usuarios**: Genera 6 usuarios (1 admin y 5 usuarios normales). La contraseña para todos es `password123`.
- **Crea Perfiles**: Genera un perfil vinculado a cada usuario.
- **Crea Categorías**: Genera 5 categorías maestras (Dibujo Digital, Escultura, etc.).
- **Crea Etiquetas**: Genera 6 etiquetas para las obras.
- **Crea Concursos**: Genera 6 concursos enfocados en **Comics, Manga y Fotografía**.
- **Crea Envíos (Obras)**: Sube 10 obras distribuidas en los concursos.
- **Crea Votos y Comentarios**: Simula interacción social en las obras.
- **Crea Notificaciones**: Genera avisos para los usuarios.

## Estructura
- `main.py`: Script principal que coordina la creación de todos los registros en el orden correcto de dependencias.
