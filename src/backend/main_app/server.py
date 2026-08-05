from fastapi import FastAPI
from endpoints.user_endpoints import *
from endpoints.thing_endpoints import *
from endpoints.sale_endpoints import *
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Market Simulation API",
            description="""
            REST API для моделирования и анализа рынка.

            Позволяет создавать пользователей, товары и продажи,
            генерировать синтетические данные и получать сводную
            аналитику (включая кластеризацию пользователей).
            """)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# endpoints for users
app.post("/api/v1/users",
        summary="Добавить нового пользователя",
        description="""
        Позволяет руками добавить нового пользователя.
        Если нужно добавить много пользователей сразу,
        используйте /api/v1/users/generate_users
        """)(add_user)

app.post("/api/v1/users/generate_users",
 summary="Сгенерировать пользователей",
 description="""
 Создаёт заданное количество случайных пользователей
 со случайными именами, возрастом и флагом покупки премиума.
 В ответ возвращаются первые 10 созданных пользователей.
 """)(generate_users)

app.post("/api/v1/users/cluster_users",
 summary="Провести кластеризацию пользователей",
 description="Возвращает список центроид кластеров")(cluster_users)

app.get("/api/v1/users/summary",
 summary="Сводка по пользователям",
 description="""
 Возвращает агрегированную статистику: общее число пользователей,
 количество и долю купивших премиум, а также квартили по возрасту.
 """)(get_users_summary)

app.get("/api/v1/users",
 summary="Получить список пользователей",
 description="""
 Возвращает пользователей с пагинацией.
 Параметры: limit (по умолчанию 100), offset (по умолчанию 0).
 """)(get_users)

app.get("/api/v1/users/{user_id}",
 summary="Получить пользователя по id",
 description="Возвращает данные конкретного пользователя по его user_id.")(get_user)

app.get("/api/v1/users/clusters/{cluster_ix}", 
 summary="Получить всех пользователей из кластера",
 description="""
 Возвращает пользователей, попавших в кластер с заданным индексом,
 вместе с размером кластера.
 """)(get_cluster)

app.delete("/api/v1/users/{user_id}",
 summary="Удалить пользователя по id",
 description="Удаляет пользователя с указанным user_id из базы.")(delete_user)

app.delete("/api/v1/users",
 summary="Удалить всех пользователей",
 description="Полностью очищает таблицу пользователей.")(delete_users)



# endpoints for things
app.post("/api/v1/things",
 summary="Добавить новый товар",
 description="""
 Позволяет руками добавить новый товар.
 Если нужно добавить много товаров сразу,
 используйте /api/v1/things/generate_things
 """)(add_thing)

app.post("/api/v1/things/generate_things",
 summary="Сгенерировать товары",
 description="""
 Создаёт заданное количество случайных товаров
 со случайной категорией и ценой.
 В ответ возвращаются первые 10 созданных товаров.
 """)(generate_things)

app.get("/api/v1/things/summary",
 summary="Сводка по товарам",
 description="""
 Возвращает общее число товаров и для каждой категории —
 квартили цены, количество и долю товаров в категории.
 """)(get_things_summary)

app.get("/api/v1/things",
 summary="Получить список товаров",
 description="""
 Возвращает товары с пагинацией.
 Параметры: limit (по умолчанию 100), offset (по умолчанию 0).
 """)(get_things)

app.get("/api/v1/things/{thing_id}",
 summary="Получить товар по id",
 description="Возвращает данные конкретного товара по его thing_id.")(get_thing)

app.delete("/api/v1/things/{thing_id}",
 summary="Удалить товар по id",
 description="Удаляет товар с указанным thing_id из базы.")(delete_thing)

app.delete("/api/v1/things",
 summary="Удалить все товары",
 description="Полностью очищает таблицу товаров.")(delete_things)



# endpoints for sales
app.post("/api/v1/sales",
 summary="Добавить новую продажу",
 description="""
 Позволяет руками добавить новую продажу.
 Если поле sale_time не указано, подставляется текущее время.
 """)(add_sale)

app.post("/api/v1/sales/generate_sales",
 summary="Сгенерировать продажи",
 description="""
 Создаёт заданное количество случайных продаж с учётом
 возрастных предпочтений пользователей.
 В ответ возвращаются первые 10 созданных продаж.
 """)(generate_sales)

app.get("/api/v1/sales/summary",
        summary="Сводка по продажам",
        description="""
        Возвращает целую кучу ПОЛЕЗНОЙ информации:
        общее число продаж, среднее число продаж на пользователя,
        самые активные пользователи, самые популярные товары,
        распределение по категориям и способам оплаты,
        а также временные метрики (самые активные час и дата).
        """)(get_sales_summary)

app.get("/api/v1/sales",
 summary="Получить список продаж",
 description="""
 Возвращает продажи с пагинацией.
 Параметры: limit (по умолчанию 100), offset (по умолчанию 0).
 """)(get_sales)

app.get("/api/v1/sales/{sale_id}",
 summary="Получить продажу по id",
 description="Возвращает данные конкретной продажи по её sale_id.")(get_sale)

app.delete("/api/v1/sales/{sale_id}",
 summary="Удалить продажу по id",
 description="Удаляет продажу с указанным sale_id из базы.")(delete_sale)
 
app.delete("/api/v1/sales",
 summary="Удалить все продажи",
 description="Полностью очищает таблицу продаж.")(delete_sales)
