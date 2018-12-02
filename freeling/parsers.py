from globals import Category, Gender, Number, Token


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



