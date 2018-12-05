from globals import Token, Category, Gender, Number

class FreelingStructParser:
    
    def __init__(self, text_info):
        self.parseText(text_info)

    def parseText(self, text_info):
        sentences = text_info.find_all('sentence')
        self.nouns = {} # {lemma : Token}
        self.verbs = {} # {lemma : Token}
        self.word_series = {} # {verb : {lemma : nouns}}

        for s in sentences:
            tokens = s.find_all('token')
            for token_info in tokens:
                token = Token(token_info.attrs['form'], token_info.attrs['lemma'], s.attrs['id'], token_info.attrs['tag'])
                if token.category == Category.NOUN:
                    if token.lemma in self.nouns.keys():
                        self.nouns[token.lemma].incRepeat()
                    else:
                        self.nouns[token.lemma] = token
                if token.category == Category.VERB:
                    if token.lemma in self.verbs.keys():
                        self.verbs[token.lemma].incRepeat()
                    else:
                        self.verbs[token.lemma] = token
            
            for verb in self.verbs.values():
                for noun in self.nouns.values():
                    if (verb.sentenceId == noun.sentenceId and verb.gender == noun.gender and verb.number == noun.number):
                        if verb.lemma not in self.word_series.keys():
                            self.word_series[verb.lemma] = {}
                        if noun.lemma in self.word_series[verb.lemma].keys():
                            self.word_series[verb.lemma].append(noun)

        self.ratingVerb = {}
        self.ratingNoun = {}

        for val in self.nouns.values():
            self.ratingNoun[val.repeatCount] = val

        for val in self.verbs.values():
            self.ratingVerb[val.repeatCount] = val


    def getPopularNoun(self, verb_lemma, amount):
        localVerbs = self.word_series[verb_lemma]
        res = []
        for noun in self.ratingNoun.values().reverse():
            if noun.lemma in [word.lemma for word in localVerbs]:
                res.append(noun)
        if len(res) > amount:
            res = res[:amount]
        if len(res) == 0:
            return None
        return res

    
    def getPopularPhrases(self, amount):
        res = list()
        # for verb in list(self.ratingVerb.values()).reverse():
        for verb in list(reversed(list(self.ratingVerb.values()))):
            cur_nouns = self.getPopularNoun(verb.lemma, 1)
            if cur_nouns != None:
                for noun in cur_nouns:
                    res.append(noun.form + ' ' + verb.form)
        if len(res) > amount:
            res = res[:amount]
        if len(res) == 0:
            return None
        return res
