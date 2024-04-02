
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
LANGUAGE = "russian"
SENTECES_COUNT = 1


print("1.LSA")
print("2.Lung")
print("3.LexRank")
print("Введите цифру от 1 до 3")

parser = PlaintextParser.from_file("input.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
a = int(input())
lsa_summarizer = LsaSummarizer(stemmer)
lsa_summarizer.stop_words = get_stop_words(LANGUAGE)
if (a == 1):
    for sentence in lsa_summarizer(parser.document, SENTECES_COUNT):
        print(sentence)


summarizer_luhn = LuhnSummarizer()
summary_1 =summarizer_luhn(parser.document,SENTECES_COUNT)
if (a == 2):
    for sentence in summary_1:
        print(sentence)


# Using LexRank
summarizer = LexRankSummarizer()
#Summarize the document with 2 sentences
lex_summary = summarizer(parser.document, SENTECES_COUNT)
if (a == 3):
    for sentence in lex_summary:
        print(sentence)

