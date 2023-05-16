import threading

from logs.log import setup_logging
from queues import enqueue_images, dequeue_images
from db.config import engine
from redis_broker.config import redis_conn
from db.models.images import Base

image_folder = "./image_folder"


def main():
    # Подключение логирование
    setup_logging()

    # Создание таблицу в бд Postgres
    Base.metadata.create_all(bind=engine)

    # Создание события для синхронизации потоков
    event = threading.Event()

    # Создание потока для чтения изображений и добавления их в Redis
    image_enqueue_thread = threading.Thread(target=enqueue_images,
                                            args=(
                                                event, redis_conn,
                                                image_folder))

    # Создание потока для извлечения изображений из Redis
    # и записи их в Postgres
    image_dequeue_thread = threading.Thread(target=dequeue_images,
                                            args=(event, redis_conn))

    # Запуск потоков
    image_enqueue_thread.start()
    image_dequeue_thread.start()

    # Ожидание завершения потоков
    image_enqueue_thread.join()
    image_dequeue_thread.join()


if __name__ == "__main__":
    main()
