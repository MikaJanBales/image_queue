import logging
import os
import time

from sqlalchemy.exc import SQLAlchemyError

from db.config import session
from redis_broker.config import redis_queue_name
from db.models.images import Image


def enqueue_images(event, redis_conn, folder_path):
    for filename in os.listdir(folder_path):

        # Получение размера изображения в байтах
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(folder_path, filename)
            image_bytes = os.path.getsize(image_path)

            # Запись изображения в Redis очередь
            redis_conn.rpush(redis_queue_name, image_bytes)

            logging.info(f"Added image {filename} to Redis queue")

        else:
            logging.warning("Фото не передались в брокер", exc_info=True)

        # Во избежание задержек
        time.sleep(1)

    # Переменная для окончания работы другого потока
    event.set()


def dequeue_images(event, redis_conn):
    while True:
        # Окончание работы потока
        if event.is_set():
            logging.info("Done")
            break

        # Извлечение изображения из Redis очереди
        image_bytes = redis_conn.lpop(redis_queue_name)

        # Если очередь пуста, подождать некоторое время
        if not image_bytes:
            time.sleep(1)
            continue

        # Получение текущего времени и размера изображения
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        image_size = int(image_bytes)

        # Запись в базу данных Postgres
        try:
            image = Image(
                time=current_time,
                size=image_size
            )
            session.add(image)
            session.commit()
        except SQLAlchemyError as error:
            logging.error(f"Ошибка при заполнении бд {error}", exc_info=True)
        except Exception as error:
            logging.error(f"Неожиданная ошибка {error}", exc_info=True)

        logging.info(
            f"Saved image to Postgres at {current_time} with size {image_size} bytes")

