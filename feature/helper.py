import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine
import os
import json

USER='globant'
PASS='globant'
HOST='postgres'
DATABASE='data'
PORT='5432'
BACKUP_DIR = os.getcwd() + '/backup/'
SCHEMA_DIR = os.getcwd() + '/schema/'

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASS,
            host=HOST,
            port=PORT,
            database=DATABASE)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    else:
        return cursor, connection

def get_engine():
    return create_engine(f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}')

def execute_sql(con, cur, sql):
    cur.execute(sql)
    con.commit()

def files_to_restore(table):
    files = []
    for path in os.listdir(BACKUP_DIR):
        full_path = os.path.join(BACKUP_DIR, path)
        if os.path.isfile(full_path) and table in path:
            files.append(full_path)
    return files

def format_value(value):
    return str(value).replace('\n', '')

def read_schema_file():
    file = open(str(SCHEMA_DIR) + str('schema_backup.json'))
    data = json.load(file)
    return data

def get_table_names():
    table_list = []
    data = read_schema_file()
    for d in data:
        table_list.append(d['table_name'])
    return table_list