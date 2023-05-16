import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_connect_string(env):
    adapter = env.get('DATABASE_ADAPTER', 'postgresql')
    username = env.get('DATABASE_USERNAME', 'image')
    password = env.get('DATABASE_PASSWORD', 'image')
    host = env.get('DATABASE_HOST', "db")
    port = env.get('DATABASE_PORT', 5432)
    db_name = env.get('DATABASE_NAME', 'image')
    if password:
        password = f':{password}'
    connect_string = (
        f'{adapter}://{username}{password}@{host}:{port}/{db_name}'
    )
    return connect_string


connect_string = get_connect_string(os.environ)
engine = create_engine(connect_string)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

session = SessionLocal()
