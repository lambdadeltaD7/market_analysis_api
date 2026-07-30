from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import mapped_column, Mapped, Session, DeclarativeBase
import os
from models import *

# user = os.environ.get("POSTGRES_USER")

user = "abobus"
passw = "qwerty"
db_host = "127.0.0.1"
db_name = "sh_db"
db_port = 8002 

sql_engine = create_engine(f"postgresql+psycopg://{user}:{passw}@{db_host}:{db_port}/{db_name}")

app = FastAPI()

@app.post("/api/v1/users")
def add_user(user: User):
    with Session(sql_engine) as ses:
        obj = DbUser(**user.model_dump())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()

@app.get("/api/v1/users")
def get_users():
    with Session(sql_engine) as ses:
        stmt = select(DbUser)
        users = ses.scalars(stmt).all()
    return [u.to_dict() for u in users]

@app.get("/api/v1/users/{user_id}")
def get_user(user_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbUser).where(DbUser.user_id == user_id)
        user = ses.scalar(stmt)
    if user:
        return user.to_dict()
    else:
        return {"error" : f"there is no user with user_id = {user_id}"}

@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbUser).where(DbUser.user_id == user_id)
        result = ses.execute(stmt)
        ses.commit()
    return {"log": f"deleted {result.rowcount} rows" }



@app.post("/api/v1/things")
def add_thing(thing: Thing):
    with Session(sql_engine) as ses:
        obj = DbThing(**thing.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()

@app.get("/api/v1/things")
def get_things():
    with Session(sql_engine) as ses:
        stmt = select(DbThing)
        things = ses.scalars(stmt).all()
    return [t.to_dict() for t in things]

@app.get("/api/v1/things/{thing_id}")
def get_thing(thing_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbThing).where(DbThing.thing_id == thing_id)
        res = ses.scalar(stmt) 
    if res:
        return res.to_dict()
    else:
        return f"there is no thing with thing_id={thing_id}"

@app.delete("/api/v1/things/{thing_id}")
def delete_thing(thing_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbThing).where(DbThing.thing_id == thing_id)
        res = ses.execute(stmt)
        ses.commit() 
    return f"deleted {res.rowcount} rows"



@app.post("/api/v1/sales")
def add_sale(sale: Sale):
    with Session(sql_engine) as ses:
        obj = DbSale(**sale.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj

@app.get("/api/v1/sales")
def get_sales():
    with Session(sql_engine) as ses:
        stmt = select(DbSale)
        sales = ses.scalars(stmt).all()
    return [s.to_dict() for s in sales]

@app.get("/api/v1/sales/{sale_id}")
def get_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbSale).where(DbSale.sale_id == sale_id)
        sale = ses.scalar(stmt)
    if sale:
        return sale.to_dict()
    else:
        return f"there is no sale with sale_id={sale_id}"

@app.delete("/api/v1/sales/{sale_id}")
def delete_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbSale).where(DbSale.sale_id == sale_id)
        res = ses.execute(stmt)
        ses.commit()
    return f"deleted {res.rowcount} rows"

