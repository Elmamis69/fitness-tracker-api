# 🏋️ Fitness Tracker API

API para tracking de entrenamientos con **MongoDB**, **InfluxDB** y **Grafana**.

## 📋 Características

- ✅ Registro de usuarios y autenticación JWT
- ✅ CRUD de ejercicios y rutinas
- ✅ Registro de entrenamientos (sets, reps, peso)
- ✅ Mediciones corporales (peso, medidas) con historial
- ✅ Métricas en tiempo real con InfluxDB
- ✅ Visualización de progreso con Grafana

## 🗄️ Bases de Datos

- **MongoDB**: Datos estructurados (usuarios, ejercicios, rutinas)
- **InfluxDB**: Series temporales (peso, mediciones, volumen levantado, calorías)

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
npm install
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
3. Copia el token generado y pégalo en `.env` como `INFLUXDB_TOKEN`

### 5. Iniciar el servidor
```bash
npm run dev
```

El servidor estará en `http://localhost:3000`

## 📁 Estructura del Proyecto

```
src/
├── config/          # Configuración de DB
├── controllers/     # Lógica de controladores
├── middleware/      # Auth, validaciones
├── models/          # Schemas de MongoDB
├── routes/          # Definición de rutas
├── services/        # Lógica de negocio e InfluxDB
├── utils/           # Funciones auxiliares
└── index.js         # Punto de entrada
```

## 🎯 Modelos a Crear (MongoDB)

### 1. User
- email, password (hash), nombre, fecha registro
- mediciones iniciales (peso, altura)

### 2. Exercise
- nombre, descripción, categoría (pecho, espalda, piernas, etc.)
- tipo (fuerza, cardio, flexibilidad)

### 3. Workout
- usuario, fecha, duración
- ejercicios realizados (array de { exerciseId, sets: [{ reps, peso, fecha }] })
- notas

### 4. BodyMeasurement (opcional en Mongo o solo InfluxDB)
- usuario, fecha, peso, medidas (cintura, pecho, brazos, piernas)

## 📊 Métricas en InfluxDB

Datos que se guardarán como time-series:
- Peso corporal diario
- Volumen total levantado por día/semana
- Calorías quemadas
- Mediciones corporales
- Progreso por ejercicio (peso máximo, 1RM estimado)

## 🛠️ Endpoints a Implementar

### Auth
- `POST /api/users/register`
- `POST /api/users/login`
- `GET /api/users/me`

### Exercises
- `GET /api/exercises` - Listar todos
- `POST /api/exercises` - Crear nuevo
- `GET /api/exercises/:id`
- `PUT /api/exercises/:id`
- `DELETE /api/exercises/:id`

### Workouts
- `POST /api/workouts` - Registrar entrenamiento
- `GET /api/workouts` - Listar entrenamientos del usuario
- `GET /api/workouts/:id` - Detalle de entrenamiento
- `PUT /api/workouts/:id`
- `DELETE /api/workouts/:id`

### Metrics
- `POST /api/metrics/weight` - Registrar peso en InfluxDB
- `GET /api/metrics/weight` - Obtener historial de peso
- `POST /api/metrics/body-measurements` - Registrar mediciones
- `GET /api/metrics/volume` - Volumen levantado por periodo
- `GET /api/metrics/progress/:exerciseId` - Progreso en ejercicio específico

## 🎓 Guía de Aprendizaje

### Orden Recomendado:

1. **Modelo User** → AuthController → AuthMiddleware
2. **Modelo Exercise** → ExerciseController → ExerciseRoutes
3. **Modelo Workout** → WorkoutController → WorkoutRoutes
4. **MetricsService** (InfluxDB) → MetricsController → MetricsRoutes

### Lo que YO hago (automatizado):
- Crear carpetas y archivos base
- Configuración de conexiones (database.js, influxdb.js)
- Docker compose setup

### Lo que TÚ programas:
- **Models**: Schemas con validaciones
- **Controllers**: Lógica de cada endpoint
- **Services**: Interacción con InfluxDB y cálculos
- **Middleware**: Autenticación, autorización, validaciones
- **Routes**: Definir endpoints y vincular controllers

## 📦 Dependencias Principales

- `express` - Framework web
- `mongoose` - ODM para MongoDB
- `@influxdata/influxdb-client` - Cliente de InfluxDB
- `jsonwebtoken` - Autenticación JWT
- `bcryptjs` - Hash de contraseñas
- `express-validator` - Validación de datos

## 🔗 Acceso a Servicios

- API: http://localhost:3000
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
- [x] Servidor Express básico

### Fase 2: Sistema de Autenticación
- [ ] Modelo User (schema de Mongoose)
- [ ] AuthController (register, login)
- [ ] Middleware de autenticación JWT
- [ ] Rutas de autenticación
- [ ] Validaciones con express-validator

### Fase 3: Gestión de Ejercicios
- [ ] Modelo Exercise
- [ ] ExerciseController (CRUD)
- [ ] Rutas de ejercicios
- [ ] Validaciones de ejercicios

### Fase 4: Registro de Entrenamientos
- [ ] Modelo Workout
- [ ] WorkoutController (crear, listar, detalle)
- [ ] Rutas de workouts
- [ ] Guardar métricas en InfluxDB al crear workout

### Fase 5: Métricas y Estadísticas
- [ ] MetricsService para InfluxDB
- [ ] Registro de peso corporal
- [ ] Registro de mediciones corporales
- [ ] Cálculo de volumen total levantado
- [ ] Endpoint de progreso por ejercicio
- [ ] MetricsController y rutas

### Fase 6: Visualización con Grafana
- [ ] Configurar datasource de InfluxDB en Grafana
- [ ] Dashboard de peso corporal
- [ ] Dashboard de volumen levantado
- [ ] Dashboard de progreso por ejercicio
- [ ] Dashboard de mediciones corporales

### Fase 7: Mejoras y Optimizaciones
- [ ] Manejo de errores centralizado
- [ ] Logging con Winston/Morgan
- [ ] Paginación en endpoints
- [ ] Filtros y búsqueda
- [ ] Tests unitarios
- [ ] Documentación API (Swagger/Postman)

---

**¡Empieza programando!** 🚀

**Siguiente paso:** Crea el modelo `User.js` en `src/models/` y marca el checkbox cuando termines.
