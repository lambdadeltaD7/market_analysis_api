from datetime import datetime, timedelta
from collections import Counter
from fastapi import Query, HTTPException, status
from sqlalchemy import select, delete, text
from sqlalchemy.orm import Session
from models import *
from db import sql_engine
import numpy as np

def add_sale(sale: Sale):
    with Session(sql_engine) as ses:
        d = sale.dict()
        if d["sale_time"] is None:
            d["sale_time"] = datetime.now()
        obj = DbSale(**d)
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj.to_dict()


def generate_sales(count: int):
    with Session(sql_engine) as ses:
        stmt = select(DbUser.user_id, DbUser.user_age)
        available_users = [(uid,age) for (uid,age) in ses.execute(stmt).all()]

        stmt = select(DbThing.thing_id, DbThing.category)
        available_things = [(tid,cat) for (tid,cat) in ses.execute(stmt).all()]
        

        if len(available_things) * len(available_users) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="To generate sales you must have ssome users and some things. Consider visitnig /users /things and generating some.")

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
                                            p=[0.4,0.6])
        else:
            pref_cat = np.random.choice(
                list(young_preferences.keys()),
                p=list(young_preferences.values()))
            payment_type = np.random.choice(['card','nalik'],
                                            p=[0.6,0.4])

        if pref_cat not in t_dict.keys():
            pref_cat = list(t_dict.keys())[0]

        tid = np.random.choice(t_dict[pref_cat])

        d["user_id"] = uid
        d["thing_id"] = tid
        d["count"] = np.random.randint(1,10)
        d["payment_type"] = payment_type
        d["sale_time"] = datetime.now() - timedelta(
            days=np.random.randint(0, 30),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60),
        )

        sales.append(DbSale(**d))
        
    with Session(sql_engine) as ses:
        ses.add_all(sales)
        ses.commit()
        for s in sales:
            ses.refresh(s)

    return [s.to_dict() for s in sales[:10]]

def get_sales_summary():

    d = dict()

    with Session(sql_engine) as ses:
        stmt = text("SELECT COUNT(*) FROM sales")
        res = ses.execute(stmt).one()
        d["cnt_sales"] = res._data[0]

        if d["cnt_sales"] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="No sales in database. Consider visiting /sales and generating some.")

        stmt = text("SELECT user_id, COUNT(*) FROM sales GROUP BY user_id")
        res = ses.execute(stmt).all()
        d["avg_sales_per_user"] = np.mean([cnt for uid,cnt in res])

        stmt = text("""
                    SELECT user_id, COUNT(*) AS cnt
                    FROM sales
                    GROUP BY user_id
                    ORDER BY cnt DESC
                    LIMIT 5
                    """)
        res = ses.execute(stmt).all()
        if len(res)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                       detail='No sales in database. Consider visiting /sales and generating some sales first.')
        d["most_active_users"] = [ {"user_id":uid, "cnt_sales":cnt} for uid,cnt in res ]
        
        stmt = text("""
                    SELECT thing_id, COUNT(*) AS cnt
                    FROM sales
                    GROUP BY thing_id
                    ORDER BY cnt DESC
                    LIMIT 5
                    """)
        res = ses.execute(stmt).all()
        d["most_popular_things"] = [ {"thing_id":tid, "cnt_sales":cnt} for tid,cnt in res ]

        stmt = text("""
                    SELECT t.category, COUNT(*) as cnt 
                    FROM sales s   
                    LEFT JOIN things t ON t.thing_id=s.thing_id
                    GROUP BY t.category 
                    ORDER BY cnt DESC
                    """)
        res = ses.execute(stmt).all()
        for cat,cnt in res:
            if cat is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                       detail='It seems like something in sales table is referring to thing that had been deleted')
        d["cnt_per_category"] = {cat:cnt for cat,cnt in res}
        d["frac_per_category"] = {cat:cnt / d["cnt_sales"] for cat,cnt in res}

        stmt = text("""
                    SELECT payment_type, COUNT(*)
                    FROM sales
                    GROUP BY payment_type
                    """)
        res = ses.execute(stmt).all()
        d["cnt_payment_type"] = {pt:cnt for pt,cnt in res}
        d["frac_payment_type"] = {pt:cnt / d["cnt_sales"] for pt,cnt in res}

        stmt = text("SELECT sale_time FROM sales")
        res = ses.execute(stmt).all()
        times = [x[0] for x in res if x[0] is not None]

        if times:
            d["earliest_sale_time"] = min(times).isoformat()
            d["latest_sale_time"] = max(times).isoformat()
            span_days = max((max(times) - min(times)).days, 1)
            d["avg_sales_per_day"] = len(times) / span_days
            d["avg_sales_per_hour"] = len(times) / (span_days * 24)
            hour_counts = Counter(t.hour for t in times)
            day_counts = Counter(t.date() for t in times)
            d["most_active_hour"] = hour_counts.most_common(1)[0][0]
            d["most_active_date"] = day_counts.most_common(1)[0][0].isoformat()
        else:
            d["earliest_sale_time"] = None
            d["latest_sale_time"] = None
    
    return d


def get_sales(limit: int = Query(default=100, ge=0), offset: int = Query(default=0, ge=0)):
    with Session(sql_engine) as ses:
        stmt = select(DbSale).order_by(DbSale.sale_id).offset(offset).limit(limit)
        sales = ses.scalars(stmt).all()
    return [s.to_dict() for s in sales]


def get_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = select(DbSale).where(DbSale.sale_id == sale_id)
        sale = ses.scalar(stmt)
    if sale:
        return sale.to_dict()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Sale with sale_id = {sale_id} not found")


def delete_sale(sale_id: int):
    with Session(sql_engine) as ses:
        stmt = delete(DbSale).where(DbSale.sale_id == sale_id)
        res = ses.execute(stmt)
        ses.commit()
    return {"log": f"deleted {res.rowcount} rows"}


def delete_sales():
    with Session(sql_engine) as ses:
        stmt = delete(DbSale)
        res = ses.execute(stmt)
        ses.commit()
    return {"log": f"deleted {res.rowcount} rows"}