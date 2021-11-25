#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

import pymysql
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
HOST     = os.getenv('DB_HOST')
PORT     = os.getenv('DB_PORT')
USER     = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_DATABASE')

class dbConnection:
    def __init__(self):
        self.conn = None

    def getDatabaseConnection(self):
        self.conn = pymysql.connect(
            host       = HOST,
            port       = PORT,
            user       = USER,
            password   = PASSWORD,
            db         = DATABASE,
            autocommit=True
        )
        return self.conn.cursor()

    def closeDatabaseConnection(self):
        if self.conn != None:
            self.conn.close()

    def insertFile(self, file_name):
        cursor = self.getDatabaseConnection()
        cursor.execute(f"""INSERT INTO text.files (full_name) VALUES ('{file_name}');""")
        cursor.close()
        self.closeDatabaseConnection()

    def getFile(self, id):
        cursor = self.getDatabaseConnection()
        cursor.execute(f"""
                        select
                        id,
                        full_name
                        from
                        text.files
                        where
                        id = {id}
                    """)

        cursor.close()
        self.closeDatabaseConnection()

        result = cursor.fetchall()[0]

        file_info = {"id":result[0], "name":result[1]}

        return file_info

    def getFiles(self):
        cursor = self.getDatabaseConnection()
        cursor.execute("""select id, full_name from text.Files""")

        filesList = []
        for item in cursor.fetchall():
            filesList.append({"id":item[0], "name":item[1]})

        cursor.close()
        self.closeDatabaseConnection()
        return filesList

    def insertRawText(self, insertDataframe):
        engine = create_engine('mysql+pymysql://'+ USER +':'+ PASSWORD +'@'+ HOST +'/'+ DATABASE)
        insertDataframe.columns = ['fileId', 'rawText']
        insertDataframe.set_index('fileId', inplace=True)
        insertDataframe.to_sql('ingestion_files', con = engine, if_exists='append')

    def insertRefinedText(self, insertDataframe):
        engine = create_engine('mysql+pymysql://'+ USER +':'+ PASSWORD +'@'+ HOST +'/'+ DATABASE)
        insertDataframe.columns = ['fileId', 'refinedText']
        insertDataframe.set_index('fileId', inplace=True)
        insertDataframe.to_sql('refined_files', con = engine, if_exists='append')

    def insertFeatureText(self, insertDataframe):
        engine = create_engine('mysql+pymysql://'+ USER +':'+ PASSWORD +'@'+ HOST +'/'+ DATABASE)
        insertDataframe.columns = ['fileId', 'word', 'sentence']
        insertDataframe.set_index('fileId', inplace=True)
        insertDataframe.to_sql('feature_files', con = engine, if_exists='append')
