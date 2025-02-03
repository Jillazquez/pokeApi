# utils/redis_client.py
import redis
import os
from utils.Logger import Logger
def connect_to_redis():
    """Conectar a Redis y devolver el cliente Redis."""
    try:
        redis_host = os.getenv("REDIS_HOST", "redis")  # Usar la variable de entorno REDIS_HOST
        redis_port = os.getenv("REDIS_PORT", 6379)    # Puerto por defecto de Redis
        r = redis.Redis(host=redis_host, port=redis_port)
        if r.ping():
            print("Conectado a Redis.")
        return r
    except redis.ConnectionError as e:
        logger = Logger()
        logger.add_to_log("error", f"Error al conectar con Redis: {e}")
        return None