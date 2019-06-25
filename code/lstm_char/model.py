


class Tokenizer:
    
    def __init__(self, dict_wws):
        self.dict_wws = dict_wws
        
    def repair_word(self, word):
        try:
            
        for word_ws in self.dict_wws:
            
        
    def __iter__(self, batch_paragraph)
        
    
    

def tokenizer(text, alpha_only=True):  # create a tokenizer function
    tokens = [tok for tok in nltk.word_tokenize(text) if (not alpha_only or tok.isalpha())]
    if len(tokens) <= 1:
        tokens += ['xxx', 'xxx']
    return tokens