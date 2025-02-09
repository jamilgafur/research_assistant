import logging
import os
from researcher.summarization.summarizer import TextSummarizer
from researcher.text_to_speech.tts import TextToSpeech
from researcher.reasoner.reasoning import LLMReasoning
from researcher.tomarkdown.Converter import PdfToMarkdown
import torch

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchAndSummarizeChain:
    """A class that combines search, iterative reasoning, and summarization."""

    def __init__(self, text_input: str, audio_filename: str = "final_summary.mp3", text_filename: str = "final_summary.txt"):
        self.text_input = text_input
        self.audio_filename = audio_filename  # Path for saving the audio file in the base directory
        self.text_filename = text_filename  # Path for saving the summarized text file
        logger.info("SearchAndSummarizeChain initialized.")

    def run(self):
        """Run the combined search, iterative reasoning, and summarization chain."""
        # After the reasoning iterations, summarize the final result
        ts = TextSummarizer()
        
        # Summarize the text (will handle splitting if needed)
        summary = ts.summarize(self.text_input, chunk_size=2000)
        
        # Save summary to text file
        self.save_summary_to_file(summary)
        
        # Convert summary to speech
        try:
            tts = TextToSpeech()
            tts.convert_text_to_speech(summary, output_file=self.audio_filename)
        except Exception as e :
            logger.error(f"Error converting summary to speech: {str(e)}")

            
        # Clear GPU memory to prevent memory buildup
        self.clear_gpu_memory()
        
        logger.debug(f"Final summary result: {summary[:100]}...")  # Print the first 100 characters of the final summary

        return summary  # Return the final summary

    def save_summary_to_file(self, summary: str):
        """Save the summarized text to a .txt file."""
        try:
            with open(self.text_filename, 'w') as f:
                f.write(summary)
            logger.info(f"Summary saved to {self.text_filename}")
        except Exception as e:
            logger.error(f"Error saving summary to file: {str(e)}")

    def clear_gpu_memory(self):
        """Clear GPU memory to prevent memory buildup."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("GPU memory cleared.")

if __name__ == "__main__":
    logger.info("Starting the search, iterative reasoning, and summarize process.")

    text = PdfToMarkdown("/workspace/3555154.pdf").convert_pdf_to_markdown()
    
    # Initialize the chain with 5 equal chunks and the audio filename in the base directory
    search_and_summarize = SearchAndSummarizeChain(text, audio_filename="3555154.mp3", text_filename="3555154_summary.txt")
    result = search_and_summarize.run()
    
    print(f"Results: {result}")
