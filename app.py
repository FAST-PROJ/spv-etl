#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from flask import Flask, request, jsonify
from flask import render_template
from mysql import dbConnection
from reader import Reader
from cleaner import Cleaner
from feature import Feature
import pandas as pd
from transformers import pipeline
from bertSingleton import Bert

app = Flask(__name__)

# Inicia a classe de conexão com o banco
connection = dbConnection()
# Inicia a classe de leitura do arquivo
reader = Reader()
# Inicia a classe de limpeza
cleaner = Cleaner()
# Inicia a classe de features
feature = Feature()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/insertFiles', methods=['POST'])
def insertFiles():
    input_json = request.get_json(force=True)
    # 1 - Pegar o id do arquivo salvo
    id = connection.insertFile(input_json['file_name'], input_json['file_content'])

    rawText(id)
    refinedText()
    featureText()
    return '200'

@app.route('/recebePergunta', methods=['POST'])
def processFiles():
    input_json = request.get_json(force=True)
    alunoID = input_json['id']
    questionText = input_json['question']
    contextData = connection.getRefinedFile(35, 145)

    bert = Bert.instance()
    result = bert(question=[questionText], context=contextData['text'])

    connection.insertAnswer(questionText, result['answer'], result['score'], alunoID)
    # 1 - SELECT FROM refined_files WHERE ID = 35 AND fileid = 145
    #       Utilizar o metodo connection.getRefinedFile(35, 145)
    # 2 - SALVAR A PERGUNTA `questionText`, o ID do aluno `alunoID` e a resposta (gerada pelo BERTI) acuracy Na tabela answers
    # 3 - Chamar o endpoint de notificação do chatbot
    #       http://senac-professor-virtual.herokuapp.com/api/notifications
    #       POST
    #       {
    #           "id": 1,
    #           "answer": "IA é uma áres de estudo"
    #       }
    return '200'

def rawText(id):
    # Preenche o parametro de fileId
    reader.setFileId(id)

    # Coleta as informações do banco de dados a partir do id do arquivo
    file = connection.getFile(reader.getFileId())

    # Leitura do arquivo da pasta source
    reader.setTextFromPdf(f"{file['name']}")

    # Cria um dicionario com as informações do arquivo
    rawText = {
        "id": [reader.getFileId()],
        "text":[reader.getTextFromPdf()]
    }

    # Efetua o insert na camada bronze
    connection.insertRawText(pd.DataFrame(data=rawText))

def refinedText():
    numbersClean = cleaner.removeIsolatedNumbers(reader.getTextFromPdf())
    spaceClean = cleaner.removeSpaces(numbersClean)
    blankClean = cleaner.removeBlankLines(spaceClean)
    cleanText = cleaner.removeSpecialCaracteres(blankClean)
    cleaner.setCleanText(cleanText)

    # Cria um dicionario com as informações do arquivo
    refinedText = {
        "id": [reader.getFileId()],
        "text":[cleaner.getCleanText()]
    }

    # Efetua o insert na camada silver
    connection.insertRefinedText(pd.DataFrame(data=refinedText))

def featureText():
    feature.setSentenceToList(cleaner.getCleanText())
    feature.setWordToList(cleaner.getCleanText())

    # Cria um dicionario com as informações do arquivo
    featureText = {
        "id": [reader.getFileId()],
        "word":[str(feature.getWordToList())],
        "sentence":[str(feature.getSentenceToList())]
    }

    # Efetua o insert na camada gold
    connection.insertFeatureText(pd.DataFrame(data=featureText))