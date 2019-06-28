import nltk
import re


class TokenizerParagraphCharWWS:
    
    def __init__(self, dict_wws):
        self.dict_wws = dict_wws
        
    def correct_word(self, word_ws, word_wos):
        star_idx = word_ws.index('*')
        word_ws[star_idx] = word_wos[star_idx]
        return word_ws 
    
    def repair_word(self, word_ws):
        word_wos = self.dict_wws.get(word_ws.lower(), '')
        if (word_wos == '') or (len(word_ws) != len(word_wos)):
            return word_ws
        else:
            return self.correct_word(word_ws, word_wos)
        
    def __iter__(self, paragraph):
        for phrase in paragraph:
            phrase = re.sub('''[^!"()*,-.:;? 0-9A-Za-zА-Яа-яЁё]''','',phrase)
            for tok in nltk.word_tokenize(phrase):
                if ('*' in tok) and ()
        
    
    

def tokenizer(text, alpha_only=True):  # create a tokenizer function
    tokens = [tok for tok in nltk.word_tokenize(text) if (not alpha_only or tok.isalpha())]
    if len(tokens) <= 1:
        tokens += ['xxx', 'xxx']
    return tokens