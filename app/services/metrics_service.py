from datetime import datetime
from typing import List, Optional
from influxdb_client import Point
from influxdb_client.client.query_api import SYNCHRONOUS

from app.core.influxdb import get_write_api, get_query_api, get_influx_client
from app.core.config import get_settings
from app.schemas.metric import (
    BodyWeightMetric,
    WorkoutVolumeMetric,
    ExerciseMaxMetric,
    MetricType,
    MetricResponse
)

settings = get_settings()

class MetricsService:
    """Service for writing and reading metrics from InfluxDB"""
     
    @staticmethod
    async def write_body_weight_metric(user_id: str, metric: BodyWeightMetric):
        """Write body weight metric to InfluxDB"""
        write_api = get_write_api()

        point = Point("body_weight") \
            .tag("user_id", user_id) \
            .field("peso", metric.peso) \
            .time(metric.timestamp)
        
        write_api.write(
            bucket = settings.INFLUXDB_BUCKET,
            record = point)
        
    @staticmethod
    async def write_workout_volume(user_id: str, metric: WorkoutVolumeMetric):
        """Write workout volume metric to InfluxDB"""
        write_api = get_write_api()

        point = Point("workout_volume") \
            .tag("user_id", user_id) \
            .tag("workout_id", metric.workout_id) \
            .field("volumen_total", metric.volumen_total) \
            .time(metric.timestamp)
        
        write_api.write(
            bucket = settings.INFLUXDB_BUCKET,
            record = point)
        
    @staticmethod
    async def write_exercise_max(user_id: str, metric: ExerciseMaxMetric):
        """Write exercise max metric to InfluxDB"""
        write_api = get_write_api()

        point = Point("exercise_max") \
            .tag("user_id", user_id) \
            .tag("exercise_id", metric.exercise_id) \
            .field("peso_maximo", metric.peso_maximo) \
            .field("reps", metric.reps) \
            .time(metric.timestamp)
        
        write_api.write(
            bucket = settings.INFLUXDB_BUCKET,
            record = point)
        
    @staticmethod
    async def write_workout_count(user_id: str, timestamp: Optional[datetime] = None):
        """Write workout count metric to InfluxDB"""
        write_api = get_write_api()

        if timestamp is None:
            timestamp = datetime.utcnow()

        point = Point("workout_count") \
            .tag("user_id", user_id) \
            .field("count", 1) \
            .time(timestamp)
        
        write_api.write(
            bucket = settings.INFLUXDB_BUCKET,
            record = point)
    
    @staticmethod
    async def query_metrics(
        user_id: str,
        metric_type: MetricType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        exercise_id: Optional[str] = None,
        workout_id: Optional[str] = None
    ) -> List[MetricResponse]:
        """Query metrics from InfluxDB"""
        query_api = get_query_api()

        # Build time range filter
        time_filter = ""
        if start_date:
            time_filter += f'|> range(start: {start_date.isoformat()}Z'
            if end_date:
                time_filter += f', stop: {end_date.isoformat()}Z)'
            else:
                time_filter += ')'
        else:
            time_filter += '|> range(start: -30d)' # Default last 30 days

        # Build tag filters
        tag_filters = '|> filter(fn: (r) => r["user_id"] == "{user_id}")'

        if exercise_id and metric_type == MetricType.EXERCISE_MAX:
            tag_filters += f' |> filter(fn: (r) => r["exercise_id"] == "{exercise_id}")'

        if workout_id and metric_type == MetricType.WORKOUT_VOLUME:
            tag_filters += f' |> filter(fn: (r) => r["workout_id"] == "{workout_id}")'

        # Map metric type to measurement name
        measurement_map = {
            MetricType.BODY_WEIGHT: "body_weight",
            MetricType.WORKOUT_VOLUME: "workout_volume",
            MetricType.EXERCISE_MAX: "exercise_max",
            MetricType.WORKOUT_COUNT: "workout_count"
        }

        measurement = measurement_map[metric_type]

        # Build query
        query = f'''
        from(bucket: "{settings.INFLUXDB_BUCKET}")
            {time_filter}
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            {tag_filters}
            |> sort(columns: ["_time"], desc: false)
        '''

        result = query_api.query(query=query)

        # Parse results
        metrics = []
        for table in result:
            for record in table.records:
                metrics.append(MetricResponse(
                    timestamp = record.get_time(),
                    value = record.get_value(),
                    metadata = {
                        "field": record.get_field(),
                        **{k: v for k, v in record.values.items() if k.startswith("exercise_") or k.startswith("workout_")}
                    }
                ))
                
        return metrics