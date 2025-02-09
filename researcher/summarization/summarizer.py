from transformers import pipeline
from typing import List
from tqdm import tqdm  # Import tqdm for progress bar

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

    def summarize(self, text: str, chunk_size: int = 1000) -> str:
        """
        Summarize a given text using the pre-trained model.
        
        If the text is too long, it will be split into manageable pieces and summarized separately,
        and the summaries will be combined into one.

        Parameters:
        - text (str): The input text to summarize.

        Returns:
        - str: The summarized version of the input text.
        """
        # Dynamically set max_length and min_length based on text length
        text_length = len(text)
        
        # Dynamically calculate max_length and min_length
        max_length = min(150, text_length // 2)  # Half the length, but capped at 150
        min_length = max(30, text_length // 10)  # 1/10th the length, but at least 30
        
        # If the text length is smaller than the max_length, adjust it accordingly
        max_length = min(max_length, text_length)
        min_length = min(min_length, max_length)

        # If the text is too long, split it into chunks
        if len(text) > chunk_size:  # Example threshold for chunking
            chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
            chunk_summaries = self._summarize_multiple(chunks, max_length, min_length)
            return " ".join(chunk_summaries)
        else:
            try:
                print(f"Summarizing: {text[:100]}...")  # Debugging message to show the start of the text
                summary = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return summary[0]['summary_text']
            except ValueError as e:
                raise ValueError(f"Summarization error: {str(e)}")

    def _summarize_multiple(self, texts: List[str], max_length: int = 150, min_length: int = 50) -> List[str]:
        """
        Summarize multiple texts sequentially (private method).

        Parameters:
        - texts (List[str]): A list of input texts to summarize.
        - max_length (int): Maximum length of each summary (default: 150).
        - min_length (int): Minimum length of each summary (default: 50).

        Returns:
        - List[str]: A list of summarized texts.
        """
        summaries = []
        
        # Use tqdm to show a progress bar while summarizing multiple texts
        for text in tqdm(texts, desc="Summarizing chunks", unit="chunk"):
            summary = self.summarize(text)
            summaries.append(summary)
        
        return summaries
