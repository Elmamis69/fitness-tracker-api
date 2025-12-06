# 🏋️ Fitness Tracker API

API para tracking de entrenamientos con **Python**, **FastAPI**, **MongoDB**, **InfluxDB** y **Grafana**.

## 📋 Características

-  Registro de usuarios y autenticación JWT
-  CRUD de ejercicios y rutinas
-  Registro de entrenamientos (sets, reps, peso)
-  Mediciones corporales (peso, medidas) con historial
-  Métricas en tiempo real con InfluxDB
-  Visualización de progreso con Grafana

## 🗄️ Bases de Datos

- **MongoDB**: Datos estructurados (usuarios, ejercicios, rutinas)
- **InfluxDB**: Series temporales (peso, mediciones, volumen levantado, calorías)

## 🚀 Inicio Rápido

### 1. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus valores
```

### 3. Levantar servicios con Docker
```bash
docker-compose up -d
```

Esto levantará:
- **MongoDB** en `localhost:27017`
- **InfluxDB** en `localhost:8086`
- **Grafana** en `localhost:3001`

### 4. Configurar InfluxDB (primera vez)

1. Abre http://localhost:8086
2. Usuario: `admin` / Contraseña: `adminpassword`
3. El token ya está configurado: `my-super-secret-auth-token`
4. Verifica que esté en tu `.env` como `INFLUXDB_TOKEN`

### 5. Iniciar el servidor
```bash
# Opción 1: Directamente con Python
python main.py

# Opción 2: Con Uvicorn (recomendado para desarrollo)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará en `http://localhost:8000`
Documentación interactiva en `http://localhost:8000/docs`

## 📁 Estructura del Proyecto

```
app/
├── api/
│   └── routes/          # Definición de endpoints
├── core/
│   ├── config.py        # Configuración y settings
│   ├── database.py      # Conexión MongoDB
│   └── influxdb.py      # Conexión InfluxDB
├── models/              # Modelos de datos (MongoDB)
├── schemas/             # Pydantic schemas (validación)
├── services/            # Lógica de negocio
└── utils/               # Funciones auxiliares
main.py                  # Punto de entrada FastAPI
```

## 🎯 Modelos a Crear

### 1. User (MongoDB)
- email, password_hash, nombre, fecha_registro
- peso_inicial, altura

### 2. Exercise (MongoDB)
- nombre, descripción, categoría (pecho, espalda, piernas, etc.)
- tipo (fuerza, cardio, flexibilidad)
- user_id (ejercicios personalizados)

### 3. Workout (MongoDB)
- user_id, fecha, duración
- ejercicios: [{ exercise_id, sets: [{ reps, peso, fecha }] }]
- notas

### 4. Schemas (Pydantic)
- UserCreate, UserLogin, UserResponse
- ExerciseCreate, ExerciseUpdate, ExerciseResponse
- WorkoutCreate, WorkoutResponse
- MetricCreate, MetricResponse

## 📊 Métricas en InfluxDB

Datos que se guardarán como time-series:
- Peso corporal diario
- Volumen total levantado por día/semana
- Calorías quemadas
- Mediciones corporales (cintura, pecho, brazos, piernas)
- Progreso por ejercicio (peso máximo, 1RM estimado)

## 🛠️ Endpoints a Implementar

### Auth
- `POST /api/users/register` - Registrar usuario
- `POST /api/users/login` - Login (retorna JWT token)
- `GET /api/users/me` - Obtener usuario actual (requiere auth)

### Exercises
- `GET /api/exercises` - Listar todos
- `POST /api/exercises` - Crear nuevo
- `GET /api/exercises/{id}` - Detalle
- `PUT /api/exercises/{id}` - Actualizar
- `DELETE /api/exercises/{id}` - Eliminar

### Workouts
- `POST /api/workouts` - Registrar entrenamiento
- `GET /api/workouts` - Listar entrenamientos del usuario
- `GET /api/workouts/{id}` - Detalle de entrenamiento
- `PUT /api/workouts/{id}` - Actualizar
- `DELETE /api/workouts/{id}` - Eliminar

### Metrics
- `POST /api/metrics/weight` - Registrar peso en InfluxDB
- `GET /api/metrics/weight` - Obtener historial de peso
- `POST /api/metrics/body-measurements` - Registrar mediciones
- `GET /api/metrics/volume` - Volumen levantado por periodo
- `GET /api/metrics/progress/{exercise_id}` - Progreso en ejercicio específico

## 🔗 Acceso a Servicios

- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/docs
- Documentación alternativa (ReDoc): http://localhost:8000/redoc
- Grafana: http://localhost:3001 (admin/admin)
- InfluxDB: http://localhost:8086 (admin/adminpassword)

---

## 🗺️ Roadmap del Proyecto

### Fase 1: Configuración Inicial
- [x] Estructura de carpetas
- [x] Configuración de package.json
- [x] Variables de entorno (.env.example)
- [x] Docker Compose (MongoDB, InfluxDB, Grafana)
- [x] Conexión a MongoDB
- [x] Conexión a InfluxDB
### Fase 2: Sistema de Autenticación
- [ ] Schema User (Pydantic)
- [ ] Modelo User (operaciones MongoDB)
- [ ] Utilidades (hash password, create/verify JWT)
- [ ] Rutas de autenticación (register, login)
- [ ] Dependency para obtener usuario actual
- [ ] Rutas de autenticación
- [ ] Validaciones con express-validator

### Fase 3: Gestión de Ejercicios
- [ ] Schema Exercise (Pydantic)
- [ ] Modelo Exercise (CRUD MongoDB)
- [ ] Rutas de ejercicios
- [ ] Validaciones y permisos

### Fase 4: Registro de Entrenamientos
- [ ] Schema Workout (Pydantic)
- [ ] Modelo Workout (MongoDB)
- [ ] Rutas de workouts
- [ ] Guardar métricas en InfluxDB automáticamente

### Fase 5: Métricas y Estadísticas
- [ ] Service para InfluxDB (escribir/leer datos)
- [ ] Registro de peso corporal
- [ ] Registro de mediciones corporales
- [ ] Cálculo de volumen total levantado
- [ ] Endpoint de progreso por ejercicio
- [ ] Rutas de métricas

### Fase 6: Visualización con Grafana
- [ ] Configurar datasource de InfluxDB en Grafana
- [ ] Dashboard de peso corporal
- [ ] Dashboard de volumen levantado
- [ ] Dashboard de progreso por ejercicio
- [ ] Dashboard de mediciones corporales

### Fase 7: Mejoras y Optimizaciones
- [ ] Manejo de errores centralizado
- [ ] Logging (loguru o logging estándar)
- [ ] Paginación en endpoints
- [ ] Filtros y búsqueda
- [ ] Tests unitarios (pytest)
- [ ] Documentación API mejorada

---

**¡Empieza programando!** 🚀

**Siguiente paso:** Crea `app/schemas/user.py` con los schemas de Pydantic para User (UserCreate, UserLogin, UserResponse) y marca el checkbox cuando termines.
