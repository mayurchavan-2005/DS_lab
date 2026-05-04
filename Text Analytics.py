"""
Text Analytics Practical

Operations covered:
a) Apply word-level tokenization using NLTK.
b) Perform POS tagging on the tokens.
c) Remove stop words from the tokens.
d) Apply stemming using PorterStemmer.
e) Apply lemmatization using WordNetLemmatizer.
f) Create a TF-IDF matrix using TfidfVectorizer for a sample corpus.
"""

from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


NLTK_DATA_DIR = Path(__file__).resolve().parent / "nltk_data"
nltk.data.path.append(str(NLTK_DATA_DIR))


def download_nltk_resource(resource_path, package_name):
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(package_name, download_dir=str(NLTK_DATA_DIR), quiet=True)


download_nltk_resource("tokenizers/punkt", "punkt")
download_nltk_resource("tokenizers/punkt_tab", "punkt_tab")
download_nltk_resource("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger")
download_nltk_resource(
    "taggers/averaged_perceptron_tagger_eng",
    "averaged_perceptron_tagger_eng",
)
download_nltk_resource("corpora/stopwords", "stopwords")
download_nltk_resource("corpora/wordnet", "wordnet")
download_nltk_resource("corpora/omw-1.4", "omw-1.4")


sample_text = (
    "Text analytics is an interesting field of data science. "
    "Students are learning tokenization, tagging, stemming, and lemmatization."
)

sample_corpus = [
    "Text analytics helps extract useful information from text.",
    "Natural language processing includes tokenization and tagging.",
    "TF-IDF gives importance to meaningful words in a document.",
]


# a) Word-level tokenization using NLTK.
tokens = word_tokenize(sample_text)

print("\na) Word-level Tokens:")
print(tokens)


# b) POS tagging on the tokens.
pos_tags = nltk.pos_tag(tokens)

print("\nb) POS Tags:")
print(pos_tags)


# c) Remove stop words from the tokens.
stop_words = set(stopwords.words("english"))
filtered_tokens = [
    token
    for token in tokens
    if token.lower() not in stop_words and token.isalpha()
]

print("\nc) Tokens after Stop Word Removal:")
print(filtered_tokens)


# d) Stemming using PorterStemmer.
porter_stemmer = PorterStemmer()
stemmed_words = [porter_stemmer.stem(token) for token in filtered_tokens]

print("\nd) Stemmed Words:")
print(stemmed_words)


# e) Lemmatization using WordNetLemmatizer.
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(token.lower()) for token in filtered_tokens]

print("\ne) Lemmatized Words:")
print(lemmatized_words)


# f) Create TF-IDF matrix using TfidfVectorizer.
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(sample_corpus)

tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=tfidf_vectorizer.get_feature_names_out(),
)

print("\nf) TF-IDF Matrix:")
print(tfidf_df)
