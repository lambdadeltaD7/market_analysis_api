from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine
import numpy as np
import pandas as pd

def add_thing(thing: Thing):
    with Session(sql_engine) as ses:
        obj = DbThing(**thing.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()


def generate_things(count: int):
    things = []
    means = {'electronics':6000, 'food':1000,
             'clothes':4000, 'toys':6000, 'weapons':8000}

    for _ in range(count):
        d = dict()
        d['category'] = np.random.choice(
            ['electronics', 'food', 'clothes', 'toys', 'weapons'])

        d['price'] = min(int(np.random.normal(
            loc=means[d['category']],scale=1000)), 10000)
            
        things.append(DbThing(**d))

    with Session(sql_engine) as ses:
        ses.add_all(things)
        ses.commit()
        for t in things:
            ses.refresh(t)

    return things


def get_things_summary():
    with Session(sql_engine) as ses:
        stmt = select(DbThing.category, DbThing.price)
        things = ses.execute(stmt).all()

    df = pd.DataFrame([(c,p) for c,p in things], columns=["cat","price"])
    df["price"] = pd.to_numeric(df["price"])

    d = dict()
    d['cnt_things'] = df.shape[0]
    for cat in df['cat'].unique():
        d[cat] = dict()
        d[cat]["price_quartiles"] = df[df['cat']==cat]['price'].quantile([0.25,0.5,0.75])
        d[cat]["cnt_things"] = df[df['cat']==cat].shape[0]
        d[cat]["frac_things"] = df[df['cat']==cat].shape[0] / df.shape[0]

    return d


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