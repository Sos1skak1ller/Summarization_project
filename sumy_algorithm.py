from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer

LANGUAGE = "russian"

def summarize_text(text, num_sentences, summarizer_type):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = None

        if summarizer_type.lower() == "lsa":
            summarizer = LsaSummarizer(stemmer)
        elif summarizer_type.lower() == "luhn":
            summarizer = LuhnSummarizer()
        elif summarizer_type.lower() == "lexrank":
            summarizer = LexRankSummarizer()
        else:
            raise ValueError("Unsupported summarizer type: {}".format(summarizer_type))

        summarizer.stop_words = get_stop_words(LANGUAGE)

        return summarizer(parser.document, num_sentences)
    except Exception as e:
        print("Error summarizing text:", e)
        return None
