from globals import Token, Category, Gender, Number, Case, Phrase

class FreelingStructParser:
    
    def __init__(self, text_info):
        self.parseText(text_info)

    
    def sortListByFreq(self, series):
        series.sort(key = lambda val: val.repeatCount)
        return list(reversed(series))


    def addNounToRating(self, noun: Token):
        for item in self.noun_rating:
            if item.lemma == noun.lemma:
                noun.incRepeat()
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
        self.nouns = {} # {sent_num : [noun]}
        self.verbs = {} # {sent_num : [verb]}
        self.phrases = {} # {noun_lemma : [sentence]}
        self.noun_rating = []

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








# class FreelingStructParser_old:


#     def parseText_old(self, text_info):
#         sentences = text_info.find_all('sentence')
#         self.nouns = {} # {lemma : Token}
#         self.verbs = {} # {lemma : Token}
#         self.word_series = {} # {verb : {lemma : nouns}}
#         self.phraseByNouns = {} # {noun : { cnt : #, verbs : { verb : freq }}}

#         for s in sentences:
#             tokens = s.find_all('token')
#             for token_info in tokens:
#                 token = Token(token_info.attrs['form'], token_info.attrs['lemma'], s.attrs['id'], token_info.attrs['tag'])
#                 if token.category == Category.NOUN:
#                     if token.lemma in self.nouns.keys():
#                         self.nouns[token.lemma].incRepeat()
#                     else:
#                         self.nouns[token.lemma] = token
#                 if token.category == Category.VERB:
#                     if token.lemma in self.verbs.keys():
#                         self.verbs[token.lemma].incRepeat()
#                     else:
#                         self.verbs[token.lemma] = token
            
#             for verb in self.verbs.values():
#                 for noun in self.nouns.values():
#                     if verb.sentenceId == noun.sentenceId and verb.gender == noun.gender and verb.number == noun.number:
#                     # if noun.gender == Gender.NEUTER and (noun.gender == verb.gender or noun.gender == Gender.UNKNOWN) and (noun.number == verb.number or noun.number == Number.UNKNOWN):
#                         if verb.lemma not in self.word_series.keys():
#                             self.word_series[verb.lemma] = {}
#                         if noun.lemma not in self.word_series[verb.lemma].keys():
#                             self.word_series[verb.lemma].update({noun.lemma : noun})

#             for verb in self.word_series:
#                 for noun in self.word_series[verb].values():
#                     if noun.lemma not in self.phraseByNouns:
#                         self.phraseByNouns.update({noun.lemma : {'count' : 1, 'verbs' : {verb.lemma : 1}}})
#                     else:
#                         if verb.lemma not in self.phraseByNouns[noun.lemma]['verbs']:
#                             self.word_series[noun]




#             localSentences = {} # {verb_lemma : { 'verb' : verb_form, 'noun' : [noun_form]}}
#             _dictKeyStruct = {} # {noun_lemma : {'count' : #, 'verbs' : {verb_lemma : #}}}

#             for key in localSentences:
#                 print(",".join(localSentences[key]['noun']) + " " + localSentences[key]['verb'])
#                 for noun in localSentences[key]['noun']:
#                     if noun.lower() not in self._dictKeyStruct:
#                         self._dictKeyStruct.update({noun.lower() : {'count' : 1, 'verbs': {localSentences[key]['verb'] : 1}}})
#                     else:
#                         if localSentences[key]['verb'] not in self._dictKeyStruct[noun.lower()]['verbs']:
#                             self._dictKeyStruct[noun.lower()]['verbs'].update({localSentences[key]['verb'] : 1})
#                         else:
#                             self._dictKeyStruct[noun.lower()]['verbs'][localSentences[key]['verb']] += 1
#                         self._dictKeyStruct[noun.lower()]['count'] += 1

#         self.ratingVerb = []
#         self.ratingNoun = []

#         for val in self.nouns.values():
#             self.ratingNoun.append(val)
#         self.sortListByFreq(self.ratingNoun)

#         for val in self.verbs.values():
#             self.ratingVerb.append(val)
#         self.sortListByFreq(self.ratingVerb)


#     def getPopularNoun(self, verb_lemma, amount):
#         if verb_lemma not in self.word_series.keys():
#             return None
#         localNouns = self.word_series[verb_lemma].values()
#         res = []
#         for noun in self.ratingNoun:
#             if noun.lemma in [word.lemma for word in localNouns]:
#                 res.append(noun)
#         if len(res) > amount:
#             res = res[:amount]
#         if len(res) == 0:
#             return None
#         return res

    
#     def getPopularPhrases(self, amount):
#         res = list()
#         # for verb in list(self.ratingVerb.values()).reverse():
#         for verb in self.ratingVerb:
#             cur_nouns = self.getPopularNoun(verb.lemma, 10)
#             if cur_nouns != None:
#                 for noun in cur_nouns:
#                     res.append(noun.form + ' ' + verb.form + " | " + noun.tag + " " + verb.tag)
#                     break
#         if len(res) > amount:
#             res = res[:amount]
#         if len(res) == 0:
#             return None
#         return res
