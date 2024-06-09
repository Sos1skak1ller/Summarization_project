import re
import math
from collections import Counter
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import json
import os

# Загрузка стоп-слов и инициализация стеммера для русского языка
nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer("russian")
stop_words = set(stopwords.words("russian"))

def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    return sentences

def lemmatize(word):
    return stemmer.stem(word)

def calculate_sentence_importance(sentence, word_idf):
    words = word_tokenize(sentence.lower())
    words = [lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    sentence_length = len(words)
    if sentence_length == 0:
        return 0
    sentence_importance = sum(word_idf.get(word, 0) for word in words) / sentence_length
    return sentence_importance

def extract_keywords(text):
    words = word_tokenize(text.lower())
    words = [lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    word_frequencies = Counter(words)
    total_documents = len(tokenize_sentences(text))
    word_idf = {word: math.log10(total_documents / (1 + word_frequencies[word])) for word in word_frequencies}
    return word_idf

def save_word_weights(word_idf, json_path):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(word_idf, file, ensure_ascii=False, indent=4)

def load_word_weights(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        word_weights = json.load(file)
    return word_weights
