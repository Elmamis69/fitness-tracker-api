"""InfluxDB client configuration"""
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from app.core.config import settings

client = None
write_api = None
query_api = None


def connect_to_influxdb():
    """Initialize InfluxDB client"""
    global client, write_api, query_api
    try:
        client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()
        print(" Connected to InfluxDB")
    except Exception as e:
        print(f"❌ Error connecting to InfluxDB: {e}")
        raise


def close_influxdb_connection():
    """Close InfluxDB connection"""
    global client
    if client:
        client.close()
        print("👋 Closed InfluxDB connection")


def get_write_api():
    """Get write API instance"""
    return write_api


def get_query_api():
    """Get query API instance"""
    return query_api
