from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine
import numpy as np
import pandas as pd

def add_user(user: User):
    with Session(sql_engine) as ses:
        obj = DbUser(**user.model_dump())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()


def generate_users(count: int):
    users = []
    for _ in range(count):
        d=dict()

        d["user_name"] = np.random.choice(["makise ", "alex ", "mittermier ", "yui "]) + \
        np.random.choice(["von loeingram", "hirasawsa",
                         "le monon","lando"])

        d["user_age"] = np.random.randint(1,99)

        if d["user_age"] > 18:
            d["bought_premium"] = np.random.choice([True,False],p=[0.7, 0.3])
        else:
            d["bought_premium"] = np.random.choice([True,False],p=[0.3, 0.7])

        users.append(DbUser(**d))

    with Session(sql_engine) as ses:
        ses.add_all(users)
        ses.commit()
        for u in users:
            ses.refresh(u)

    return users



def get_users_summary():
    with Session(sql_engine) as ses:
        stmt = select(DbUser.user_age, DbUser.bought_premium)
        users = ses.execute(stmt).all()

    df = pd.DataFrame([(age,prem) for age,prem in users], columns=["age","prem"])
    res = dict()

    res["cnt_users"] = df.shape[0]
    res["cnt_premium_users"] = float(df["prem"].sum())
    res["frac_premium_users"] = df["prem"].mean()
    res["quartiles(age)"] = df["age"].quantile([0.25, 0.5, 0.75])
    
    return res


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