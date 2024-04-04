import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.models.dom import ObjectDocumentModel
from sumy.summarizers.method import EdmundsonMethod

LANGUAGE = "russian"
SENTENCES_COUNT = 1

print("1. LSA")
print("2. Luhn")
print("3. LexRank")
print("4. Edmundson")

parser = PlaintextParser.from_file("input.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
a = int(input())

if a == 1:
    lsa_summarizer = LsaSummarizer(stemmer)
    lsa_summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in lsa_summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)

elif a == 2:
    summarizer_luhn = LuhnSummarizer()
    summary_1 = summarizer_luhn(parser.document, SENTENCES_COUNT)
    for sentence in summary_1:
        print(sentence)

elif a == 3:
    summarizer = LexRankSummarizer()
    lex_summary = summarizer(parser.document, SENTENCES_COUNT)
    for sentence in lex_summary:
        print(sentence)


