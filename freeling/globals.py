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

class Number(Enum):
    UNKNOWN = '0'
    SINGULAR = 'S'
    PLURAL = 'P'

    @staticmethod
    def contains(val):
        return val in [item.value for item in Number]


class Case(Enum):
    UNKNOWN = '0'
    NOMINATIVE = 'N'

    @staticmethod
    def contains(val):
        return val in [item.value for item in Case]

class TagParser:
    
    def __init__(self, tag_info):
        self.tag_info = tag_info

    def getCategory(self):
        if Category.contains(self.tag_info[0]) and len(self.tag_info) > 0:
            return Category(self.tag_info[0])
        return Category.UNKNOWN

    def getCase(self):
        # q1 = self.getCategory == Category.NOUN
        # try:
        #     q2 = Case.contains(self.tag_info[2])
        # except:
        #     pass
        # q3 = len(self.tag_info) >= 2
        try:
            if self.getCategory() == Category.NOUN and len(self.tag_info) >= 2 and Case.contains(self.tag_info[2]):
                return Case(self.tag_info[2])
        except:
            pass
        return Case.UNKNOWN

    def getGen(self):
        pos = -1
        if self.getCategory() == Category.UNKNOWN or len(self.tag_info) < 5:
            return Gender.UNKNOWN
        if self.getCategory() == Category.NOUN:
            pos = 4
        if self.getCategory() == Category.VERB:
            pos = 3
        if Gender.contains(self.tag_info[pos]):
            return Gender(self.tag_info[pos])
        return Gender.UNKNOWN

    def getNum(self):
        pos = -1
        if self.getCategory() == Category.UNKNOWN or len(self.tag_info) < 4:
            return Number.UNKNOWN
        if self.getCategory() == Category.NOUN:
            pos = 3
        if self.getCategory() == Category.VERB:
            pos = 2
        if Number.contains(self.tag_info[pos]):
            return Number(self.tag_info[pos])
        return Number.UNKNOWN
    

class Token:
    
    def __init__(self, form: str, lemma: str, sentenceId: int, tag: str):
        self.sentenceId = sentenceId
        self.form = form.lower()
        self.lemma = lemma.lower()
        tp = TagParser(tag)
        self.tag = tag
        self.case = tp.getCase()
        self.category = tp.getCategory()
        self.number = tp.getNum()
        self.gender = tp.getGen()
        self.repeatCount = 1

    def incRepeat(self):
        self.repeatCount = self.repeatCount + 1

    def __eq__(self, other):
        return self.lemma == other.lemma

    def __gt__(self, other):
        return self.lemma > other.lemma

    def __lt__(self, other):
        return self.lemma < other.lemma


class Phrase:
    
    def __init__(self, noun_lemma, verb_lemma, sentenceId):
        self.noun_lemma = noun_lemma
        self.verb_lemma = verb_lemma
        self.sentenceId = sentenceId
        self.repeatCount = 1

    
    def incRepeat(self):
        self.repeatCount = self.repeatCount + 1

    def __eq__(self, other):
        return self.noun_lemma == other.noun_lemma and \
            self.verb_lemma == other.verb_lemma

    def __gt__(self, other):
        return self.noun_lemma > other.noun_lemma and \
            self.verb_lemma > other.verb_lemma

    def __lt__(self, other):
        return self.noun_lemma < other.noun_lemma and \
            self.verb_lemma < other.verb_lemma


if __name__ == '__main__':
    if Case.contains('N'):
        print('y')
    else:
        print('n')