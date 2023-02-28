import random


class Ngram:
    def __init__(self):
        pass

    def perplexity(self, texts):
        raise NotImplementedError

    def generate(self, begin_texts, n):
        raise NotImplementedError

    def get_grams(self):
        raise NotImplementedError


class Unigram(Ngram):
    def __init__(self, texts):
        super().__init__()
        self.corpus = texts
        self.process_corpus()

    def process_corpus(self):
        self.count_dict = dict()
        self.count = 0
        for text in self.corpus:
            for c in text:
                if c not in self.count_dict:
                    self.count_dict[c] = 1
                else:
                    self.count_dict[c] += 1
                self.count += 1
        self.tokens = list(self.count_dict.keys())
        self.pls = []
        for c in self.tokens:
            self.pls.append(self.count_dict[c] / self.count)

    def perplexity(self, texts) -> float:
        p = 1
        n = 0
        for text in texts:
            for c in text:
                p *= self.count_dict[c] / self.count
                n += 1
        res = pow(p, -1 / n)
        print("unigram perplexity:", res)
        return res

    def generate(self, begin_text, n):
        res = ''.join(random.choices(self.tokens, self.pls, k=n))
        print("generated text:", res)
        return res

    def get_grams(self):
        print("unigram word counts:")
        for c in self.count_dict:
            print(f'{c}:{self.count_dict[c]}')
        return self.count_dict


class Bigramword:
    def __init__(self, word):
        self.word = word
        self.count = 0
        self.count_dict = dict()

    def add_word(self, word):
        if word not in self.count_dict:
            self.count_dict[word] = 1
        else:
            self.count_dict[word] += 1
        self.count += 1

    def compute(self):
        self.tokens = list(self.count_dict.keys())
        self.pls = []
        self.token2id = dict()
        for i, token in enumerate(self.tokens):
            self.token2id[token] = i
        for c in self.tokens:
            self.pls.append(self.count_dict[c] / self.count)

    def generate(self):
        return random.choices(self.tokens, self.pls)[0]

    def getp(self, word):
        return self.pls[self.token2id[word]]


class Bigram(Ngram):

    def __init__(self, texts):
        super().__init__()
        self.corpus = texts
        self.process_corpus()

    def perplexity(self, texts):
        p = 1
        n = 0
        for text in texts:
            text = 'b' + text + 'e'
            for i, c in enumerate(text[:-1]):
                p *= self.count_dict[c].getp(text[i + 1])
                n += 1
        res = pow(p, -1 / n)
        print("bigram perplexity:", res)
        return res

    def generate(self, begin_text, n):
        if begin_text is not None:
            res = begin_text
        else:
            res = 'b'
        for i in range(n):
            gen_text = self.count_dict[res[i]].generate()
            res += gen_text
            if gen_text == 'e':
                break
        if res[-1] == 'e':
            res = res[:-1]
        if res[0] == 'b':
            res = res[1:]
        print("bigram generated text:", res)
        return res

    def get_grams(self):
        print("bigram word counts:")
        for c in self.count_dict:
            for c1 in self.count_dict[c].count_dict:
                print(f'{c} {c1}:{self.count_dict[c].count_dict[c1]}')
        return self.count_dict

    def process_corpus(self):
        self.count_dict = dict()
        for text in self.corpus:
            text = 'b' + text + 'e'
            m = len(text)
            for i, c in enumerate(text):
                if c not in self.count_dict and i < m - 1:
                    self.count_dict[c] = Bigramword(c)
                    self.count_dict[c].add_word(text[i + 1])
                elif i < m - 1:
                    self.count_dict[c].add_word(text[i + 1])
        for c in self.count_dict:
            self.count_dict[c].compute()


if __name__ == '__main__':
    unigram = Unigram(['我爱自然语言处理', '我爱北航'])
    unigram.generate(None, 10)
    unigram.get_grams()
    unigram.perplexity(['我爱北航'])

    bigram = Bigram(['我爱自然语言处理', '我爱北航'])
    bigram.generate(None, 10)
    bigram.get_grams()
    bigram.perplexity(['我爱北航'])
