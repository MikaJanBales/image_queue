import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logs/py_log.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
        filemode="w"
    )
