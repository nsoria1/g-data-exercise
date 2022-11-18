import pandas as pd
import pandavro as pdx
from helper import format_value, get_engine, get_table_names, BACKUP_DIR, SCHEMA_DIR

CHUNK_SIZE = 1000

### Backup schema
def backup_schema():
    query = open('get_ddl.sql', 'r').read()
    en = get_engine()
    df = pd.read_sql(query, en)
    if df.empty:
        return False
    else:
        df['ddl'] = df['ddl'].apply(format_value)
        df.to_json(SCHEMA_DIR + 'schema_backup.json', orient='records', force_ascii=True)
        return True

### Backup table
def backup_table(table):
    engine = get_engine()
    i = 1
    rowcount = pd.read_sql(sql=f"select * from {table} limit 1", con=engine)
    if rowcount.empty is False:
        for chunk in pd.read_sql(sql=f"select * from {table}", con=engine, chunksize=CHUNK_SIZE):
            filename = f'{table}_{str(i)}.avro'
            i += 1
            pdx.to_avro(BACKUP_DIR + filename, chunk)

### Main application
def backup():
    status = backup_schema()
    if status:
        table_list = get_table_names()
        for table in table_list:
            backup_table(table)
        return True
    else:
        return False