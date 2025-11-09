# Тестовое задание UCAR<>TOPDOER

## Запуск

1. Устанавливаем [Docker](https://www.docker.com/products/docker-desktop/).
2. Клонируем репозиторий и идем внутрь.
   ```shell
   git clone git@github.com:pgoltsev/test_ucar_topdoer.git 
   ```
3. Запускаем сервер и базу данных:
   ```shell
   docker compose up -d
   ```

## Тестирование

1. Создаем несколько инцидентов:
   ```shell
   curl -X POST --location "http://localhost:8081/api/v1/incidents" \
    -H "Content-Type: application/json" \
    -d '{
          "description": "Случилась беда!",
          "status": "submitted",
          "source": "partner"
        }'
   ```
   ```shell
   curl -X POST --location "http://localhost:8081/api/v1/incidents" \
    -H "Content-Type: application/json" \
    -d '{
          "description": "Случилась вторая беда!",
          "status": "submitted",
          "source": "monitoring"
        }'
   ```
   ```shell
   curl -X POST --location "http://localhost:8081/api/v1/incidents" \
    -H "Content-Type: application/json" \
    -d '{
          "description": "Случилась третья беда!",
          "status": "submitted",
          "source": "monitoring"
        }'
   ```
2. Меняем статус одного из созданных:
   ```shell
   curl -X PATCH --location "http://localhost:8081/api/v1/incidents/1/status" \
    -H "Content-Type: application/json" \
    -d '{
          "status": "acknowledged"
        }'
   ```
3. Получаем инциденты с указанным статусом:
   ```shell
   curl -X GET --location "http://localhost:8081/api/v1/incidents/?status=submitted" \
    -H "Accept: application/json"
   ```
   ```shell
   curl -X GET --location "http://localhost:8081/api/v1/incidents/?status=acknowledged" \
    -H "Accept: application/json"
   ```
4. Пробуем несуществующий инцидент:
   ```shell
   curl -X PATCH --location "http://localhost:8081/api/v1/incidents/0/status" \
    -H "Content-Type: application/json" \
    -d '{
          "status": "acknowledged"
        }'
   ```