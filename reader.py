#!/usr/bin/env python
__author__     = "Mateus Ferreira"
__copyright__  = "Copyright 2020, The FAST-PROJ Group"
__credits__    = ["Mateus Ferreira"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "FAST-PROJ"
__email__      = "#"
__status__     = "Development"

from pdfminer.high_level import extract_text # pip install pdfminer.six
import os
import re

class Reader:
  def __init__(self):
    self.sourcePath = Reader.setSourceDataPath()
    self.text = ''
    self.id = None

  def setSourceDataPath():
    # The last item '""' create a separator "/" for linux or "\" for windows
    return os.path.join(os.getcwd(), "etl", "source", "")

  def setTextFromPdf(self, fileName):
    try:
      self.text = extract_text(f"{self.sourcePath}{fileName}.pdf")
    except Exception as e:
      print(str(e))

  def getTextFromPdf(self):
      return self.text

  def getLinks(self, text):
    return re.findall("www\.\w+\.\w+[^ \n]+", text, flags=re.M)

  def setFileId(self, id):
    self.id = id

  def getFileId(self):
    return self.id
