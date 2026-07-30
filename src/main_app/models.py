from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import mapped_column, Mapped, Session, DeclarativeBase



class DbBase(DeclarativeBase):
    pass



class DbUser(DbBase):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    user_age: Mapped[int]
    bought_premium: Mapped[bool] 

    def __str__(self) -> str:
        return f"user_id: {self.user_id}\n user_name: {self.user_name}\n" + \
               f"user_age: {self.user_age}\n bought_premium: {self.bought_premium}"

    def to_dict(self) -> dict:
        return {"user_id": self.user_id, "user_name": self.user_name,
             "user_age": self.user_age, "bought_premium": self.bought_premium}


class User(BaseModel):
    user_name: str = Field(max_length=10, description="Имя пользователя")
    user_age: int = Field(ge=0, le=100, description="Возраст пользователя")
    bought_premium: bool =  Field(description="Указывает, приобрёл ли пользователь премиум")



class DbThing(DbBase):
    __tablename__ = "things"
    thing_id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    price: Mapped[int]

    def to_dict(self) -> dict:
        return {"thing_id": self.thing_id, "category": self.category,
             "price": self.price}
    
class Thing(BaseModel):
    category: Literal['electronics', 'food', 'clothes', 'toys', 'weapons']
    price: int = Field(ge=1, le=10000)



class DbSale(DbBase):
    __tablename__ = "sales"
    sale_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    thing_id: Mapped[int]
    count: Mapped[int]
    payment_type: Mapped[str]

    def to_dict(self) -> dict:
        return {"sale_id": self.sale_id, "user_id": self.user_id,
                "thing_id": self.thing_id, "count": self.count, 
                "payment_type": self.payment_type}

class Sale(BaseModel):
    user_id: int
    thing_id: int
    count: int = Field(ge=1, le=67)
    payment_type: Literal['card', 'nalik']



