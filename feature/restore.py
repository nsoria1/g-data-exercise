import pandavro as pdx
import pandas as pd
from helper import connect_to_db, get_engine, execute_sql, files_to_restore, read_schema_file, get_table_names

### Table restore
def restore_table(table):
    files = files_to_restore(table)
    engine = get_engine()
    for file in files:
        df = pdx.read_avro(file)
        tablename = table + '2'
        print(tablename)
        df.to_sql(con=engine, name=tablename, if_exists='append', index=False)

### Schema restore
def restore_schema():
    schema_bkp = read_schema_file()
    df = pd.DataFrame.from_records(schema_bkp)
    cur, con = connect_to_db()
    df['ddl'].map(lambda x: execute_sql(con, cur, x))
    con.commit()
    con.close()
    return True

### Main
def restore():
    status = restore_schema()
    if status:
        table_list = get_table_names()
        for table in table_list:
            restore_table(table)
        return True
    else:
        return False