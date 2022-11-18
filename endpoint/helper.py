from sqlalchemy import create_engine

USER='globant'
PASS='globant'
HOST='postgres'
DATABASE='data'
PORT='5432'

def get_engine():
    return create_engine(f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DATABASE}')