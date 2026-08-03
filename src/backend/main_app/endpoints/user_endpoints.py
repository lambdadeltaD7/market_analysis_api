from fastapi import Query
from sqlalchemy import select, delete, text
from sqlalchemy.orm import Session
from models import *
from db import sql_engine
from logic import do_cluster
import numpy as np
import pandas as pd


def get_cluster(cluster_ix: int):
    with Session(sql_engine) as ses:
        query = text(f"SELECT * FROM clusters where cluster={cluster_ix}")
        raw = ses.execute(query).all()

    if len(raw)==0:
        return {"error": f"there is no cluster with cluster_ix={cluster_ix}"}

    users = []

    for x in raw:
        d = dict()
        d["user_id"] = x[1]
        d["cluster"] = x[2]
        d["cnt_sales"] = x[3]
        d["avg_price"] = x[4]
        d["med_price"] = x[5]
        d["user_age"] = x[6]
        d["bought_premium"] = x[7]
        d["mode_category"] = x[8]
        users.append(d)

    return {"cluster_size":len(raw), "users":users}

def cluster_users(n_clusters: int):
    with Session(sql_engine) as ses:

        query = text("TRUNCATE TABLE clusters;")
        ses.execute(query)

        query = text("""
            SELECT
            s.user_id,
            COUNT(*),
            AVG(t.price),
            percentile_cont(0.5) WITHIN GROUP(ORDER BY t.price),
            u.user_age,
            u.bought_premium,
            MODE() WITHIN GROUP(ORDER BY t.category)
            FROM sales s
            LEFT JOIN users u ON s.user_id=u.user_id
            LEFT JOIN things t ON t.thing_id=s.thing_id
            GROUP BY s.user_id, u.user_age, u.bought_premium
        """)
        res = ses.execute(query).all()

        ses.commit()

    df = pd.DataFrame([x for x in res], 
                     columns=['user_id', 'cnt_sales', 'avg_price', 
                            'med_price', 'user_age', 'bought_premium',
                            'mode_category'])
    for col in ['user_id', 'med_price', 'cnt_sales', 'avg_price','user_age']:
        df[col] = pd.to_numeric(df[col])

    centroids, labels = do_cluster(df, n_clusters)

    df["cluster"] = labels

    df.to_sql(
        name="clusters",
        index=False,
        con = sql_engine,
        if_exists="append"
    )

    return centroids


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
            d["bought_premium"] = np.random.choice([True,False],p=[0.52, 0.48])
        else:
            d["bought_premium"] = np.random.choice([True,False],p=[0.48, 0.52])

        users.append(DbUser(**d))

    with Session(sql_engine) as ses:
        ses.add_all(users)
        ses.commit()
        for u in users:
            ses.refresh(u)

    return [u.to_dict() for u in users[:10]]



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


def get_users(limit: int = Query(default=100, ge=0), offset: int = Query(default=0, ge=0)):
    with Session(sql_engine) as ses:
        stmt = select(DbUser).order_by(DbUser.user_id).offset(offset).limit(limit)
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