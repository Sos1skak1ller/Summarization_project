# tokenizer.py
import re
import math
from collections import Counter
from razdel import sentenize
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()

def tokenize_sentences(text):
    sentences = [sentence.text for sentence in sentenize(text)]
    return sentences

def lemmatize(word):
    return morph.parse(word)[0].normal_form

def calculate_sentence_importance(sentence, word_idf):
    words = re.findall(r'\b\w+\b', sentence.lower())
    words = [lemmatize(word) for word in words]
    sentence_length = len(words)
    if sentence_length == 0:
        return 0
    sentence_importance = sum(word_idf.get(word, 0) for word in words) / sentence_length
    return sentence_importance

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    words = [lemmatize(word) for word in words]
    word_frequencies = Counter(words)
    total_documents = len(tokenize_sentences(text))
    word_idf = {word: math.log10(total_documents / (1 + word_frequencies[word])) for word in word_frequencies}
    return word_idf

def load_word_weights(json_path):
    import json
    with open(json_path, 'r', encoding='utf-8') as file:
        word_weights = json.load(file)
    return word_weights
