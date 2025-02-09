import logging
from summarization.summarizer import TextSummarizer
from text_to_speech.tts import TextToSpeech

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchAndSummarizeChain:
    """A class that combines search and summarization."""
    
    def __init__(self, text_input: str):
        self.text_input = text_input
        logger.info("SearchAndSummarizeChain initialized.")
    
    def run(self):
        """Run the combined search and summarization chain."""
        try:
            logger.info("Running search and summarization.")
            ts = TextSummarizer()

            # Perform summarization in the desired language (e.g., Arabic)
            summary = ts.summarize(f"in arabic: {self.text_input}")
            logger.debug(f"Summary result: {summary[:200]}...")
            return summary
        except Exception as e:
            logger.error(f"Error in summarization: {str(e)}")
            return None

    def speak(self, text: str):
        """Convert text to speech."""
        try:
            tts = TextToSpeech()
            tts.convert_text_to_speech(text)
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting the search and summarize process.")
    
    # Initialize the chain
    search_and_summarize = SearchAndSummarizeChain(text)

    try:
        result = search_and_summarize.run()

        if result:
            logger.info("Final summarized result:")
            logger.info(result)
            search_and_summarize.speak(result)
        else:
            logger.warning("No result to display.")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
