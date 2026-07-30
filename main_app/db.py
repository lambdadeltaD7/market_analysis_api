import os
from sqlalchemy import create_engine

# user = os.environ.get("POSTGRES_USER")

user = "abobus"
passw = "qwerty"
db_host = "127.0.0.1"
db_name = "sh_db"
db_port = 8002 

sql_engine = create_engine(f"postgresql+psycopg://{user}:{passw}@{db_host}:{db_port}/{db_name}")