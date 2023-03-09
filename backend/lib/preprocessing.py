from nltk.stem import PorterStemmer
import re

with open("lib/datasets/stopwords_en.txt") as f:
    enStopWords = set(f.read().splitlines())

stemmer = PorterStemmer()

def preprocess_line_en(line: str) -> list[str]:
    tokens = line.lower()

    tokens = re.split("[^\w]", tokens)

    tokens = [stemmer.stem(x) for x in tokens if x and x not in enStopWords]

    return tokens
