import redis

redis_queue_name = 'image_queue'
redis_conn = redis.Redis(
    host='redis',
    port=6379,
    charset="utf-8",
    decode_responses=True
)
