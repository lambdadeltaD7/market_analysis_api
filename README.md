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
| `nginx_app` | 8003 | Nginx обёртка на всё это |


## Документация и примеры

- Web interface for API (пока что только для юзеров и без css) `http://localhost:8003/users`
- Swagger-документация: `http://localhost:8001/docs`
- Непосредственный доступ к API: `http://localhost:8001/api/v1/`
- Доступ к API через Nginx: `http://localhost:8003/api/v1/`
- Примеры использования API: `examples.ipynb`

## Технологии

FastAPI, SQLAlchemy, PostgreSQL, pydantic, scipy, numpy, pandas, html, javascript, nginx, docker. 

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
