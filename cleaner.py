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

class Cleaner:
  def __init__(self):
    self.cleanText = ''

  def removeIsolatedNumbers(self, text):
    return re.sub(r"^\d+[^\w-]", "", text, flags=re.MULTILINE)
  
  def removeSpaces(self, text):
    return re.sub(r"(^ +)|( +$)", "", text, flags=re.MULTILINE)

  def removeBlankLines(self, text):
    return re.sub(r"^(?:[\t ]*(?:\r?[\n\r]))+", "", text, flags=re.MULTILINE)

  def removeSpecialCaracteres(self, text):
    special = re.sub(r'[ç]', 'c', text)
    a = re.sub(r'[áâãà]', 'a', special)
    e = re.sub(r'[éêè]', 'e', a)
    i = re.sub(r'[íîì]', 'i', e)
    o = re.sub(r'[óôõò]', 'o', i)
    u = re.sub(r'[úûù]', 'u', o)
    return re.sub(r'[\(\)]', '', u)

  def setCleanText(self, cleanText):
    self.cleanText = cleanText

  def getCleanText(self):
    return self.cleanText
