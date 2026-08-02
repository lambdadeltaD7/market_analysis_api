# RESTful API for market simulation/analysis

REST API для симуляции и анализа торговой площадки: управление пользователями, товарами и событиями продаж, получение аналитических сводок и кластеризация пользователей по истории покупок.

## Сущности

- **users** — пользователи (`user_id`, `user_name`, `user_age`, `bought_premium`)
- **things** — товары (`thing_id`, `category`, `price`), категории: `electronics`, `food`, `clothes`, `toys`, `weapons`
- **sales** — продажи (`sale_id`, `user_id`, `thing_id`, `count`, `payment_type`), тип оплаты: `card` / `nalik`

## Возможности

- CRUD для всех трёх сущностей + массовая генерация тестовых данных (`/generate_users`, `/generate_things`, `/generate_sales`)
- Аналитические сводки по пользователям, товарам и продажам (количество, доли, квартили цен/возраста, топ активных пользователей и популярных товаров, распределение по категориям и типу оплаты)
- **Кластеризация пользователей** (`/users/cluster_users`) на основе `kmeans2` (scipy) по признакам: число покупок, средняя/медианная цена, возраст, покупка премиума и самая частая категория товара

## Запуск

```
docker compose up
```

Состав сервисов:

| Сервис | Порт | Описание |
|--------|------|----------|
| `db_cluster` | 8002 | PostgreSQL (инициализируется из `src/db_cluster/init.sql`) |
| `main_app` | 8001 | FastAPI-приложение |

Порт 8001 можно перебиндить, отредактировав `docker-compose.yml`.

## Документация и примеры

- Swagger-документация: `http://localhost:8001/docs`
- API: `http://localhost:8001/api/v1/`
- Примеры использования: `examples.ipynb`

## Технологии

FastAPI, SQLAlchemy, PostgreSQL, pydantic, scipy, numpy, pandas.

## Структура

```
src/
├── db_cluster/   # PostgreSQL + init.sql
└── main_app/     # FastAPI приложение
    ├── server.py                 # роутинг
    ├── models.py                 # SQLAlchemy- и pydantic-модели
    ├── db.py                     # подключение к БД
    ├── logic.py                  # кластеризация (kmeans2)
    └── endpoints/                # обработчики по сущностям
```
