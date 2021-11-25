#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

import re

class Feature:
  def __init__(self):
    self.words = ''
    self.sentences = ''

  def setSentenceToList(self, text):
    self.sentences = re.findall("[^\n]+", text, flags=re.M)

  def getSentenceToList(self):
    return self.sentences

  def setWordToList(self, text):
    self.words = re.findall("\w+", text, flags=re.M)

  def getWordToList(self):
    return self.words
