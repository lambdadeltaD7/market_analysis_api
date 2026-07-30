from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine


def add_thing(thing: Thing):
    with Session(sql_engine) as ses:
        obj = DbThing(**thing.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()


def get_things():
    with Session(sql_engine) as ses:
        stmt = select(DbThing)
        things = ses.scalars(stmt).all()
    return [t.to_dict() for t in things]


def get_thing(thing_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbThing).where(DbThing.thing_id == thing_id)
        res = ses.scalar(stmt) 
    if res:
        return res.to_dict()
    else:
        return f"there is no thing with thing_id={thing_id}"


def delete_thing(thing_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbThing).where(DbThing.thing_id == thing_id)
        res = ses.execute(stmt)
        ses.commit() 
    return f"deleted {res.rowcount} rows"


def delete_things():
    with Session(sql_engine) as ses:
        stmt = delete(DbThing)
        res = ses.execute(stmt)
        ses.commit() 
    return f"deleted {res.rowcount} rows"