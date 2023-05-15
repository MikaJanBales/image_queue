import threading

from app import enqueue_images, dequeue_images
from db.config.postgres_utils import engine, db
from db.config.redis_utils import redis_conn
from db.models.images import Base

image_folder = "./image_folder"


def main():
    # Создаем таблицу в бд Postgres
    Base.metadata.create_all(bind=engine)

    # Создание потока для чтения изображений и добавления их в Redis
    image_enqueue_thread = threading.Thread(target=enqueue_images, args=(redis_conn, image_folder))

    # Создание потока для извлечения изображений из Redis и записи их в Postgres
    image_dequeue_thread = threading.Thread(target=dequeue_images, args=(redis_conn, db))

    # Запуск потоков
    image_enqueue_thread.start()
    image_dequeue_thread.start()

    # Ожидание завершения потоков
    image_enqueue_thread.join()
    image_dequeue_thread.join()


if __name__ == '__main__':
    main()
