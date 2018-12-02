from enum import Enum
from parsers import TagParser

class MegaEnum(Enum):
    @staticmethod
    def contains(val):
        return val in [item.value for item in MegaEnum]

class Category(MegaEnum):
    UNKNOWN = '0'
    NOUN = 'N'
    VERB = 'V'

class Gender(MegaEnum):
    UNKNOWN = '0'
    MASCULINE = 'M'
    FEMININE = 'F'
    NEUTER = 'N'
    COMMON = 'C'
    AMBIGUOUS = 'A'

class Number(MegaEnum):
    UNKNOWN = '0'
    SINGULAR = 'S'
    PLURAL = 'P'

    

class Token:
    
    def __init__(self, form, lemma, sentenceId, tag):
        self.sentenceId = sentenceId
        self.form = form
        self.lemma = lemma
        tp = TagParser(tag)
        self.category = tp.getCategory()
        self.number = tp.getNum()
        self.gender = tp.getGen()
        self.repeatCount = 0

    def incRepeat(self):
        self.repeatCount = self.repeatCount + 1

    def __eq__(self, other: Token):
        return self.lemma == other.lemma

    def __gt__(self, other: Token):
        return self.lemma > other.lemma

    def __lt__(self, other: Token):
        return self.lemma < other.lemma