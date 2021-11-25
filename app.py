#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from reader import Reader
from cleaner import Cleaner
from feature import Feature
from mysql import dbConnection
import pandas as pd

# Inicia a classe de conexão com o banco
connection = dbConnection()
# Inicia a classe de leitura do arquivo
reader = Reader()
# Inicia a classe de limpeza
cleaner = Cleaner()
# Inicia a classe de features
feature = Feature()

def rawText(id):

  # Preenche o parametro de fileId
  reader.setFileId(id)

  # Coleta as informações do banco de dados a partir do id do arquivo
  file = connection.getFile(reader.getFileId())

  # Leitura do arquivo da pasta source
  reader.setTextFromPdf(f"{file['name']}")

  #Cria um dicionario com as informações do arquivo
  rawText = {
              "id": [reader.getFileId()], 
              "text":[reader.getTextFromPdf()]
  }

  #Efetua o insert na camada bronze
  connection.insertRawText(pd.DataFrame(data=rawText))

def refinedText():
  
  numbersClean = cleaner.removeIsolatedNumbers(reader.getTextFromPdf())
  spaceClean = cleaner.removeSpaces(numbersClean)
  blankClean = cleaner.removeBlankLines(spaceClean)
  cleanText = cleaner.removeSpecialCaracteres(blankClean)
  cleaner.setCleanText(cleanText)

  #Cria um dicionario com as informações do arquivo
  refinedText = {
              "id": [reader.getFileId()],
              "text":[cleaner.getCleanText()]
  }

  #Efetua o insert na camada silver
  connection.insertRefinedText(pd.DataFrame(data=refinedText))

def featureText():

  feature.setSentenceToList(cleaner.getCleanText())
  feature.setWordToList(cleaner.getCleanText())

  #Cria um dicionario com as informações do arquivo
  featureText = {
              "id": [reader.getFileId()],
              "word":[str(feature.getWordToList())],
              "sentence":[str(feature.getSentenceToList())]
  }

  #Efetua o insert na camada gold
  connection.insertFeatureText(pd.DataFrame(data=featureText))

rawText(1)
refinedText()
featureText()
