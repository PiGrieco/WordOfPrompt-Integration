from yake import KeywordExtractor
from rake_nltk import Rake
from typing import List, Union
import nltk


# if nltk.data.find('tokenizers/punkt') is None:
#     print("Package punkt is not found. Downloading...")
#     nltk.download('punkt')
#     nltk.download('stopwords')
 
# else:
#      nltk.download('punkt')
#      nltk.download('stopwords')

class KeywordExtractors:
    """
    A wrapper for the Rake class that provides default configuration
    and could be extended with additional methods if needed.
    """

    def __init__(self, prompt: str, language: str = "en", max_keywords: int = 5, method: str = "rake"):
        """
        Initialize the RakeKeywordExtractor wrapper.
        """

        self.language: str = language
        self.max_keywords: int = max_keywords

        if method == "rake":
            self.extractor = Rake()
        elif method == "yake":
            self.extractor = KeywordExtractor(lan=self.language, n=3, dedupLim=0.9, top=self.max_keywords, features=None)
        else:
            raise ValueError("Method not supported")

        self.keywords: List[str] = self.extract_keywords(prompt)

    def extract_keywords(self, prompt: str) -> List[str]:
        """
        Extract keywords from the given prompt using the selected method.

        Args:
            prompt (str): The input prompt from which keywords will be extracted.

        Returns:
            List[str]: A list of extracted keywords.
        """

        if isinstance(self.extractor, Rake):
            self.extractor.extract_keywords_from_text(prompt)
            return self.extractor.get_ranked_phrases()[:self.max_keywords]
        else:
            return [keyword for keyword, score in self.extractor.extract_keywords(prompt)]


if __name__ == "__main__":
    prompt ="i am looking to buy a new Iphone averge between 1000$ and 600$"
    rake_extractor = KeywordExtractors(prompt=prompt, method="rake")
    rake_keywords = rake_extractor.keywords

    print("Keywords extracted using Rake method:", rake_keywords)

    yake_extractor = KeywordExtractors(prompt=prompt, method="yake")

    yake_keywords = yake_extractor.keywords
    print("Keywords extracted using YAKE method:", yake_keywords)
