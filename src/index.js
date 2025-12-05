require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/database');
const { initInfluxDB } = require('./config/influxdb');

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Conectar bases de datos
connectDB();
initInfluxDB();

// Ruta de prueba
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Fitness Tracker API Running' });
});

// Aquí irán las rutas
// app.use('/api/users', require('./routes/userRoutes'));
// app.use('/api/workouts', require('./routes/workoutRoutes'));
// app.use('/api/exercises', require('./routes/exerciseRoutes'));
// app.use('/api/metrics', require('./routes/metricRoutes'));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
