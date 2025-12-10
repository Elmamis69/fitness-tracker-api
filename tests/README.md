# Tests

Suite de tests unitarios para el Fitness Tracker API.

## 📦 Estructura

```
tests/
├── conftest.py          # Configuración y fixtures compartidos
├── test_auth.py         # Tests de autenticación (register, login, JWT)
├── test_exercises.py    # Tests de CRUD de ejercicios
├── test_workouts.py     # Tests de CRUD de entrenamientos
├── test_pagination.py   # Tests de utilidades de paginación
└── test_filters.py      # Tests de filtros y búsqueda
```

## 🧪 Fixtures Disponibles

- `client`: Cliente HTTP async para hacer requests
- `test_db`: Conexión a base de datos de prueba
- `test_user`: Usuario de prueba con token JWT
- `auth_headers`: Headers de autorización con token
- `test_exercise`: Ejercicio de prueba creado
- `test_workout`: Entrenamiento de prueba creado

## 🚀 Ejecutar Tests

### Todos los tests
```bash
pytest
```

### Tests con cobertura
```bash
pytest --cov=app --cov-report=html
```

### Solo tests de un módulo
```bash
pytest tests/test_auth.py
pytest tests/test_exercises.py
pytest tests/test_workouts.py
```

### Tests por categoría (markers)
```bash
pytest -m unit              # Solo tests unitarios
pytest -m integration       # Solo tests de integración
pytest -m "not slow"        # Excluir tests lentos
```

### Verbose output
```bash
pytest -v                   # Verbose
pytest -vv                  # Extra verbose
pytest -s                   # Mostrar prints
```

## 📊 Cobertura

Después de ejecutar tests con `--cov-report=html`, abre:
```bash
open htmlcov/index.html
```

## ✅ Categorías de Tests

### test_auth.py
- ✅ Registro exitoso
- ✅ Registro con email duplicado
- ✅ Registro con email inválido
- ✅ Login exitoso
- ✅ Login con credenciales incorrectas
- ✅ Acceso a rutas protegidas con/sin token

### test_exercises.py
- ✅ CRUD completo de ejercicios
- ✅ Paginación
- ✅ Filtros (search, categoria, tipo)
- ✅ Validaciones de campos
- ✅ Autorización por usuario

### test_workouts.py
- ✅ CRUD completo de entrenamientos
- ✅ Paginación
- ✅ Filtros (search, fecha, duración)
- ✅ Validaciones de campos
- ✅ Autorización por usuario

### test_pagination.py
- ✅ PaginationParams
- ✅ PaginatedResponse
- ✅ Cálculos (skip, limit, total_pages)
- ✅ Navegación (has_next, has_prev)

### test_filters.py
- ✅ WorkoutFilters (búsqueda, fechas, duración)
- ✅ ExerciseFilters (búsqueda, categoría, tipo)
- ✅ Conversión a queries de MongoDB
- ✅ Case-insensitive search

## 🔧 Configuración

El archivo `pytest.ini` contiene la configuración:
- Directorio de tests
- Modo async
- Cobertura de código
- Markers personalizados

## 📝 Notas

- Los tests usan una base de datos separada (`fitness_tracker_test`)
- La base de datos se limpia después de cada test
- Los fixtures crean datos de prueba automáticamente
- Todos los tests son asíncronos usando `pytest-asyncio`
