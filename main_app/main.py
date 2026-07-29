from fastapi import FastAPI
from funcs import *
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# user = os.environ.get("POSTGRES_USER")
# passw = os.environ.get("POSTGRES_PASSWORD")
# db_host = os.environ.get("POSTGRES_HOST")
# db_port = os.environ.get("POSTGRES_PORT")
# db_name = os.environ.get("POSTGRES_DB")

user = "abobus"
passw = "qwerty"
db_host = "127.0.0.1"
db_port = "8002"
db_name = "sh_db"

sql_engine = create_engine(f"postgresql+psycopg://{user}:{passw}@{db_host}:{db_port}/{db_name}")

@app.get("/api/v1/search")
def search(query: str, obj_type: str):
    if obj_type == "stock":
        return find_stocks(query).to_dict(orient="records")
    elif obj_type == "currency":
        return find_currencies(query).to_dict(orient="records")
    else:
        return {"error": f"obj_type must be stock or currency. Got {obj_type}."}


@app.post("/api/v1/things")
def add_thing(thing_name: str, obj_type: str):
    if obj_type == "stock":
        if not stock_exists(thing_name):
            return {"error": f"there is no such stock in moex: {thing_name}"}
    elif obj_type == "currency":
        if not currency_exists(thing_name):
            return {"error": f"there is no such currency in moex: {thing_name}"}
    else:
        return {"error": f"obj_type must be stock or currency. Got {obj_type}."}

    with sql_engine.connect() as connection:
        res = connection.execute(
            text(f"INSERT INTO things (thing_name,type) VALUES (:thing_name, :obj_type)"),
            {"thing_name":thing_name,"obj_type":obj_type}
            )
        connection.commit()
    # return str(res.fetchall())

@app.get("/api/v1/things")
def get_things():
    with sql_engine.connect() as connection:
        res = connection.execute(
            text("SELECT * FROM things")
        )
        connection.commit()
    return str(res.fetchall())
