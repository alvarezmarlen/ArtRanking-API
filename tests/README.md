# GUÍA DE TESTS

## Requisitos Previos

- Virtualenv activado
- mongomock instalado

## Cómo ejecutar los tests

```bash
source myEnv/bin/activate
pytest tests/test_simple.py -v
```

## ¿Qué significa la salida?

- **PASSED**: El test pasó (bien) ✅
- **FAILED**: El test falló (mal) ❌
- **ERROR**: Hubo un error (mal) ❌

## ¿Qué testea cada clase?

### TestPaginasPublicas
- Verifica que las páginas carguen
- Páginas: inicio, concursos, ranking, login, registro

### TestAPIs
- Verifica que las APIs funcionen
- APIs: concursos, envíos

### TestErrores
- Verifica errores (404)

### TestModelos
- Verifica que los modelos se creen bien
- Modelos: Usuario, Concurso, Envio
