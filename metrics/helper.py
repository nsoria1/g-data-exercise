from sqlalchemy import create_engine
import pandas as pd
import json

USER='globant'
PASS='globant'
HOST='postgres'
DATABASE='data'
PORT='5432'

def get_engine():
    return create_engine(f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}')

def read_sql_file(file):
    return open(file, 'r').read()

def query_metric(filename):
    en = get_engine()
    sql = read_sql_file(filename)
    try:
        df = pd.read_sql(sql, en)
        df = df.to_json(orient='records')
        df = json.loads(df)
        return df
    except Exception as e:
        return False