import os
from sqlalchemy import create_engine

user = os.environ.get("POSTGRES_USER")
passw = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")
db_host = os.environ.get("POSTGRES_HOST")
db_port = os.environ.get("POSTGRES_PORT")

# user = "abobus"
# passw = "qwerty"
# db_host = "127.0.0.1"
# db_name = "sh_db"
# db_port = 8002 

sql_engine = create_engine(f"postgresql+psycopg://{user}:{passw}@{db_host}:{db_port}/{db_name}")