import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer

LANGUAGE = "russian"

def summarize_text(text_path, num_sentences, summarizer_type):
    try:
        
        parser = PlaintextParser.from_file(text_path, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = None

        summarizer_type = summarizer_type.lower()  # Ensure lower case comparison

        if summarizer_type == "lsa":
            summarizer = LsaSummarizer(stemmer)
        elif summarizer_type == "luhn":
            summarizer = LuhnSummarizer()
        elif summarizer_type == "lexrank":
            summarizer = LexRankSummarizer()

        
        else:
            raise ValueError("Unsupported summarizer type: {}".format(summarizer_type))
    except Exception as e:
        print("Error summarizing text:", e)
        return None

