"""
slide 7 ~ 10
no flanking sequence
"""
import csv
import random

import numpy as np
import yaml
from gensim.models import KeyedVectors, Word2Vec
from sklearn.manifold import TSNE
from torch import tensor
import matplotlib.pyplot as plt


class PreProcesser:
    def __init__(self, config_path="./config.yaml"):
        with open(config_path) as yml:
            self.config = yaml.load(yml, Loader=yaml.FullLoader)
        self.raw_path = self.config["ALL_SEQUENCES"]
        self.slide = int(self.config["SLIDE"])
        self.n_of_seq = int(self.config["NUM_OF_SEQ"])
        self.vector_size = int(self.config["VECTOR_SIZE"])
        self.window_size = int(self.config["WINDOW"])

        self.name = f"{self.slide}_{self.n_of_seq}_{self.vector_size}_{self.window_size}"

    def main(self):
        sequences = set()
        with open(self.raw_path) as raw_fh:
            col = list()
            for line in raw_fh:
                if line[0] == "#":
                    if line[1] == "#":
                        continue
                    col = line.strip().split("\t")
                    continue

                if random.random() > 0.2:
                    continue
                split_line = line.strip().split("\t")
                row = dict(zip(col, split_line))
                sequences.add(row["DNA"])

                if len(sequences) > self.n_of_seq:
                    break

        sentences = self.make_it_sentence(sequences)

        corpus = self.make_it_corpus(sentences)
        n_corpus = len(corpus)
        total_word = len(sentences) * (23 - self.slide + 1)
        print(f"total words in corpus: {n_corpus}")
        print(f"used words in all sentences: {total_word}")
        print(f"proportion: {n_corpus / total_word}")

        model = Word2Vec(
            sentences=sentences,
            vector_size=self.vector_size,
            window=self.window_size,
            min_count=4,
            workers=8,
            sg=1,
        )

        model.wv.save_word2vec_format(f"./grna_w2v_{self.name}")

        tsne_vector = list()
        for word in corpus:
            if word in model.wv:
                tsne_vector.append(model.wv[word])

        tsne_vector = np.array(tsne_vector)

        X_embedded = TSNE(n_components=2).fit_transform(tsne_vector)

        plt.scatter(X_embedded[:, 0], X_embedded[:, 1])
        plt.savefig(f"tsne_{self.name}")

        # model_result = model.wv.most_similar(sentences[0][0])
        # print(sentences[0][0], model_result)
        # print(model.wv["GAAAA"])

    def make_it_corpus(self, sentences: list) -> set:
        res = set()

        for sentence in sentences:
            for word in sentence:
                res.add(word)

        return res

    def make_it_sentence(self, sequences: set) -> list:
        res = list()
        all_letter = set()
        for sequence in sequences:
            sentence = list()
            for char in sequence:
                all_letter.add(char)
            if "N" in sequence:
                continue
            for index in range(0, len(sequence) - self.slide + 1):
                sentence.append(sequence[index : index + self.slide])
            res.append(sentence)

        print(all_letter)
        return res


if __name__ == "__main__":
    OBJ = PreProcesser()
    OBJ.main()
