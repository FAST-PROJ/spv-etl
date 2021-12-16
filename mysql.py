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
from base64 import b64decode
import string
import random
import dropbox

load_dotenv()
HOST     = os.getenv('DB_HOST')
PORT     = os.getenv('DB_PORT')
USER     = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_DATABASE')
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

class dbConnection:
    def __init__(self):
        self.conn = None

    def getDatabaseConnection(self):
        self.conn = pymysql.connect(
            host       = HOST,
            port       = 3306,
            user       = USER,
            password   = PASSWORD,
            db         = DATABASE,
            autocommit=True
        )
        return self.conn.cursor()

    def closeDatabaseConnection(self):
        if self.conn != None:
            self.conn.close()

    def insertFile(self, file_name = None, file_content = None):
        bytes = b64decode(file_content, validate=True)

        if bytes[0:4] != b'%PDF':
            raise ValueError('O arquivo deve ser do tipo PDF')

        if file_name == None:
            file_name = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))

        file_name = file_name + '.pdf'

        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        dbx.files_upload(bytes, f'/local_files/{file_name}', mute=True)

        # Retornar o id do arquivo salvo na base de dados
        cursor = self.getDatabaseConnection()
        cursor.execute('INSERT INTO files (full_name) VALUES(%s)', file_name)
        cursor.close()
        self.closeDatabaseConnection()

    def insertAnswer(self, questionText, answer, score, alunoId):
        cursor = self.getDatabaseConnection()
        cursor.execute('INSERT INTO answers (question, answer, acuracy, user_id) VALUES(%s, %s, %s, %s)', questionText, answer, score, alunoId)
        cursor.close()
        self.closeDatabaseConnection()

    def getFile(self, id):
        cursor = self.getDatabaseConnection()
        cursor.execute('select id, full_name from files where id = %s', id)
        result = cursor.fetchall()[0]
        file_info = {"id":result[0], "name":result[1]}
        cursor.close()
        self.closeDatabaseConnection()

        return file_info

    def getRefinedFile(self, id, fileid):
        cursor = self.getDatabaseConnection()
        cursor.execute('select id, fileId, refinedText from refined_files where id = 35 AND fileid = 145')
        result = cursor.fetchall()[0]
        file_info = {"id": result[0], "fileid": result[1], "text": result[2]}
        cursor.close()
        self.closeDatabaseConnection()

        return file_info

    def getFiles(self):
        cursor = self.getDatabaseConnection()
        cursor.execute('select id, full_name from files')

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
