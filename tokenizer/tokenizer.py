import torch
import numpy as np
from tokenizer.vocabulary import make_and_save_dict_from_source

np.random.seed(0)
class Tokenizer:
    def __init__(self, saved_location, source=None, word_dict=None):
        self.EOS = 0
        self.UNK = 1
        if saved_location:
            print(f"Загружаю сохраненный словарь из {saved_location}")
            if source is not None:
                word_dict, max_len = make_and_save_dict_from_source(saved_location, source)
            else:
                raise ValueError("Необходимо предоставить ресурс для чтения")
        else:
            raise ValueError("Необходимо предоставить сохраненное местоположение для загрузки словаря")
        if word_dict is None:
            raise ValueError("Необходимо предоставить словарь для чтения.")

        self.VOCAB_SIZE = len(word_dict)
        self.MAX_LEN = max_len + 1
        self.word_dict = word_dict
        print("Создается обратный словарь")
        self.reverse_map = list(self.word_dict.items())
        self.use_cuda = torch.cuda.is_available()

    def convert_sentence_to_indices(self, sentence, return_as_tensor=True):
        sentence = self.__preprocess_sentence(sentence)
        indices = [
            self.word_dict.get(w)
            if self.word_dict.get(w, self.VOCAB_SIZE + 1) < self.VOCAB_SIZE
            else self.UNK
            for w in sentence.split()
        ][: self.MAX_LEN - 1]

        length = len(indices)
        indices += [self.EOS] * (self.MAX_LEN - len(indices))

        if return_as_tensor:
            indices = np.array(indices)
            indices = torch.tensor(indices)
            if self.use_cuda:
                indices = indices.cuda()

        return indices, length

    def convert_batch_sentences_to_indices(self, sentences):
        indices_batch = []
        lengths_batch = []
        for sentence in sentences:
            token_label, length = self.convert_sentence_to_indices(sentence, False)
            indices_batch.append(token_label)
            lengths_batch.append(length)
        indices_batch = np.array(indices_batch)
        indices_batch = torch.tensor(indices_batch)
        if self.use_cuda:
            indices_batch = indices_batch.cuda()

        return indices_batch, lengths_batch

    def convert_indices_to_sentence(self, indices, length=None):
        if length is not None:
            indices = indices[:length]
        def convert_index_to_word(idx):
            idx = idx.data
            if idx == 0:
                return "EOS"
            elif idx == 1:
                return "UNK"

            search_idx = idx - 2
            if search_idx >= len(self.reverse_map):
                return "NA"

            word, idx_ = self.reverse_map[search_idx]
            assert idx_ == idx

            return word
        words = [convert_index_to_word(idx) for idx in indices]

        return " ".join(words)

    def convert_batch_indices_to_sentences(self, batch_indices, lengths=None):
        sentences = []
        for i, indices in enumerate(batch_indices):
            if lengths is not None:
                length = lengths[i]
                sentence = self.convert_indices_to_sentence(indices, length)
            else:
                sentence = self.convert_indices_to_sentence(indices)
            sentences.append(sentence)

        return sentences

    def __preprocess_sentence(self, sentence):
        return sentence.replace(".", " .").replace(",", " ,").replace("'", " '")