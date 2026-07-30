from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine


def add_user(user: User):
    with Session(sql_engine) as ses:
        obj = DbUser(**user.model_dump())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()


def get_users():
    with Session(sql_engine) as ses:
        stmt = select(DbUser)
        users = ses.scalars(stmt).all()
    return [u.to_dict() for u in users]


def get_user(user_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbUser).where(DbUser.user_id == user_id)
        user = ses.scalar(stmt)
    if user:
        return user.to_dict()
    else:
        return {"error" : f"there is no user with user_id = {user_id}"}


def delete_user(user_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbUser).where(DbUser.user_id == user_id)
        result = ses.execute(stmt)
        ses.commit()
    return {"log": f"deleted {result.rowcount} rows" }


def delete_users():
    with Session(sql_engine) as ses:
        stmt = delete(DbUser)
        result = ses.execute(stmt)
        ses.commit()
    return {"log": f"deleted {result.rowcount} rows" }