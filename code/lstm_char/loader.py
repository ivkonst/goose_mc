import gzip
import jsonlines
from multiprocessing import Pool, Semaphore
import numpy as np
import re
from torch.utils.data import DataLoader
from zipfile import ZipFile

np.random.seed(42)


class BatchReader:

    @classmethod
    def get_file_iterator(cls, filename):
        if re.match(r'.*\.gz$', filename):
            fd = gzip.open(filename, 'rt', encoding='utf-8')
        elif re.match(r'.*\.zip$', filename):
            arch = ZipFile(filename)
            zipname = arch.namelist()[0]
            fd = map(lambda x: x.decode('utf-8'), arch.open(zipname))
        elif re.match(r'.*\.jsonl$', filename):
            fd = jsonlines.open(filename)
        else:
            fd = open(filename, 'r', encoding='utf-8')

        return fd

    @classmethod
    def read_lines(cls, fd):
        for line in fd:
            yield line

    def read_batches(self, semaphore=None):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()
        
        
class ParagraphReader(BatchReader):

    def __init__(self, filename, batch_size):
        self.batch_size = batch_size
        self.filename = filename
        self.file_len = None
        
    def make_paragraphs(self, list_phrase):
        n = len(list_phrase)

        i = 0
        while n - i > 6:
            len_paragraph = np.random.choice([2, 3, 4], p=[0.2, 0.4, 0.4])
            yield list_phrase[i:i+len_paragraph]
            i += len_paragraph

        rest = n - i
        if rest == 6:
            yield list_phrase[-rest:-3]
            yield list_phrase[-3:]
        elif rest == 5:
            yield list_phrase[-rest:-2]
            yield list_phrase[-2:]
        elif rest > 1:
            yield list_phrase[-rest:]

    def read_batches(self):
        fd = self.get_file_iterator(self.filename)
        reader = self.read_lines(fd)
        
        batch_paragraph = []
        for obj in reader:
            list_texts = obj['list_texts']
            
            for list_phrase in list_texts:
                for paragraph in self.make_paragraphs(list_phrase):
                    batch_paragraph.append(paragraph)
                    if len(batch_paragraph) >= self.batch_size:
                        yield batch_paragraph
                        batch_paragraph = []
        
        if len(batch_paragraph) > 0:
            yield batch_paragraph

    def __len__(self):
        if self.file_len is not None:
            return self.file_len
        else:
            fd = self.get_file_iterator(self.filename)
            num_phrase = sum(1 for obj in fd for list_phrase in obj['list_texts'] for phrase in list_phrase)
            self.file_len = int(num_phrase / 3.2 / self.batch_size)
            return self.file_len
        
        
class MentionsLoader(DataLoader):
    """
    This is custom test loader for mentions data
    """

    def __init__(
            self,
            batch_reader,
            tokenizer,
            parallel=0,
    ):
        """
        :param batch_reader: object to read raw batches from file
        :param tokenizer: function to split text into tokens
        :param parallel: number of data preparation processes
        """
        self.batch_reader = batch_reader
        self.tokenizer = tokenizer
        self.parallel = parallel

    @property
    def batch_size(self):
        return self.batch_reader.batch_size

    def construct_rels(self, batch_paragraph):
        raise NotImplementedError()

    def full_construct(self, batch):
        return self.construct_rels(*batch)

    @classmethod
    def to_torch(cls, batch: tuple):
        return tuple(map(torch.from_numpy, batch))

    def iter_batches(self):
        if self.parallel > 0:
            with Pool(self.parallel) as pool:
                semaphore = Semaphore(self.parallel * 10)
                for batch in pool.imap(self.full_construct, self.batch_reader.read_batches(semaphore)):
                    yield batch
                    semaphore.release()
        else:
            for batch in self.batch_reader.read_batches():
                yield self.full_construct(batch)

    def __iter__(self):
        """
        Iterate over data.
        :return:
        """
        yield from map(MentionsLoader.to_torch, self.iter_batches())

    def __len__(self):
        return len(self.batch_reader)
    
    
class EmbeddingMentionLoader(MentionsLoader):
    vectorizer = None

    def __init__(self, batch_reader, tokenizer, vectorizer, **kwargs):
        super().__init__(batch_reader, tokenizer, **kwargs)
        self.__class__.vectorizer = vectorizer

    def construct_rels(self, batch_paragraph):
        batch_a = self.__class__.vectorizer(pad_list(list(map(
            self.tokenizer,
            sentences_a
        )), pad=lambda: " ")).numpy()

        return batch_a, batch_b, target

    def target_prep(self, target):
        return target.astype(np.float32)