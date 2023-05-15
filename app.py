import os
import time

from sqlalchemy.orm import Session

from db.config.redis_utils import redis_queue_name
from db.models.images import Image


def enqueue_images(redis_conn, folder_path):
    for filename in os.listdir(folder_path):

        # Получение размера изображения в байтах
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            image_bytes = os.path.getsize(image_path)

            # Запись изображения в Redis очередь
            redis_conn.rpush(redis_queue_name, image_bytes)

            print(f'Added image {filename} to Redis queue')

            # Опциональная задержка между добавлением изображений
            time.sleep(0.1)


def dequeue_images(redis_conn, session: Session):
    while True:
        # Извлечение изображения из Redis очереди
        image_bytes = redis_conn.lpop(redis_queue_name)

        # Если очередь пуста, подождать некоторое время
        if image_bytes is None:
            time.sleep(1)
            continue

        # Получение текущего времени и размера изображения
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        image_size = len(image_bytes)

        # Запись в базу данных Postgres
        try:
            image = Image(
                time=current_time,
                size=image_size
            )
            session.add(image)
            session.commit()
        except Exception as error:
            print("Ошибка при работе с PostgreSQL", error)

        print(f'Saved image to Postgres at {current_time} with size {image_size} bytes')
