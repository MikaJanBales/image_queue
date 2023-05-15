# image_queue

## Instructions for installing and running the application:

1) Up docker, thereby creating a local database, download all dependencies and run the application using the command:

```
docker-compose up
```

2) It's all.

## Assignment:

Есть набор фотографий в папке, в количестве 100 единиц.
Необходимо в коде на Python в отдельном потоке забирать фотографии из папки и складывать их в очередь в Redis.
В другом потоке извлекать из очереди фотографии и записывать при извлечении в бд Postgres в таблицу, где два поля: время
записи и размер байт изображения.
Дополнительные инструменты и подходы к решению задачи на усмотрение кандидата.