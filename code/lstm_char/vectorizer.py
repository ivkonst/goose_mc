import numpy as np
import re

alphabet = ['#', '$', '%', '&', ' ', '!', '"', '(', ')', '*', ',', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Ё', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']

alphabet_idx = dict(map(lambda x: (x[1], x[0]), enumerate(alphabet)))


def tokenizer_paragraph_char(paragraph):
    paragraph = '#' + '$'.join([re.sub('''[^!"()*,-.:;? 0-9A-Za-zА-Яа-яЁё]''','',phrase).strip() for phrase in paragraph]) + '%'
    return list(paragraph)


class VectorizerParagraphChar:
    def __init__(self, alphabet: dict):
        self.alphabet = alphabet
        self.length = len(alphabet)

    def label(self, char):
        return self.alphabet.get(char, -100)
    
    def vect(self, phrase):
        return np.array([self.label(char) for char in phrase])
        
    def forward(self, batch):
        return np.array([self.vect(phrase) for phrase in batch])
