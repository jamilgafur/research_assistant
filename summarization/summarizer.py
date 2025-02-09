from transformers import pipeline
from typing import List, Optional

class TextSummarizer:
    """
    A class for performing text summarization using Hugging Face's transformers library.
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the TextSummarizer class.

        Parameters:
        - model_name (str): The name of the pre-trained model to use for summarization.
                             Default is 'facebook/bart-large-cnn'.
        """
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text: str, max_length: Optional[int] = 150, min_length: Optional[int] = 50) -> str:
        """
        Summarize a given text using the pre-trained model.

        Parameters:
        - text (str): The input text to summarize.
        - max_length (int): Maximum length of the summary (default: 150).
        - min_length (int): Minimum length of the summary (default: 50).

        Returns:
        - str: The summarized version of the input text.
        """
        try:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return summary[0]['summary_text']
        except ValueError as e:
            raise ValueError(f"Summarization error: {str(e)}")

    def summarize_multiple(self, texts: List[str], max_length: Optional[int] = 150, min_length: Optional[int] = 50) -> List[str]:
        """
        Summarize multiple texts at once.

        Parameters:
        - texts (List[str]): A list of input texts to summarize.
        - max_length (int): Maximum length of each summary (default: 150).
        - min_length (int): Minimum length of each summary (default: 50).

        Returns:
        - List[str]: A list of summarized texts.
        """
        from concurrent.futures import ThreadPoolExecutor

        def summarize_text(text: str):
            return self.summarize(text, max_length, min_length)

        try:
            with ThreadPoolExecutor() as executor:
                summaries = list(executor.map(summarize_text, texts))
            return summaries
        except Exception as e:
            raise Exception(f"An error occurred while summarizing multiple texts: {str(e)}")
