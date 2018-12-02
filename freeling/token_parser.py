from globals import Token, Category, Gender, Number


class FreelingStructParser:
    
    @staticmethod
    def parseText(text_info):
        sentences = text_info.find_all('sentence')
        nouns = {} # {lemma : Token}
        verbs = {} # {lemma : Token}
        word_series = {} # {verb : {lemma : nouns}}

        for s in sentences:
            tokens = s.find_all('token')
            for token_info in tokens:
                token = Token(token_info.attrs['form'], token_info.attrs['lemma'], s.attrs['id'], token_info.attrs['tag'])
                if token.category == Category.NOUN:
                    if token.lemma in nouns.keys():
                        nouns[token.lemma].incRepeat()
                    else:
                        nouns[token.lemma] = token
                if token.category == Category.VERB:
                    if token.lemma in verbs.keys():
                        verbs[token.lemma].incRepeat()
                    else:
                        verbs[token.lemma] = token
            
            for verb in verbs.values():
                for noun in nouns.values():
                    if (verb.sentenceId == noun.sentenceId and verb.gender == noun.gender and verb.number == noun.number):
                        if verb not in word_series.keys():
                            word_series[verb] = {}
                        if noun.lemma in word_series[verb].keys():
                            word_series[verb].append(noun)

        return word_series
