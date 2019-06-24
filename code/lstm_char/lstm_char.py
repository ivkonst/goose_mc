




def tokenizer(text, alpha_only=True):  # create a tokenizer function
    tokens = [tok for tok in nltk.word_tokenize(text) if (not alpha_only or tok.isalpha())]
    if len(tokens) <= 1:
        tokens += ['xxx', 'xxx']
    return tokens