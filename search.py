import logging
from summarization.summarizer import TextSummarizer
from text_to_speech.tts import TextToSpeech
from Reasoner.reasoning import LLMReasoning  # Import the LLMReasoning class
from toMarkdown.Converter import PdfToMarkdown

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchAndSummarizeChain:
    """A class that combines search, iterative reasoning, and summarization."""

    def __init__(self, text_input: str, question: str, iterations: int = 1):
        self.text_input = text_input
        self.question = question
        self.iterations = iterations  # Set the number of iterations for reasoning
        self.llm_reasoner = LLMReasoning()  # Initialize the reasoning module
        logger.info("SearchAndSummarizeChain initialized.")

    def run(self):
        """Run the combined search, iterative reasoning, and summarization chain."""
    
        logger.info(f"Running search, iterative reasoning, and summarization for {self.iterations} iterations.")

        # After the reasoning iterations, summarize the final result
        ts = TextSummarizer()
        summaries = []
        for i, page in enumerate(self.text_input.split("Vol. 6,")):
            summary = ts.summarize(page, len(page)//4)
            summaries.append(summary)
            self.speak(summary, f"{i}.mp3")
        logger.debug(f"Final summary result: {summary[:200]}...")

        return summary
        
    def speak(self, text: str, filename: str):
        """Convert text to speech."""
        try:
            tts = TextToSpeech()
            tts.convert_text_to_speech(text, output_file=filename)
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting the search, iterative reasoning, and summarize process.")

    text = PdfToMarkdown("/workspace/3555154.pdf").convert_pdf_to_markdown()
    print(text)
    question = "summarize and inform me about this"
    
    # Initialize the chain with 4 iterations of reasoning
    search_and_summarize = SearchAndSummarizeChain(text, question, iterations=1)

    try:
        result = search_and_summarize.run()
        import pdb; pdb.set_trace()
        print(f"results:{result}")
        if result:
            logger.info("Final summarized result:")
            logger.info(result)
            search_and_summarize.speak(result)
            print(result)
        else:
            logger.warning("No result to display.")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
