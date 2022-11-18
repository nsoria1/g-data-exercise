import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#a = loader.Loader('/Users/nsoria/Documents/github-nsoria/g-data-exercise/endpoint/test/jobs.csv')
class Loader:
    def __init__(self, path):
        self.path = path
        assert os.path.split(self.path)[1].split(".")[0] in ('hired_employees', 'jobs', 'departments'), "Filename unexpected."
        self.entity = os.path.split(self.path)[1].split(".")[0]
        self.db = create_engine('postgresql://globant:globant@postgres/data')
        self.schema = self.__set_required_schema()

    def __set_required_schema(self):
        if self.entity == 'hired_employees':
            return {'id': int, 'name': str, 'datetime': str, 'department_id': int, 'job_id': int}
        elif self.entity == 'departments':
            return {'id': int, 'department': str}
        elif self.entity == 'jobs':
            return {'id': int, 'job': str}
    
    def __cast_df(self, df: pd.DataFrame):
        df.columns = list(self.schema.keys())
        df = df.astype(self.schema)
        df = df.replace({'nan': np.nan})
        return df

    @staticmethod
    def __run_data_validations(df: pd.DataFrame):
        return df.isnull().values.any()
    
    def __load_batch(self, df, table='error_log'):
        df.to_sql(table, con=self.db, if_exists='append', index=False)

    @staticmethod
    def __prepare_bad_df(df, entity, message):
        df['data'] = df[list(df.columns)].apply(lambda row: ','.join([s.strip() for s in row.values.astype(str)]), axis=1)
        df = df[['data']].copy()
        df['entity'] = entity
        df['msg'] = message
        return df

    def process_data(self):
        self.status = 0
        with pd.read_csv(self.path, header=None, chunksize=1) as reader:
            reader
            for chunk in reader:
                try:
                    df = self.__cast_df(chunk)
                    validation = self.__run_data_validations(df)
                except ValueError:
                    df = self.__prepare_bad_df(chunk, self.entity, f'ValueError: Please review source file: {os.path.split(self.path)[1]}')
                    self.status += 1
                else:
                    if validation:
                        df = self.__prepare_bad_df(df, self.entity, f'Validation Error, please review the rules')
                        self.status += 1
                        self.__load_batch(df)
                    else:
                        self.__load_batch(df, table=self.entity)