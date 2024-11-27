from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

class Summarizer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.stemmer = Stemmer('english')
        self.summarizer = LsaSummarizer(self.stemmer)
        self.summarizer.stop_words = get_stop_words('english')

    def summarize(self, text: str, sentences_count: int = 5) -> str:
        """
        Summarize the given text using LSA (Latent Semantic Analysis).
        
        Args:
            text (str): Text to summarize
            sentences_count (int): Number of sentences in the summary
            
        Returns:
            str: Summarized text
        """
        parser = PlaintextParser.from_string(text, Tokenizer('english'))
        summary_sentences = self.summarizer(parser.document, sentences_count)
        return " ".join([str(sentence) for sentence in summary_sentences]) 