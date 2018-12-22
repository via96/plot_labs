from globals import Token, Category, Gender, Number, Case, Phrase

class FreelingStructParser:
    
    def __init__(self, text_info):
        self.nouns = {} # {sent_num : [noun]}
        self.verbs = {} # {sent_num : [verb]}
        self.phrases = {} # {noun_lemma : [sentence]}
        self.noun_rating = []
        self.parseText(text_info)

    
    def sortListByFreq(self, series):
        series.sort(key = lambda val: val.repeatCount)
        return list(reversed(series))


    def addNounToRating(self, noun: Token):
        for item in self.noun_rating:
            if item.lemma == noun.lemma:
                item.incRepeat()
                return
        self.noun_rating.append(noun)
            

    def getNoun(self, lemma, sentId):
        for noun in self.nouns[sentId]:
            if noun.lemma == lemma:
                return noun


    def getVerb(self, lemma, sentId):
        for verb in self.verbs[sentId]:
            if verb.lemma == lemma:
                return verb


    def parseText(self, text_info):
        sentences = text_info.find_all('sentence')

        for s in sentences:
            tokens = s.find_all('token')
            for token_info in tokens:
                token = Token(token_info.attrs['form'], token_info.attrs['lemma'], s.attrs['id'], token_info.attrs['tag'])
                if token.category == Category.NOUN:
                    if token.sentenceId not in self.nouns:
                        self.nouns[token.sentenceId] = []
                    self.nouns[token.sentenceId].append(token)
                    self.addNounToRating(token)

                if token.category == Category.VERB:
                    if token.sentenceId not in self.verbs:
                        self.verbs[token.sentenceId] = []
                    self.verbs[token.sentenceId].append(token)

        
        self.noun_rating = self.sortListByFreq(self.noun_rating)
        for val in self.noun_rating:
            print(val.lemma, " | ", val.repeatCount)
        

        for sent_num, noun_series in self.nouns.items():
            for noun in noun_series:
                if sent_num in self.verbs.keys():
                    for verb in self.verbs[sent_num]:
                        if verb.sentenceId == noun.sentenceId and noun.case == Case.NOMINATIVE and verb.gender == noun.gender and verb.number == noun.number:
                            phrase = Phrase(noun.lemma, verb.lemma, sent_num)
                            if noun.lemma not in self.phrases.keys():
                                self.phrases[noun.lemma] = []
                            if phrase not in self.phrases[noun.lemma]:
                                self.phrases[noun.lemma].append(phrase)
                            else:
                                for item in self.phrases[noun.lemma]:
                                    if item == phrase:
                                        item.incRepeat()
                                        break

        


    def getPopularPhrases(self, amount, showAll = False):
        res = []
        it = 0
        for i in range(len(self.noun_rating)):
            noun = self.noun_rating[i]
            if noun.lemma in self.phrases.keys():
                sortedPhrases = sorted(self.phrases[noun.lemma], key = lambda val: val.repeatCount)
                cur_phrase = sortedPhrases[-1]
                res.append(self.getNoun(cur_phrase.noun_lemma, cur_phrase.sentenceId).form + ' ' + self.getVerb(cur_phrase.verb_lemma, cur_phrase.sentenceId).form)
                it = it + 1
            if not showAll and it >= amount:
                return res
        return res
