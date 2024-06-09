# sumy_algorithm.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from tokenizer import tokenize_sentences, calculate_sentence_importance, extract_keywords

LANGUAGE = "russian"

def luhn_summarizer(text, num_sentences):
    sentences = tokenize_sentences(text)
    word_idf = extract_keywords(text)
    
    sentence_scores = [(sentence, calculate_sentence_importance(sentence, word_idf)) for sentence in sentences]
    sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    
    top_sentences = [sentence for sentence, score in sentence_scores[:num_sentences]]
    return top_sentences

def summarize_text(text, num_sentences, summarizer_type):
    try:
        if summarizer_type.lower() == "lsa":
            parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)
            summary = summarizer(parser.document, num_sentences)
            return summary
        elif summarizer_type.lower() == "luhn":
            return luhn_summarizer(text, num_sentences)
        elif summarizer_type.lower() == "lexrank":
            parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
            summarizer = LexRankSummarizer()
            summarizer.stop_words = get_stop_words(LANGUAGE)
            summary = summarizer(parser.document, num_sentences)
            return summary
        else:
            raise ValueError("Unsupported summarizer type: {}".format(summarizer_type))
    except Exception as e:
        print("Error summarizing text:", e)
        return None
