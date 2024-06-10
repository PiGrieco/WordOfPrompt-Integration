import os
import sys
from typing import Dict, List, Tuple, Union

from .models.openseamo import OpenSesameAPI
from .keywords_extraction import KeywordExtractors


class PromptAnalyzer:
    """
    A class to analyze prompts, extract keywords, and determine intent.
    """

    def __init__(self, config, keywords_extracted: bool = False):
        """
        Initializes the PromptAnalyzer with a zero-shot classification model
        and sets default thresholds and intent labels.
        """
        if config is None:
            raise ValueError("Please make sure to pass the Config API and Token.")
        self.Estimator_intent = OpenSesameAPI(config)
        self.Threshold: float = 0.95
        self.Keywords: List[str] = []
        self.keywords_extracted = keywords_extracted

    @staticmethod
    def extract_keywords(prompt: str) -> List[str]:
        """
        Extracts keywords from a given prompt using the specified method.

        Args:
            prompt (str): The input prompt from which to extract keywords.

        Returns:
            List[str]: A list of extracted keywords.
        """
        method = KeywordExtractors(prompt=prompt, method="rake")
        keywords = method.keywords
        return keywords

    def analyze_prompt(self, prompt: str) -> Union[Tuple[bool, List[str], float, str], Tuple[bool, float, str]]:
        """
        Analyzes the given prompt to determine intent and extract keywords.

        Args:
            prompt (str): The input prompt to analyze.

        Returns:
            Union[Tuple[bool, List[str], float, str], Tuple[bool, float, str]]:
                - If keywords_extracted is True: 
                    A tuple containing a boolean indicating if the intent matches the keywords and threshold,
                    a list of extracted keywords, the intent score, and the original prompt.
                - If keywords_extracted is False: 
                    A tuple containing a boolean indicating if the intent matches the threshold,
                    the intent score, and the original prompt.
        """
        response = self.Estimator_intent.query({"text": prompt})
        
        result = response[0]
        intent_score = result["score"]
        intent_label = result["label"]

        if self.keywords_extracted is True:
            self.Keywords = self.extract_keywords(prompt)
        else:
            self.Keywords = []
       

        if intent_score >= self.Threshold:
                return True, self.Keywords, intent_score, prompt
        else:
            return False, self.Keywords,intent_score, prompt

        
    
