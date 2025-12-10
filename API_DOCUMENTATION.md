# 📖 Fitness Tracker API - Complete Documentation

## 🚀 Base URL

```
http://localhost:8000
```

## 📝 Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔐 Authentication

All endpoints except `/api/auth/register` and `/api/auth/login` require authentication.

### How to Authenticate

1. Register or login to get an access token
2. Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your_access_token>
   ```

### Token Expiration

- Access tokens expire after **7 days**
- Store tokens securely (e.g., localStorage, secure cookies)

---

## 📚 Endpoints

### 🔑 Authentication

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-12-10T10:00:00"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

---

#### Login User

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

#### Get Current User

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-12-10T10:00:00"
}
```

---

### 💪 Exercises

#### Create Exercise

```http
POST /api/exercises/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Press de Banca",
  "descripcion": "Ejercicio compuesto para pecho",
  "categoria": "Pecho",
  "tipo": "Fuerza",
  "musculos_principales": ["Pectoral Mayor", "Tríceps"],
  "musculos_secundarios": ["Deltoides Anterior"],
  "equipo": "Barra",
  "dificultad": "Intermedio",
  "instrucciones": "1. Acuéstate en el banco\n2. Agarra la barra..."
}
```

**Response:** `201 Created`

---

#### List Exercises (Paginated & Filtered)

```http
GET /api/exercises/?page=1&size=10&search=Press&categoria=Pecho
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Items per page (default: 10, max: 100)
- `search` (string): Search in name, description, muscles
- `categoria` (string): Filter by category
- `tipo` (string): Filter by type

**Response:** `200 OK`
```json
{
  "items": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "nombre": "Press de Banca",
      "categoria": "Pecho",
      "tipo": "Fuerza",
      "musculos_principales": ["Pectoral Mayor", "Tríceps"]
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 10,
  "total_pages": 2,
  "has_next": true,
  "has_prev": false
}
```

---

#### Get Exercise by ID

```http
GET /api/exercises/{exercise_id}
Authorization: Bearer <token>
```

**Response:** `200 OK`

---

#### Update Exercise

```http
PUT /api/exercises/{exercise_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "descripcion": "Nueva descripción",
  "dificultad": "Avanzado"
}
```

**Response:** `200 OK`

**Note:** Only provided fields will be updated.

---

#### Delete Exercise

```http
DELETE /api/exercises/{exercise_id}
Authorization: Bearer <token>
```

**Response:** `200 OK`

---

### 🏋️ Workouts

#### Create Workout

```http
POST /api/workouts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Día de Pecho",
  "fecha": "2024-12-10T10:00:00",
  "duracion": 60,
  "notas": "Buen entrenamiento, aumenté peso",
  "ejercicios": [
    {
      "exercise_id": "507f1f77bcf86cd799439011",
      "sets": [
        {"reps": 10, "weight": 80.0, "rest_seconds": 90},
        {"reps": 8, "weight": 85.0, "rest_seconds": 90},
        {"reps": 6, "weight": 90.0, "rest_seconds": 120}
      ]
    },
    {
      "exercise_id": "507f1f77bcf86cd799439012",
      "sets": [
        {"reps": 12, "weight": 30.0, "rest_seconds": 60}
      ]
    }
  ]
}
```

**Response:** `201 Created`

**Automatic Calculations:**
- Total volume = Σ(weight × reps) across all sets
- Metrics saved to InfluxDB
- Available in Grafana dashboards

---

#### List Workouts (Paginated & Filtered)

```http
GET /api/workouts/?page=1&size=10&search=Pecho&duracion_min=45&fecha_desde=2024-01-01
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Items per page (default: 10, max: 100)
- `search` (string): Search in workout name or notes
- `fecha_desde` (date): Filter from date (YYYY-MM-DD)
- `fecha_hasta` (date): Filter to date (YYYY-MM-DD)
- `duracion_min` (int): Minimum duration in minutes
- `duracion_max` (int): Maximum duration in minutes

**Response:** `200 OK`
```json
{
  "items": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "nombre": "Día de Pecho",
      "fecha": "2024-12-10T10:00:00",
      "duracion": 60,
      "notas": "Buen entrenamiento",
      "ejercicios": [...]
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3,
  "has_next": true,
  "has_prev": false
}
```

**Sorting:** Workouts are sorted by date (newest first)

---

#### Get Workout by ID

```http
GET /api/workouts/{workout_id}
Authorization: Bearer <token>
```

**Response:** `200 OK`

---

#### Update Workout

```http
PUT /api/workouts/{workout_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "nombre": "Día de Pecho - Actualizado",
  "duracion": 75,
  "notas": "Notas actualizadas"
}
```

**Response:** `200 OK`

---

#### Delete Workout

```http
DELETE /api/workouts/{workout_id}
Authorization: Bearer <token>
```

**Response:** `200 OK`

---

### 📊 Metrics (InfluxDB)

#### Register Body Weight

```http
POST /api/metrics/weight
Authorization: Bearer <token>
Content-Type: application/json

{
  "weight": 75.5,
  "date": "2024-12-10T08:00:00"
}
```

**Response:** `201 Created`

**View in Grafana:**
- Body Weight Tracking Dashboard
- http://localhost:3001

---

#### Get Weight History

```http
GET /api/metrics/weight?start=-30d
Authorization: Bearer <token>
```

**Query Parameters:**
- `start` (string): Start time (e.g., "-30d", "-1w", "2024-01-01T00:00:00Z")
- `stop` (string): End time (optional, defaults to now)

**Response:** `200 OK`
```json
{
  "measurements": [
    {
      "time": "2024-12-10T08:00:00Z",
      "weight": 75.5,
      "user_id": "507f1f77bcf86cd799439011"
    }
  ]
}
```

---

#### Register Body Measurements

```http
POST /api/metrics/body-measurements
Authorization: Bearer <token>
Content-Type: application/json

{
  "chest": 100.0,
  "waist": 85.0,
  "hips": 95.0,
  "biceps_left": 35.0,
  "biceps_right": 35.5,
  "thigh_left": 55.0,
  "thigh_right": 55.0,
  "date": "2024-12-10T08:00:00"
}
```

**Response:** `201 Created`

**All measurements in centimeters**

---

#### Get Total Volume Lifted

```http
GET /api/metrics/volume?start=-7d&stop=now()
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "total_volume": 12500.5,
  "measurements": [
    {
      "time": "2024-12-10T10:00:00Z",
      "volume": 2500.0,
      "workout_id": "507f1f77bcf86cd799439011"
    }
  ]
}
```

**Volume = weight × reps for all sets**

---

#### Get Exercise Progress

```http
GET /api/metrics/progress/{exercise_id}?start=-90d
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "exercise_name": "Press de Banca",
  "measurements": [
    {
      "time": "2024-12-10T10:00:00Z",
      "max_weight": 90.0,
      "total_reps": 24,
      "total_volume": 2040.0,
      "workout_id": "507f1f77bcf86cd799439011"
    }
  ]
}
```

---

## 🎯 Common Use Cases

### 1. Complete Workout Flow

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}'

# Save the token from response

# 2. Create exercise (if not exists)
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Press de Banca","categoria":"Pecho","tipo":"Fuerza"}'

# 3. Create workout
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Día de Pecho","fecha":"2024-12-10T10:00:00","duracion":60,"ejercicios":[...]}'

# 4. Register weight
curl -X POST http://localhost:8000/api/metrics/weight \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"weight":75.5,"date":"2024-12-10T08:00:00"}'
```

---

### 2. Search and Filter

```bash
# Find all chest workouts from last month
GET /api/workouts/?search=Pecho&fecha_desde=2024-11-01&fecha_hasta=2024-11-30

# Find all strength exercises
GET /api/exercises/?tipo=Fuerza&page=1&size=50

# Find workouts longer than 45 minutes
GET /api/workouts/?duracion_min=45
```

---

## 📈 Grafana Dashboards

Access at: http://localhost:3001 (admin/admin)

### Available Dashboards:

1. **Body Weight Tracking**
   - Weight over time
   - Weight change trends
   - BMI calculations

2. **Workout Volume**
   - Total volume lifted per workout
   - Volume trends over time
   - Volume by muscle group

3. **Exercise Progress**
   - Max weight progression
   - Total reps over time
   - Personal records

4. **Workout Frequency**
   - Workouts per week/month
   - Training consistency
   - Rest day patterns

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 🔧 Best Practices

### 1. Pagination
- Always use pagination for large lists
- Default page size is 10, max is 100
- Check `has_next` and `has_prev` for navigation

### 2. Filtering
- Combine multiple filters for precise results
- Use search for text-based queries
- Use exact filters (categoria, tipo) for categories

### 3. Date Handling
- Always use ISO 8601 format: `2024-12-10T10:00:00`
- UTC timezone recommended
- InfluxDB queries support relative times: `-7d`, `-1w`, `-30d`

### 4. Token Management
- Store tokens securely
- Refresh tokens before expiration
- Don't expose tokens in URLs or logs

### 5. Metrics
- Register metrics consistently
- Use relative time ranges for recent data
- Check Grafana dashboards for visualization

---

## 📦 Data Models

### User
```json
{
  "_id": "string",
  "email": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### Exercise
```json
{
  "_id": "string",
  "nombre": "string",
  "descripcion": "string",
  "categoria": "string",
  "tipo": "string",
  "musculos_principales": ["string"],
  "musculos_secundarios": ["string"],
  "equipo": "string",
  "dificultad": "string",
  "instrucciones": "string",
  "user_id": "string",
  "created_at": "datetime"
}
```

### Workout
```json
{
  "_id": "string",
  "nombre": "string",
  "fecha": "datetime",
  "duracion": "integer",
  "notas": "string",
  "user_id": "string",
  "ejercicios": [
    {
      "exercise_id": "string",
      "sets": [
        {
          "reps": "integer",
          "weight": "float",
          "rest_seconds": "integer"
        }
      ]
    }
  ],
  "created_at": "datetime"
}
```

---

## 🛠️ Development

### Run Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_auth.py

# With coverage
pytest --cov=app --cov-report=html
```

### Check Logs
```bash
# Application logs (with emoji and colors!)
tail -f logs/app.log

# Docker logs
docker-compose logs -f
```

---

## 📞 Support

For issues or questions:
- Check the interactive docs at http://localhost:8000/docs
- Review the test files in `tests/` for examples
- Check the logs for detailed error messages

---

**Happy Tracking! 💪📊**
