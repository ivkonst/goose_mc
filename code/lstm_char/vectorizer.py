import torch.nn as nn


class EmbeddingVectorizer(nn.Module):
    def __init__(self, embedding):
        super(EmbeddingVectorizer, self).__init__()
        self.embedding = embedding

    def forward(self, batch):
        batch_size = len(batch)
        sent_len = len(batch[0])
        flatten = list(itertools.chain(*batch))

        return self.embedding(flatten).view(batch_size, sent_len, -1)
    
    
class CharVectorizer:
    def __init__(self, model_path):
        self.model = gensim.models.FastText.load(model_path)

    def __call__(self, words):
        mtx_sent = []
        for token in words:
            try:
                mtx_sent.append(self.model.wv.get_vector(token))
            except KeyError:
                seed = zlib.crc32(token.encode())
                state = np.random.get_state()
                np.random.seed(seed)
                vect = np.random.normal(size=self.model.wv.vector_size)
                np.random.set_state(state)
                mtx_sent.append(vect)

        mtx_sent = np.stack(mtx_sent)
        return torch.from_numpy(mtx_sent).float()


class GensimVectorizer:
    def __init__(self, model_path):
        self.model = gensim.models.FastText.load(model_path)

    def __call__(self, words):
        mtx_sent = []
        for token in words:
            try:
                mtx_sent.append(self.model.wv.get_vector(token))
            except KeyError:
                seed = zlib.crc32(token.encode())
                state = np.random.get_state()
                np.random.seed(seed)
                vect = np.random.normal(size=self.model.wv.vector_size)
                np.random.set_state(state)
                mtx_sent.append(vect)

        mtx_sent = np.stack(mtx_sent)
        return torch.from_numpy(mtx_sent).float()
