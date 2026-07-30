from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from models import *
from db import sql_engine


def add_sale(sale: Sale):
    with Session(sql_engine) as ses:
        obj = DbSale(**sale.dict())
        ses.add(obj)
        ses.commit()
        ses.refresh(obj)
    return obj


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