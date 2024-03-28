import pandas as pd
from sqlalchemy import create_engine, text
from web_scraper.data.db_configuration import name, user, password, host, port, table
import psycopg2


def load_data(db_name, db_user, db_password, db_host, db_port, db_table):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    conn = engine.connect()
    sql_query = text(f"SELECT * FROM {table}")

    loaded_data = pd.read_sql(sql_query, conn)

    conn.close()
    return loaded_data


