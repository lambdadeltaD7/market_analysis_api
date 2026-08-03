from fastapi import FastAPI
from endpoints.user_endpoints import *
from endpoints.thing_endpoints import *
from endpoints.sale_endpoints import *

app = FastAPI(title="Market Simulation API",
            description="""
            SOME DESCR HERE
            SOME DESCR HERE
            SOME DESCR HERE
            SOME DESCR HERE
            """)

app.post("/api/v1/users",
        summary="Добавить нового пользователя",
        description="""
        Позволяет руками добавить нового пользователя.
        Если нужно добавить много пользователей сразу,
        используйте /api/v1/users/generate_users
        """)(add_user)
app.post("/api/v1/users/generate_users")(generate_users)
app.post("/api/v1/users/cluster_users",
 summary="Провести кластеризацию пользователей",
 description="Возвращает список центроид кластеров")(cluster_users)
app.get("/api/v1/users/summary")(get_users_summary)
app.get("/api/v1/users")(get_users)
app.get("/api/v1/users/{user_id}")(get_user)
app.get("/api/v1/users/clusters/{cluster_ix}", 
summary="Получить всех пользователей из кластера")(get_cluster)
app.delete("/api/v1/users/{user_id}")(delete_user)
app.delete("/api/v1/users")(delete_users)

app.post("/api/v1/things")(add_thing)
app.post("/api/v1/things/generate_things")(generate_things)
app.get("/api/v1/things/summary")(get_things_summary)
app.get("/api/v1/things")(get_things)
app.get("/api/v1/things/{thing_id}")(get_thing)
app.delete("/api/v1/things/{thing_id}")(delete_thing)
app.delete("/api/v1/things")(delete_things)

app.post("/api/v1/sales")(add_sale)
app.post("/api/v1/sales/generate_sales")(generate_sales)
app.get("/api/v1/sales/summary",
        summary="Сводка по продажам",
        description="Целая куча ПОЛЕЗНОЙ информации")(get_sales_summary)
app.get("/api/v1/sales")(get_sales)
app.get("/api/v1/sales/{sale_id}")(get_sale)
app.delete("/api/v1/sales/{sale_id}")(delete_sale)
app.delete("/api/v1/sales")(delete_sales)

