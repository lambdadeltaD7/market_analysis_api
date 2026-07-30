from fastapi import FastAPI
from endpoints.user_endpoints import *
from endpoints.thing_enpoints import *
from endpoints.sale_endpoints import *

app = FastAPI()

app.post("/api/v1/users")(add_user)
app.post("/api/v1/users/generate_users")(generate_users)
app.get("/api/v1/users")(get_users)
app.get("/api/v1/users/{user_id}")(get_user)
app.delete("/api/v1/users/{user_id}")(delete_user)
app.delete("/api/v1/users")(delete_users)

app.post("/api/v1/things")(add_thing)
app.post("/api/v1/things/generate_things")(generate_things)
app.get("/api/v1/things")(get_things)
app.get("/api/v1/things/{thing_id}")(get_thing)
app.delete("/api/v1/things/{thing_id}")(delete_thing)
app.delete("/api/v1/things")(delete_things)

app.post("/api/v1/sales")(add_sale)
app.get("/api/v1/sales")(get_sales)
app.get("/api/v1/sales/{sale_id}")(get_sale)
app.delete("/api/v1/sales/{sale_id}")(delete_sale)
app.delete("/api/v1/sales")(delete_sales)

