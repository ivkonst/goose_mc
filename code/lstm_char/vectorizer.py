import numpy as np

alphabet = ['#', '$', '%', ' ', '!', '"', '(', ')', '*', ',', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Ё', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']

alphabet_idx = dict(map(lambda x: (x[1], x[0]), enumerate(alphabet)))


class VectorizerParagraphChar:
    def __init__(self, alphabet: dict):
        self.alphabet = alphabet
        self.length = len(alphabet)

    @classmethod
    def make_diff_alphabet(cls, alphabet):
        charset = ['', '--'] + list(alphabet.keys()) + ['+' + x for x in alphabet.keys()]
        return dict(map(lambda x: (x[1], x[0]), enumerate(charset)))

    def one_hot(self, char):
        vector = np.zeros(self.length, dtype=np.float32)
        char_idx = self.alphabet.get(char)
        if char_idx is not None:
            vector[char_idx] = 1.0
        return vector

    def label(self, char):
        return self.alphabet.get(char, -100)

    def vect(self, string: str, length=None, foo=None):
        if foo is None:
            foo = self.one_hot

        diff = (length or len(words)) - len(words)
        if isinstance(words, list):
            new_words = words + ['%'] * diff
        else:
            new_words = words + '%' * diff
        return np.stack([foo(x) for x in new_words])

    def vect_batch(self, batch):
        
        
        
        if foo is None:
            foo = self.one_hot
        length = len(batch[0])
        res = np.stack([self.vect_words(x, length, foo=foo) for x in batch])
        lengths = list(map(len, batch))
        return res, lengths
