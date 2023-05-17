import threading

from logs.log import setup_logging
from queues import enqueue_images, dequeue_images
from db.config import engine
from redis_broker.config import redis_conn
from db.models.images import Base

image_folder = "./image_folder"


def main():
    # Connecting Logging
    setup_logging()

    # Creating a table in a Postgres database
    Base.metadata.create_all(bind=engine)

    # Creating an event to synchronize threads
    event = threading.Event()

    # Creating a thread to read images and add them to Redis
    image_enqueue_thread = threading.Thread(target=enqueue_images,
                                            args=(
                                                event, redis_conn,
                                                image_folder))

    # Creating a stream to extract images from Redis and write them to Postgres
    image_dequeue_thread = threading.Thread(target=dequeue_images,
                                            args=(event, redis_conn))

    # Starting threads
    image_enqueue_thread.start()
    image_dequeue_thread.start()

    # Waiting for threads to complete
    image_enqueue_thread.join()
    image_dequeue_thread.join()


if __name__ == "__main__":
    main()
