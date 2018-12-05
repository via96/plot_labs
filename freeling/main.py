from lxml import etree
from pyfreeling import Analyzer
from os import path
from token_parser import FreelingStructParser
import subprocess
import bs4



class TextAnalyzer:

    def __init__(self, pathToTextFile, language='ru'):
        self._configFolder = '/usr/share/freeling/config/'
        self._pathToTextFile = pathToTextFile
        self._language = language
        if not path.exists(self._pathToTextFile):
            print('Wrong path to text file.', self._pathToTextFile)
            raise FileNotFoundError

    
    def start(self):
        self.xml = self.parseText()
        doc = bs4.BeautifulSoup(self.xml, 'html.parser')
        parser = FreelingStructParser(doc)
        res = parser.getPopularPhrases(5)
        if res != None:
            for val in res:
                print(val)


    def parseText(self):
        p = subprocess.Popen(
            'analyze -f ' + path.join(self._configFolder, self._language + '.cfg') + ' --output xml < ' + self._pathToTextFile,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        r = p.communicate()
        return r[0]



if __name__ == '__main__':
    a = TextAnalyzer('text')
    a.start()