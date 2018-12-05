from enum import Enum

class MegaEnum(Enum):
    @staticmethod
    def contains(val):
        return val in [item.value for item in MegaEnum]

    @staticmethod
    def contains_test(val):
        for item in MegaEnum:
            if val == item.value:
                return True
        return False

class Category(Enum):
    UNKNOWN = '0'
    NOUN = 'N'
    VERB = 'V'

    @staticmethod
    def contains(val):
        return val in [item.value for item in Category]

class Gender(Enum):
    UNKNOWN = '0'
    MASCULINE = 'M'
    FEMININE = 'F'
    NEUTER = 'N'
    COMMON = 'C'
    AMBIGUOUS = 'A'

    @staticmethod
    def contains(val):
        return val in [item.value for item in Gender]

class Number(MegaEnum):
    UNKNOWN = '0'
    SINGULAR = 'S'
    PLURAL = 'P'

    @staticmethod
    def contains(val):
        return val in [item.value for item in Number]


class TagParser:
    
    def __init__(self, tag_info):
        self.tag_info = tag_info

    def getCategory(self):
        if Category.contains(self.tag_info[0]) and len(self.tag_info) > 0:
            return Category(self.tag_info[0])
        return Category.UNKNOWN

    def getGen(self):
        pos = -1
        if self.getCategory() == Category.UNKNOWN or len(self.tag_info) < 5:
            return Gender.UNKNOWN
        if self.getCategory() == Category.NOUN:
            pos = 4
        if self.getCategory() == Category.VERB:
            pos = 3
        if Category.contains(self.tag_info[pos]):
            return Gender.contains(self.tag_info[pos])
        return Gender.UNKNOWN

    def getNum(self):
        pos = -1
        if self.getCategory() == Category.UNKNOWN or len(self.tag_info) < 4:
            return Gender.UNKNOWN
        if self.getCategory() == Category.NOUN:
            pos = 3
        if self.getCategory() == Category.VERB:
            pos = 2
        if Number.contains(self.tag_info[pos]):
            return Number(self.tag_info[pos])
    

class Token:
    
    def __init__(self, form: str, lemma: str, sentenceId: int, tag: str):
        self.sentenceId = sentenceId
        self.form = form.lower()
        self.lemma = lemma.lower()
        tp = TagParser(tag)
        self.category = tp.getCategory()
        self.number = tp.getNum()
        self.gender = tp.getGen()
        self.repeatCount = 0

    def incRepeat(self):
        self.repeatCount = self.repeatCount + 1

    def __eq__(self, other):
        return self.lemma == other.lemma

    def __gt__(self, other):
        return self.lemma > other.lemma

    def __lt__(self, other):
        return self.lemma < other.lemma


if __name__ == '__main__':
    if Category.contains('N'):
        print('y')
    else:
        print('n')