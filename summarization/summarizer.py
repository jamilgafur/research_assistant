# summarization/summarizer.py

from transformers import pipeline
from typing import List

class TextSummarizer:
    """
    A class for performing text summarization using Hugging Face's transformers library.
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the TextSummarizer class.

        Parameters:
        - model_name (str): The name of the pre-trained model to use for summarization.
                             Default is 'facebook/bart-large-cnn', a BART-based model for summarization.
        """
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize a given text using the pre-trained model.

        Parameters:
        - text (str): The input text to summarize.
        - max_length (int): Maximum length of the summary.
        - min_length (int): Minimum length of the summary.

        Returns:
        - str: The summarized version of the input text.
        """
        try:
            # Perform the summarization using the Hugging Face pipeline
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            # Extract the summary from the model's output
            return summary[0]['summary_text']
        except Exception as e:
            raise Exception(f"An error occurred during summarization: {str(e)}")

    def summarize_multiple(self, texts: List[str], max_length: int = 150, min_length: int = 50) -> List[str]:
        """
        Summarize multiple texts at once.

        Parameters:
        - texts (List[str]): A list of input texts to summarize.
        - max_length (int): Maximum length of each summary.
        - min_length (int): Minimum length of each summary.

        Returns:
        - List[str]: A list of summarized texts.
        """
        try:
            # Summarize each text in the list
            summaries = [self.summarize(text, max_length, min_length) for text in texts]
            return summaries
        except Exception as e:
            raise Exception(f"An error occurred during summarization: {str(e)}")
