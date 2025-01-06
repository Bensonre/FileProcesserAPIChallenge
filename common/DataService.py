from random import randrange
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from configparser import ConfigParser
import pandas as pd
import psycopg2
from common.Status import Status
import json

class File(BaseModel):
    uri: str
    out_uri: str
    job_id: int
    status: str
    start_time: str
    end_time: str = ""

class Job(BaseModel):
    files: List[File] = []
    job_id: int = -1
    start_time: str
    end_time: str = ""
    status: str

class DataBaseConnector:
    _conn = None
    def __init__(self, db_params=None,db_config_file=None, schema = "public"):
        #TODO:: Implment
        self.schema = schema
        if(db_params == None and db_config_file == None):
            raise Exception('One of db_params and db_config_file is required they must not both be None.')

        if db_config_file:
            db_params = self.config(filename=db_config_file)
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self._conn = psycopg2.connect(**db_params)
            
            # create a cursor
            self._cur = self._conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        pass

    def __del__(self):
         if self._conn is not None:
            self._conn.close()
            print('Database connection closed.')
    
    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def querry_table_where(self,table, values = "*",where_condition=None, fetchall=False):
        #TODO:: implement
        self._cur.execute(f'SELECT {values} from {self.schema}."{table}"{(' where ' + where_condition) if where_condition else ""}')
        rows = None
        if(fetchall):
            rows = self._cur.fetchall()    
            columns = [desc[0] for desc in self._cur.description]
            if(rows):
                return json.loads(pd.DataFrame(rows, columns=columns).to_json(orient='records'))
        else:
            rows = self._cur.fetchone()
            columns = [desc[0] for desc in self._cur.description]
            if(rows):
                return zip(columns,rows)
        return { "error": "the file you are looking for does not exist"}   

    def insert(self,table, keys, values, returning):
        try:
            self._cur.execute(f'INSERT INTO {self.schema}."{table}" ({keys}) VALUES ({values}) RETURNING {returning};')
            self._conn.commit()
            rows = self._cur.fetchone()
            return rows[0]
        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print(error)
        return

class DataService:
    def __init__(self):
        #TODO:: Implement
        params = { 
                    'host': 'localhost',
                    'database': 'postgres',
                    'user': 'postgres',
                    'password': '8d056af4b5f14fabb34e0485df278abd'
                 }
                    
        self.db_connector = DataBaseConnector(db_params = params)
    
    def create_job(self):
        return self.db_connector.insert(table= "Jobs", keys = "start_time", values ="timezone('utc'::text, now())", returning= "job_id")
    
    def create_file(self, file: str, job_id: int, status: str, out_uri: str):
        # TODO:: Implement
        return self.db_connector.insert(table= "Files", keys = "file_name,start_time, job_id, status, out_uri", values =f"'{file}',timezone('utc'::text, now()),{job_id},'{status}','{out_uri}/{file}'", returning= "job_id")
    
    def get_job(self, job_id, attributes = "*"):
        # TODO:: Implement
        return  self.db_connector.querry_table_where(table="Jobs",  values= attributes, where_condition= f"job_id = {job_id}")
    
    
    def get_file(self, job_id,fileName, attributes = "*"):
        #TODO:: Implement
        return  self.db_connector.querry_table_where(table="Files", values= attributes, where_condition= f"job_id = {job_id} and file_name = '{fileName}'")
    
    def get_job_files(self, job_id, attributes = "*"):
        #TODO:: Implement
        #job = Job(files = File(uri="fileName",out_uri="",job_id=job_id,start_time="",end_time="", status="N/A"),job_id=job_id,start_time="",end_time="", status="n/a").files
        #return [file.uri for file in job.files]
        return self.db_connector.querry_table_where(table="Files", values= attributes, where_condition= f"job_id = {job_id}", fetchall= True)