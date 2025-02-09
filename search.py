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

        # Initialize the input for reasoning
        current_input = self.text_input

        # Perform iterative reasoning for the specified number of iterations
        for iteration in range(1, self.iterations + 1):
            logger.info(f"Iteration {iteration}: Reasoning with input text.")
            # Perform reasoning with the current input
            reasoning_result = self.llm_reasoner.query(current_input, self.question)
            logger.debug(f"Reasoning result for iteration {iteration}: {reasoning_result[:200]}...")

            # Update the current input with the reasoning result for the next iteration
            current_input = reasoning_result

        # After the reasoning iterations, summarize the final result
        ts = TextSummarizer()
        summary = ts.summarize(f"Final reasoning result: {current_input}")
        logger.debug(f"Final summary result: {summary[:200]}...")

        return summary
        
    def speak(self, text: str):
        """Convert text to speech."""
        try:
            tts = TextToSpeech()
            tts.convert_text_to_speech(text)
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting the search, iterative reasoning, and summarize process.")

    text = PdfToMarkdown("/workspace/3555154.pdf").convert_pdf_to_markdown()
    print(text)
    import pdb; pdb.set_trace()
    question = "summarize and inform me about this"
    
    # Initialize the chain with 4 iterations of reasoning
    search_and_summarize = SearchAndSummarizeChain(text, question, iterations=1)

    try:
        result = search_and_summarize.run()

        if result:
            logger.info("Final summarized result:")
            logger.info(result)
            search_and_summarize.speak(result)
            print(result)
        else:
            logger.warning("No result to display.")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
