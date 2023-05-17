import logging
import os
import time

from sqlalchemy.exc import SQLAlchemyError

from db.config import session
from redis_broker.config import redis_queue_name
from db.models.images import Image


def enqueue_images(event, redis_conn, folder_path):
    for filename in os.listdir(folder_path):

        # Getting the size of the image in bytes
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(folder_path, filename)
            image_bytes = os.path.getsize(image_path)

            # Record the image in the Redis queue
            redis_conn.rpush(redis_queue_name, image_bytes)

            logging.info(f"Added image {filename} to Redis queue")

        else:
            logging.warning("Фото не передались в брокер", exc_info=True)

        time.sleep(0.1)

    # Variable for the end of another thread
    event.set()


def dequeue_images(event, redis_conn):
    while True:
        # End of flow operation
        if event.is_set():
            logging.info("Done")
            break

        # Extracting an image from the Redis queue
        image_bytes = redis_conn.lpop(redis_queue_name)

        # If the queue is empty, wait a while
        if not image_bytes:
            time.sleep(0.1)
            continue

        # Getting the current time and image size
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        image_size = int(image_bytes)

        # Writing to the Postgres database
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

