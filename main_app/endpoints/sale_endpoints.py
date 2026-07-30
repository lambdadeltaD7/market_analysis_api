from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine
import numpy as np

def add_sale(sale: Sale):
    with Session(sql_engine) as ses:
        obj = DbSale(**sale.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj


def generate_sales(count: int):
    with Session(sql_engine) as ses:
        stmt = select(DbUser.user_id, DbUser.user_age)
        available_users = [(uid,age) for (uid,age) in ses.execute(stmt).all()]

        stmt = select(DbThing.thing_id, DbThing.category)
        available_things = [(tid,cat) for (tid,cat) in ses.execute(stmt).all()]
        

        if len(available_things) * len(available_users) == 0:
            return "you need to add items and users before that..."

    t_dict = dict()
    for tid,cat in available_things:
        if cat not in t_dict.keys():
            t_dict[cat] = [tid]
        else:
            t_dict[cat].append(tid)
    
    old_preferences = {'electronics':0.1, 'food':0.3,
                       'clothes':0.4, 'toys':0.1, 'weapons':0.1}

    young_preferences = {'electronics':0.3, 'food':0.1,
                       'clothes':0.1, 'toys':0.0, 'weapons':0.5}
    sales = []

    for _ in range(count):
        d = dict()
        uid,age = available_users[np.random.randint(0,len(available_users))]

        if age > 18:
            pref_cat = np.random.choice(
                list(old_preferences.keys()),
                p=list(old_preferences.values()))
            payment_type = np.random.choice(['card','nalik'],
                                            p=[0.3,0.7])
        else:
            pref_cat = np.random.choice(
                list(young_preferences.keys()),
                p=list(young_preferences.values()))
            payment_type = np.random.choice(['card','nalik'],
                                            p=[0.7,0.3])

        if pref_cat not in t_dict.keys():
            pref_cat = list(t_dict.keys())[0]

        tid = np.random.choice(t_dict[pref_cat])

        d["user_id"] = uid
        d["thing_id"] = tid
        d["count"] = np.random.randint(1,10)
        d["payment_type"] = payment_type

        sales.append(DbSale(**d))
        
    with Session(sql_engine) as ses:
        ses.add_all(sales)
        ses.commit()
        for s in sales:
            ses.refresh(s)

    return sales


def get_sales():
    with Session(sql_engine) as ses:
        stmt = select(DbSale)
        sales = ses.scalars(stmt).all()
    return [s.to_dict() for s in sales]


def get_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbSale).where(DbSale.sale_id == sale_id)
        sale = ses.scalar(stmt)
    if sale:
        return sale.to_dict()
    else:
        return f"there is no sale with sale_id={sale_id}"


def delete_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbSale).where(DbSale.sale_id == sale_id)
        res = ses.execute(stmt)
        ses.commit()
    return f"deleted {res.rowcount} rows"


def delete_sales():
    with Session(sql_engine) as ses:
        stmt = delete(DbSale)
        res = ses.execute(stmt)
        ses.commit()
    return f"deleted {res.rowcount} rows"